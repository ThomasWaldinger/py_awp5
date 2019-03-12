# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
srvinfo
This command returns information about the current P5 server.
"""
from awp5.base.connection import exec_nsdchat
from awp5.base.helpers import onereturnvalue

module_name = "srvinfo"


@onereturnvalue
def buildstamp(p5_connection=None):
    """
    Syntax: srvinfo buildstamp
    Description: Returns the build time-stamp of the P5 release
    Return Values:
    -On Success: The build time-stamp
    """
    method_name = "buildstamp"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def address(p5_connection=None):
    """
    Syntax: srvinfo address
    Description: Returns the IP address of the P5 host
    Return Values:
    -On Success: The IP address in standard dot notation
    """
    method_name = "address"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def hostid(p5_connection=None):
    """
    Syntax: srvinfo hostid
    Description: Returns the host ID of the P5 host (as shown in the about box)
    Return Values:
    -On Success: The host ID
    """
    method_name = "hostid"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def hostname(p5_connection=None):
    """
    Syntax: srvinfo hostname
    Description: Returns the host name of the P5 host
    Return Values:
    -On Success: The host name as returned with the hostname shell command
    """
    method_name = "hostname"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def lexxvers(p5_connection=None):
    """
    Syntax: srvinfo lexxvers
    Description: Returns the P5 application version
    Return Values:
    -On Success: The application version string as X.Y.Z number
    """
    method_name = "lexxvers"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def platform(p5_connection=None):
    """
    Syntax: srvinfo platform
    Description: Returns the OS platform of the P5 host
    Return Values:
    -On Success: One of: linux, solaris, windows or macosx
    """
    method_name = "platform"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def port(p5_connection=None):
    """
    Syntax: srvinfo port
    Description: Returns the TCP port of the P5 server
    Return Values:
    -On Success: The TCP port number
    """
    method_name = "port"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def server(p5_connection=None):
    """
    Syntax: srvinfo server
    Description: Returns the name of the P5 server. Currently there
    is only one server assigned: lexxsrv.
    Return Values:
    -On Success: The server name
    """
    method_name = "server"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def uptime(p5_connection=None):
    """
    Syntax: srvinfo uptime
    Description: Returns the time in seconds since the P5 server was started
    Return Values:
    -On Success: The uptime in seconds
    """
    method_name = "uptime"
    return exec_nsdchat([module_name, method_name], p5_connection)


@onereturnvalue
def version(p5_connection=None):
    """
    Syntax: srvinfo version
    Description: Returns the version of the P5 application server.
    Return Values:
    -On Success: The application server version string as X.Y number
    """
    method_name = "version"
    return exec_nsdchat([module_name, method_name], p5_connection)
