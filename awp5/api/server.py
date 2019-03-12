# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Server
Queries P5 Backup2Go server resources configured on the Backup2Go workstation
and their parameters. A P5 server is the computer running the P5 server
software and providing backup services to P5 workstation computers.
These commands are to be executed on the Backup2Go workstation.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.backup2go import Backup2Go
from awp5.api.job import Job

module_name = "Server"


def names(as_object=False, p5_connection=None):
    """
    Syntax: Server names
    Description: Returns the list of names of all configured servers
    Return Values:
    -On Success:    the list of names
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Server, p5_connection)


@onereturnvalue
def create(as_object=False, p5_connection=None):
    """
    Syntax: Server create
    Description: Creates a new server resource
    Return Values:
    -On Success:    the name/ID of the new server resource
    """
    method_name = "create"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Server, p5_connection)


@onereturnvalue
def delete(server_name, p5_connection=None):
    """
    Syntax: Server <name> delete
    Description: Deletes server resource, automatically stopping any scheduled
    job. If any jobs are running, the resource will not be deleted
    Return Values:
    -On Success:    the string "1" if deleted or "0" if not
    """
    method_name = "delete"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def disabled(server_name, p5_connection=None):
    """
    Syntax: Server <name> disabled
    Description: Queries the server Disabled status
    Return Values:
    -On Success:    the string "1" (disabled) or "0" (not disabled)
    """
    method_name = "disabled"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def enabled(server_name, p5_connection=None):
    """
    Syntax: Server <name> enabled
    Description: Queries the server Enabled status.
    Return Values:
    -On Success:    the string “1" (enabled) or "0" (not enabled)
    """
    method_name = "enabled"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def lastbegin(server_name, p5_connection=None):
    """
    Syntax: Server <name> lastbegin
    Description: Returns the absolute time in seconds (Posix time) of the
    beginning of the last backup operation on the server <name>
    Return Values:
    -On Success:    the time in seconds (Posix time)
    """
    method_name = "lastbegin"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def lastend(server_name, p5_connection=None):
    """
    Syntax: Server <name> lastend
    Description: Returns the absolute time in seconds (Posix time) of the
    successful end of the last backup operation on the server <name>. This time
    may be older then the time returned by the lastbegin method, indicating an
    incomplete (interrupted) backup.
    Return Values:
    -On Success:    the time in seconds (Posix time)
    """
    method_name = "lastend"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def nextrun(server_name, p5_connection=None):
    """
    Syntax: Server <name> nextrun
    Description: Returns absolute time in seconds (Posix time) of the beginning
    of the next scheduled backup operation to the server <name>. It will return
    the string "0" if no scheduled backup is present.
    Return Values:
    -On Success:    the time in seconds (Posix time)
    """
    method_name = "nextrun"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def template(server_name, as_object=False, p5_connection=None):
    """
    Syntax: Server <name> template
    Description: Returns the server-side template ID used for the backup
    operation to the server <name>. If no template ID is assigned, it will
    return the string "<empty>".
    Return Values:
    -On Success:    the template ID
    """
    method_name = "template"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def configure(host, port, user_name, password, template=None,
              p5_connection=None):
    """
    Syntax: Server configure <host> <port> <user name> <password> [<template>]
    Description: Creates new (or reuses existing) server resource and
    configures the required connection parameter in a single call.
    If the optional <template> argument is set, it forces the selection of the
    given template on the server, otherwise the default template is used.
    Return Values:
    -On Success:    name/ID of the created server resource
    -On Failure:    a negative integer as a string:
                    "-1": Network connection problem (bad host or port)
                    "-2": Wrong user name or password (log in denied)
                    "-3": The template cannot be set
                           (it is disabled or cannot be found)
    """
    method_name = "configure"
    return exec_nsdchat([module_name, method_name, host, port, user_name,
                         password, template], p5_connection)


@onereturnvalue
def cputhrottle(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> cputhrottle [<value>]
    Description: If no additional arguments specified, returns the workstation
    CPU throttle in percent (0% - 100%). Otherwise interprets the given
    argument as the new throttle value and stores the value.
    Return Values:
    -On Success:    the throttle value in percent
    """
    method_name = "cputhrottle"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def hostname(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> hostname [<value>]
    Description: If no additional arguments are specified, returns the host
    name or IP address of the server. Otherwise it stores the given argument
    as the new host name.
    Return Values:
    -On Success:    the host name
    """
    method_name = "hostname"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def disable(server_name, p5_connection=None):
    """
    Syntax: Server <name> disable
    Description: Sets the server to the Disabled state thereby automatically
    stopping any scheduled job
    Return Values:
    -On Success:    the string "0"
    """
    method_name = "disable"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def enable(server_name, p5_connection=None):
    """
    Syntax: Server <name> enable
    Description: Sets the server to the Enabled state thereby automatically
    scheduling the job
    Return Values:
    -On Success:    the string "1"
    """
    method_name = "enable"
    return exec_nsdchat([module_name, server_name, method_name], p5_connection)


@onereturnvalue
def dataencryption(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> dataencryption [<value>]
    Description: If no additional arguments are specified, returns the boolean
    corresponding string "0" or "1" depending whether the workstation will
    encrypt file contents of the files transferred to this server and store
    them on the server in encrypted form (1) or not (0). Otherwise it stores
    the given argument as the new flag value.
    Return Values:
    -On Success:    the boolean corresponding string "0" or "1"
    """
    method_name = "dataencryption"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def netencryption(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> netencryption [<value>]
    Description: If no additional arguments are specified, returns the boolean
    corresponding string "1" or "0" depending whether the workstation will
    encrypt the network traffic targeted to this server (1) or not (0).
    Otherwise it stores the given argument as the new flag value.
    Return Values:
    -On Success:    the boolean corresponding string "0" or "1"
    """
    method_name = "netencryption"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def netthrottle(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> netthrottle [<value>]
    Description: If no additional arguments are specified, returns the
    bandwidth throttle of the communication link used to talk to this server in
    percents (0% - 100%). Otherwise it stores the given argument as the new
    throttle value.
    Return Values:
    -On Success:    the throttle value in percent
    """
    method_name = "netthrottle"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def password(server_name, value, p5_connection=None):
    """
    Syntax: Server <name> password <value>
    Description: Stores the given argument as the new password.
    Return Values:
    -On Success:    the password
    """
    method_name = "password"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


def pathlist(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> pathlist [<value>]
    Description: If no additional arguments are specified, returns the list of
    paths configured for the backup operation. The paths are delimited by a
    single space character. If one of the returned paths itself contains one or
    more spaces, the complete path is enclosed in curly braces { and }.
    Otherwise it stores the given argument as the new list of paths. Each path
    in the list must be delimited from the next by a single space. If one of
    the given paths itself contains one or more spaces, that whole path must be
    enclosed in curly braces { and }.
    Return Values:
    -On Success:    list of paths separated by a single space
    """
    method_name = "pathlist"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def ping(server_name, timeout=None, p5_connection=None):
    """
    Syntax: Server <name> ping [<timeout>]
    Description: Tests the connection to the <name> server. The optional
    <timeout> argument controls how many seconds to wait for the server
    response. If the argument is omitted, the timeout defaults to 600 seconds
    (10 minutes).
    Return Values:
    -On Success: The string:
    "-2"    wrong user name or password
    "-1"    network connection problem
    "0"     reserved for future use
    "1"     ping ok
    """
    method_name = "ping"
    return exec_nsdchat([module_name, client_name, method_name, timeout],
                        p5_connection)


@onereturnvalue
def port(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> port [<value>]
    Description: If no additional arguments are specified, returns the TCP port
    number of the server. Otherwise it stores the given argument as the new
    port number.
    Return Values:
    -On Success:    the port number
    """
    method_name = "port"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def reschedule(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> reschedule [<value>]
    Description: If no additional arguments are specified, returns the number
    of hours to re-schedule the backup job after regular completion. Note that
    jobs that do not complete regularly are immediately automatically
    rescheduled. Otherwise it stores the given argument as the new number of
    hours.
    Return Values:
    -On Success:    the number of hours
    """
    method_name = "reschedule"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def submit(server_name, now=False, as_object=False, p5_connection=None):
    """
    Syntax: Server <name> submit [<now>]
    Description: Submits the workstation backup job for execution to the server
    <name>. You can optionally override plan execution times by using the
    verbatim string now or the integer value zero for the <now> argument. The
    returned job ID can be used to query the status of the job by using the Job
    resource. Please see the Job resource description for more details.
    Return Values:
    -On Success:    the backup job ID
    """
    method_name = "reschedule"
    now_option = "now"
    if now:
        now_option = now
    result = exec_nsdchat([module_name, server_name, method_name, now_option],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def useevents(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> useevents [<value>]
    Description: If no additional arguments are specified, returns the boolean
    corresponding string "0" or "1", depending on whether the workstation will
    use the file system events facility when gathering files of this server (1)
    to store or will use a linear file system walk (0). Otherwise it stores the
    given argument as the new value.
    Return Values:
    -On Success:    the boolean corresponding string "0" or "1"
    """
    method_name = "useevents"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def usecompression(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> usecompression [<value>]
    Description: If no additional arguments are specified, returns the boolean
    corresponding string "0" or "1" depending whether the workstation will
    compress the network traffic targeted to this server (1) or not (0).
    Otherwise it stores the given argument as the new flag value.
    Return Values:
    -On Success:    the boolean corresponding string "0" or "1"
    """
    method_name = "usecompression"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


@onereturnvalue
def username(server_name, value=None, p5_connection=None):
    """
    Syntax: Server <name> username [<value>]
    Description: If no additional arguments are specified, returns the name of
    the user to use for authentication on the current server. Otherwise it
    stores the given argument as the new user name.
    Return Values:
    -On Success:    the user name
    """
    method_name = "username"
    return exec_nsdchat([module_name, server_name, method_name, value],
                        p5_connection)


class Server(P5Resource):
    def __init__(self, server_name, p5_connection=None):
        super().__init__(server_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: Server names
        Description: Returns the list of names of all configured servers
        Return Values:
        -On Success:    the list of names
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Server, p5_connection)

    @onereturnvalue
    def create(as_object=True, p5_connection=None):
        """
        Syntax: Server create
        Description: Creates a new server resource
        Return Values:
        -On Success:    the name/ID of the new server resource
        """
        method_name = "create"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Server, p5_connection)

    @onereturnvalue
    def delete(self):
        """
        Syntax: Server <name> delete
        Description: Deletes server resource, automatically stopping any
        scheduled job. If any jobs are running, the resource will not be
        deleted
        Return Values:
        -On Success:    the string "1" if deleted or "0" if not
        """
        method_name = "delete"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def disabled(self):
        """
        Syntax: Server <name> disabled
        Description: Queries the server Disabled status
        Return Values:
        -On Success:    the string "1" (disabled) or "0" (not disabled)
        """
        method_name = "disabled"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def enabled(self):
        """
        Syntax: Server <name> enabled
        Description: Queries the server Enabled status.
        Return Values:
        -On Success:    the string “1" (enabled) or "0" (not enabled)
        """
        method_name = "enabled"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def lastbegin(self):
        """
        Syntax: Server <name> lastbegin
        Description: Returns the absolute time in seconds (Posix time) of the
        beginning of the last backup operation on the server <name>
        Return Values:
        -On Success:    the time in seconds (Posix time)
        """
        method_name = "lastbegin"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def lastend(self):
        """
        Syntax: Server <name> lastend
        Description: Returns the absolute time in seconds (Posix time) of the
        successful end of the last backup operation on the server <name>. This
        time may be older then the time returned by the lastbegin method,
        indicating an incomplete (interrupted) backup.
        Return Values:
        -On Success:    the time in seconds (Posix time)
        """
        method_name = "lastend"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def nextrun(self):
        """
        Syntax: Server <name> nextrun
        Description: Returns absolute time in seconds (Posix time) of the
        beginning of the next scheduled backup operation to the server <name>.
        It will return the string "0" if no scheduled backup is present.
        Return Values:
        -On Success:    the time in seconds (Posix time)
        """
        method_name = "nextrun"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def template(self):
        """
        Syntax: Server <name> template
        Description: Returns the server-side template ID used for the backup
        operation to the server <name>. If no template ID is assigned, it will
        return the string "<empty>".
        Return Values:
        -On Success:    the template ID
        """
        method_name = "template"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def configure(host, port, user_name, password, template=None,
                  p5_connection=None):
        """
        Syntax: Server configure <host> <port> <user name> <password>
        [<template>]
        Description: Creates new (or reuses existing) server resource and
        configures the required connection parameter in a single call.
        If the optional <template> argument is set, it forces the selection of
        the given template on the server, otherwise the default template is
        used.
        Return Values:
        -On Success:    name/ID of the created server resource
        -On Failure:    a negative integer as a string:
                        "-1": Network connection problem (bad host or port)
                        "-2": Wrong user name or password (log in denied)
                        "-3": The template cannot be set
                               (it is disabled or cannot be found)
        """
        method_name = "configure"
        return exec_nsdchat([module_name, method_name, host, port, user_name,
                             password, template], p5_connection)

    @onereturnvalue
    def cputhrottle(self, value=None):
        """
        Syntax: Server <name> cputhrottle [<value>]
        Description: If no additional arguments specified, returns the
        workstation CPU throttle in percent (0% - 100%). Otherwise interprets
        the given argument as the new throttle value and stores the value.
        Return Values:
        -On Success:    the throttle value in percent
        """
        method_name = "cputhrottle"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def hostname(self, value=None):
        """
        Syntax: Server <name> hostname [<value>]
        Description: If no additional arguments are specified, returns the host
        name or IP address of the server. Otherwise it stores the given
        argument as the new host name.
        Return Values:
        -On Success:    the host name
        """
        method_name = "hostname"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def disable(self):
        """
        Syntax: Server <name> disable
        Description: Sets the server to the Disabled state thereby
        automatically stopping any scheduled job
        Return Values:
        -On Success:    the string "0"
        """
        method_name = "disable"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def enable(self):
        """
        Syntax: Server <name> enable
        Description: Sets the server to the Enabled state thereby automatically
        scheduling the job
        Return Values:
        -On Success:    the string "1"
        """
        method_name = "enable"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name])

    @onereturnvalue
    def dataencryption(self, value=None):
        """
        Syntax: Server <name> dataencryption [<value>]
        Description: If no additional arguments are specified, returns the
        boolean corresponding string "0" or "1" depending whether the
        workstation will encrypt file contents of the files transferred to this
        server and store them on the server in encrypted form (1) or not (0).
        Otherwise it stores the given argument as the new flag value.
        Return Values:
        -On Success:    the boolean corresponding string "0" or "1"
        """
        method_name = "dataencryption"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def netencryption(self, value=None):
        """
        Syntax: Server <name> netencryption [<value>]
        Description: If no additional arguments are specified, returns the
        boolean corresponding string "1" or "0" depending whether the
        workstation will encrypt the network traffic targeted to this server
        (1) or not (0). Otherwise it stores the given argument as the new flag
        value.
        Return Values:
        -On Success:    the boolean corresponding string "0" or "1"
        """
        method_name = "netencryption"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def netthrottle(self, value=None):
        """
        Syntax: Server <name> netthrottle [<value>]
        Description: If no additional arguments are specified, returns the
        bandwidth throttle of the communication link used to talk to this
        server in percents (0% - 100%). Otherwise it stores the given
        argument as the new throttle value.
        Return Values:
        -On Success:    the throttle value in percent
        """
        method_name = "netthrottle"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def password(self, value):
        """
        Syntax: Server <name> password <value>
        Description: Stores the given argument as the new password.
        Return Values:
        -On Success:    the password
        """
        method_name = "password"
        return exec_nsdchat([module_name, server_name, method_name, value],
                            p5_connection)

    def pathlist(self, value=None):
        """
        Syntax: Server <name> pathlist [<value>]
        Description: If no additional arguments are specified, returns the list
        of paths configured for the backup operation. The paths are delimited
        by a single space character. If one of the returned paths itself
        contains one or more spaces, the complete path is enclosed in curly
        braces { and }.
        Otherwise it stores the given argument as the new list of paths. Each
        path in the list must be delimited from the next by a single space. If
        one of the given paths itself contains one or more spaces, that whole
        path must be enclosed in curly braces { and }.
        Return Values:
        -On Success:    list of paths separated by a single space
        """
        method_name = "pathlist"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def ping(self, timeout=None):
        """
        Syntax: Server <name> ping [<timeout>]
        Description: Tests the connection to the <name> server. The optional
        <timeout> argument controls how many seconds to wait for the server
        response. If the argument is omitted, the timeout defaults to 600
        seconds (10 minutes).
        Return Values:
        -On Success: The string:
        "-2"    wrong user name or password
        "-1"    network connection problem
        "0"     reserved for future use
        "1"     ping ok
        """
        method_name = "ping"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, timeout])

    @onereturnvalue
    def port(self, value=None):
        """
        Syntax: Server <name> port [<value>]
        Description: If no additional arguments are specified, returns the TCP
        port number of the server. Otherwise it stores the given argument as
        the new port number.
        Return Values:
        -On Success:    the port number
        """
        method_name = "port"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def reschedule(self, value=None):
        """
        Syntax: Server <name> reschedule [<value>]
        Description: If no additional arguments are specified, returns the
        number of hours to re-schedule the backup job after regular completion.
        Note that jobs that do not complete regularly are immediately
        automatically rescheduled. Otherwise it stores the given argument as
        the new number of hours.
        Return Values:
        -On Success:    the number of hours
        """
        method_name = "reschedule"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def submit(self, now=False, as_object=True):
        """
        Syntax: Server <name> submit [<now>]
        Description: Submits the workstation backup job for execution to the
        server <name>. You can optionally override plan execution times by
        using the verbatim string now or the integer value zero for the <now>
        argument. The returned job ID can be used to query the status of the
        job by using the Job resource. Please see the Job resource description
        for more details.
        Return Values:
        -On Success:    the backup job ID
        """
        method_name = "reschedule"
        now_option = "now"
        if now:
            now_option = now
        result = self.p5_connection.nsdchat_call([modulname, self.name,
                                                  method_name, now_option])
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, self.p5_connection)

    @onereturnvalue
    def useevents(self, value=None):
        """
        Syntax: Server <name> useevents [<value>]
        Description: If no additional arguments are specified, returns the
        boolean corresponding string "0" or "1", depending on whether the
        workstation will use the file system events facility when gathering
        files of this server (1) to store or will use a linear file system walk
        (0). Otherwise it stores the given argument as the new value.
        Return Values:
        -On Success:    the boolean corresponding string "0" or "1"
        """
        method_name = "useevents"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def usecompression(self, value=None):
        """
        Syntax: Server <name> usecompression [<value>]
        Description: If no additional arguments are specified, returns the
        boolean corresponding string "0" or "1" depending whether the
        workstation will compress the network traffic targeted to this server
        (1) or not (0). Otherwise it stores the given argument as the new flag
        value.
        Return Values:
        -On Success:    the boolean corresponding string "0" or "1"
        """
        method_name = "usecompression"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    @onereturnvalue
    def username(self, value=None):
        """
        Syntax: Server <name> username [<value>]
        Description: If no additional arguments are specified, returns the name
        of the user to use for authentication on the current server. Otherwise
        it stores the given argument as the new user name.
        Return Values:
        -On Success:    the user name
        """
        method_name = "username"
        return self.p5_connection.nsdchat_call([modulname, self.name,
                                                method_name, value])

    def __repr__(self):
        return ": ".join([module_name, self.name])
