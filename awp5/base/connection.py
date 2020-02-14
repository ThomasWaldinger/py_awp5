# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Use the Connection class for accessing the nsdchat commandline.
"""
import hashlib
import time
import sys
import subprocess
import errno
import logging
import os
import locale
from awp5.base import config
from awp5.base.helpers import strings, defaultIfNotSet, singlevalue


class ConnectionBase(object):
    string_template = 'awsock:/{user}:{password}:{sessionid}@{hostip}:{port}'

    def __init__(self, p5_user, p5_pass, p5_ip, p5_port_nr, p5_path):
        self.p5_user = defaultIfNotSet(p5_user, config.p5_user)
        self.p5_pass = defaultIfNotSet(p5_pass, config.p5_pass)
        self.p5_ip = defaultIfNotSet(p5_ip, p5_ip)
        self.p5_port_nr = defaultIfNotSet(p5_port_nr, config.p5_port_nr)
        self.p5_path = defaultIfNotSet(p5_path, config.p5_path)


class Connection(ConnectionBase):
    """
    Stores the connection and session data used to communicate with p5 via
    the nsdchat executable and awsock protocol
    """
    
    default_connection = None
    """
    The default connection is initialized with the first Connection object
    created. If 'Connection.prefer_last_connection=False' it's settings are used
    in resulting nsdchat calls if no explicit Connection object is
    passed to the awp5 operations or during the creation of P5Resource objects.
    """
    
    last_connection = None
    """
    holds the last Connection object used to communicate with P5
    If 'Connection.prefer_last_connection=True' it's settings are used
    in resulting nsdchat calls if no explicit Connection object is
    passed to the awp5 operations or during the creation of P5Resource objects.
    """
    
    prefer_last_connection = False
    """
    defines wich connection settings should be used if no explicit Connection is
    defined for a awp5 operation. Set this to true only when working with
    subroutines using a own connection session id and only in single threaded
    applications.
    """
    logger = logging.getLogger('awp5')

    def __init__(self, p5_user=None, p5_pass=None,
                 p5_ip=None, p5_port_nr=None,
                 p5_path=None, sessionid=None):
        super().__init__(defaultIfNotSet(p5_user, config.p5_user),
                         defaultIfNotSet(p5_pass, config.p5_pass),
                         defaultIfNotSet(p5_ip, config.p5_ip),
                         defaultIfNotSet(p5_port_nr, config.p5_port_nr),
                         defaultIfNotSet(p5_path, config.p5_path))
        self.debugMsg = False
        self.connection_string = None
        self.session_id = None
        if not self.session_id:
            self.session_id = "_".join(["awp5", hashlib.sha224(str(time.time())
                                                               .encode('utf-8')
                                                               ).hexdigest()])
        else:
            self.session_id = sessionid
        if sys.platform == 'win32':
            self.nsdchat = os.path.join(self.p5_path, 'bin', 'nsdchat.exe')
        else:
            self.nsdchat = os.path.join(self.p5_path, 'bin', 'nsdchat')
        if not Connection.default_connection:
            Connection.default_connection = self

    def getConnectionString(self):
        if not self.connection_string:
            self.connection_string = Connection.string_template.format(
                                     user=self.p5_user, password=self.p5_pass,
                                     sessionid=self.session_id,
                                     hostip=self.p5_ip, port=self.p5_port_nr
                                     + 1001)
        return self.connection_string

    def test(self,version=''):
        """
        tries to connect to the P5 Server and returns True if the server is
        available and runs at least the given 'version'. False if version is
        lower.
        If no connection could be made the nsdchat executable does timeout and
        a 'subprocess.TimeoutExpired' execption will be raised.
        """
        p5cmd = ['srvinfo', 'lexxvers']
        try:
            res = self.nsdchat_call(p5cmd,5)
            p5_version = singlevalue(res)
            if (p5_version >= str(version)):
                return True
            return False
        except subprocess.TimeoutExpired:
            print("Could not connect to the archiware p5 server.\nPlease review"
            "the connection and firewall settings.")
            raise
        

    def get():
        if Connection.prefer_last_connection and Connection.last_connection:
            return Connection.last_connection
        elif Connection.default_connection:
            return Connection.default_connection
        raise AssertionError("No Connection has been established yet. Create a"
                             " connection object first")

    def geterror(self):
        """
        Returns the error message associated with the last issued CLI command.
        You should invoke this command after getting an empty result string
        from any CLI command to receive an explanation for the encountered
        error.
        """
        c = [self.nsdchat, '-s', self.connection_string, '-c', 'geterror']
        process = subprocess.Popen(
                c, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if (process.returncode != 0):
            Connection.logger.error("nsdchat exited with errorcode "
                                    "{rc}.".format(rc=process.returncode))
        else:
            return out.decode('utf-8')

    def nsdchat_call(self, cmd, timeout=10):
        nsdcmd = [self.nsdchat, '-s', self.getConnectionString(), '-c']
        c = nsdcmd + strings(cmd)
        process = subprocess.Popen(
            c, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(timeout=timeout)
        if (process.returncode != 0 and out.strip() == ''):
            Connection.logger.error("P5 error while executing '{}'".format(cmd))
            Connection.logger.error(self.geterror())
            return None
        try:
            res = out.decode('utf-8').strip().split(' ')
        except UnicodeDecodeError:
            res = out.decode(locale.getpreferredencoding()).strip().split(' ')
        Connection.last_connection = self
        return res


class P5Resource(object):
    def __init__(self, name, p5_connection):
        self.name = name
        if not p5_connection:
            p5_connection = Connection.get()
        self.p5_connection = p5_connection

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.name == other.name and self.p5_connection == \
                                                    other.p5_connection
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return self.name != other.name or self.p5_connection != \
                                                    other.p5_connection
        elif isinstance(other, str):
            return self.name != other
        else:
            raise TypeError("other must be a str or {} instance"
                             "".format(type(self)))
            
def exec_nsdchat(cmd, p5_connection=None):
    if not p5_connection:
        p5_connection = Connection.get()
    return p5_connection.nsdchat_call(cmd)
