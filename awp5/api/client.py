# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Client
Queries configured P5 client resources and their parameters. A P5 client is the
computer running the P5 client software. A P5 server is the computer running
the P5 server software. A server can archive, backup, restore and synchronize
files to and from any registered client.
In the current version of the CLI, there is only read access to client data.
You can't modify any of the existing client resources nor can you create new or
delete existing clients. To configure and maintain client resources, use the
standard system administrator account in the P5 Web GUI.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue

module_name = "Client"


def names(as_objects=False, p5_connection=None):
    """
    Syntax: Client <name> describe
    Description: Returns a human-readable description of the client <name>. If
    the client does not have a description assigned, the command returns the
    string "<empty>"
    Return Values:
    -On Success:    the client description
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_objects:
        return result
    else:
        return resourcelist(result, Client, p5_connection)


@onereturnvalue
def describe(client_name, p5_connection=None):
    """
    Syntax: Client <name> describe
    Description: Returns a human-readable description of the client <name>. If
    the client does not have .
    Return Values:
    -On Success:    the client description
    """
    method_name = "describe"
    return exec_nsdchat([module_name, client_name, method_name], p5_connection)


@onereturnvalue
def hostname(client_name, p5_connection=None):
    """
    Syntax: Client <name> hostname
    Description: Returns the host name (or IP address) of the client <name>
    Return Values:
    -On Success:    the host name or IP address
    """
    method_name = "hostname"
    return exec_nsdchat([module_name, client_name, method_name], p5_connection)


@onereturnvalue
def isthin(client_name, p5_connection=None):
    """
    Syntax: Client <name> isthin
    Description: Returns true in case the client is of type Workstation  (as
    opposed to type Server)
    Return Values:
    -On Success:    the string “1” if the client type is Workstation
                    the string “0”  otherwise
    """
    method_name = "isthin"
    return exec_nsdchat([module_name, client_name, method_name], p5_connection)


@onereturnvalue
def port(client_name, p5_connection=None):
    """
    Syntax: Client <name> port
    Description: Returns the TCP port of the client <name>
    Return Values:
    -On Success:    the configured TCP port
    """
    method_name = "port"
    return exec_nsdchat([module_name, client_name, method_name], p5_connection)


@onereturnvalue
def ping(client_name, timeout=None, p5_connection=None):
    """
    Syntax: Client <name> ping [<timeout>]
    Description: Tests the connection to the <name> client. The optional
    <timeout> argument controls how many seconds to wait for the client
    response. If the argument is omitted, the timeout defaults to 600 seconds
    (10 minutes).
    Return Values:
    -On Success: The string:
    "-4"    wrong client version
    "-3"    the client is disabled
    "-2"    wrong user name/password
    "-1"    network connection problem
    "0"     (reserved for future use)
    "1"     ping OK
    """
    method_name = "ping"
    timeout_option = ""
    if timeout:
        timeout_option = timeout
    method_name = "ping"
    return exec_nsdchat([module_name, client_name, method_name,
                        timeout_option], p5_connection)


class Client(P5Resource):
    def __init__(self, client_name, p5_connection=None):
        super().__init__(client_name, p5_connection)

    def names(as_objects=True, p5_connection=None):
        """
        Syntax: Client <name> describe
        Description: Returns a human-readable description of the client <name>.
        If the client does not have a description assigned, the command returns
        the string "<empty>"
        Return Values:
        -On Success:    the client description
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_objects:
            return result
        else:
            return resourcelist(result, Client, p5_connection)

    @onereturnvalue
    def describe(self):
        """
        Syntax: Client <name> describe
        Description: Returns a human-readable description of the client <name>.
        If the client does not have a description assigned, the command returns
        the string "<empty>"
        Return Values:
        -On Success:    the client description
        """
        method_name = "describe"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def hostname(self):
        """
        Syntax: Client <name> hostname
        Description: Returns the host name (or IP address) of the client <name>
        Return Values:
        -On Success:    the host name or IP address
        """
        method_name = "hostname"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def isthin(self):
        """
        Syntax: Client <name> isthin
        Description: Returns true in case the client is of type Workstation (as
        opposed to type Server)
        Return Values:
        -On Success:    the string “1” if the client type is Workstation
                        the string “0”  otherwise
        """
        method_name = "isthin"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def port(self):
        """
        Syntax: Client <name> port
        Description: Returns the TCP port of the client <name>
        Return Values:
        -On Success:    the configured TCP port
        """
        method_name = "port"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def ping(self, timeout=None):
        """
        Syntax: Client <name> ping [<timeout>]
        Description: Tests the connection to the <name> client. The optional
        <timeout> argument controls how many seconds to wait for the client
        response. If the argument is omitted, the timeout defaults to 600
        seconds (10 minutes).
        Return Values:
        -On Success: The string:
        "-4"    wrong client version
        "-3"    the client is disabled
        "-2"    wrong user name/password
        "-1"    network connection problem
        "0"     (reserved for future use)
        "1"     ping OK
        """
        method_name = "ping"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, timeout])

    def __repr__(self):
        return ": ".join([module_name, self.name])
