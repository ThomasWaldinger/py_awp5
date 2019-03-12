# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Workstation
Queries Backup2Go workstation resources configured on the Backup2Go Server and
queries and controls their parameters. These commands are to be executed on the
Backup2Go server.
A P5 workstation is the computer running the P5 client software in a Backup2Go
infrastructure. To configure and maintain workstation resources, use the
standard system-administrator account in the P5 Web GUI
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.backup2go import Backup2Go

module_name = "Workstation"


def names(as_object=False, p5_connection=None):
    """
    Syntax: Workstation names
    Description: Returns the list of names of all workstations
    Return Values:
    -On Success:    the list of names
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Workstation, p5_connection)


@onereturnvalue
def describe(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> describe
    Description: Returns a human-readable description of the workstation
    <name>.
    If the workstation does not have a description assigned, the command
    returns the string "<empty>"
    Return Values:
    -On Success:    the workstation description
    """
    method_name = "describe"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def disabled(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> disabled
    Description: Queries the workstations Disabled status
    Return Values:
    -On Success:    the string "1" (disabled) or "0" (enabled)
    """
    method_name = "disabled"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def enabled(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> enabled
    Description: Queries the workstation Enabled status
    Return Values:
    -On Success:    the string "1" (enabled) or "0" (disabled)
    """
    method_name = "enabled"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def hostid(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> hostid
    Description: Returns the configured P5 machine-ID of the workstation
    <name>.
    Return Values:
    -On Success:    the workstation's machine ID
    """
    method_name = "hostid"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def lastbegin(workstation_name, p5_connection=None):
    """
    Syntax: Workstation<name> lastbegin
    Description: Returns the absolute time in seconds (Posix time) of the start
    of the last backup operation for the workstation <name>
    Return Values:
    -On Success:    the time in seconds (Posix time)
    """
    method_name = "lastbegin"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def lastend(workstation_name, p5_connection=None):
    """
    Syntax: Workstation<name> lastend
    Description: Returns the absolute time in seconds (Posix time) of the
    successful end of the last backup operation for the workstation <name>.
    This time may be older then the time returned by the lastbegin method
    indicating an incomplete (interrupted) backup.
    Return Values:
    -On Success:    the time in seconds (Posix time)
    """
    method_name = "lastend"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def lasterror(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> lasterror
    Description: Returns the error message that resulted from the last backup
    run for the workstation <name>.
    The string "<empty>" is returned in case there is no last error.
    Return Values:
    -On Success:    the error message or the string "<empty>"
    """
    method_name = "lasterror"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def nextrun(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> nextrun
    Description: Returns the absolute time in seconds (Posix time) of the next
    anticipated backup of the workstation
    Return Values:
    -On Success:    the time in seconds (Posix time)
    """
    method_name = "nextrun"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def peerip(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> peerip
    Description: Returns the last known IP of the workstation <name>. If the
    workstation does not have an IP recorded so far (for example, it never got
    connected to the server), the command returns the string "<empty>"
    Return Values:
    -On Success:    the workstation IP address in standard dot notation
    """
    method_name = "peerip"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def snapshots(workstation_name, since="", p5_connection=None):
    """
    Syntax: Workstation <name> snapshots [<since>]
    Description: Returns a list of snapshots maintained for the given
    workstation. The optional <since> argument may be given in seconds (Posix
    time) to address only snapshots since that date. Otherwise all known
    snapshots are returned.
    Return Values:
    -On Success:    a list of snapshots IDs
    """
    method_name = "snapshots"
    return exec_nsdchat([module_name, workstation_name, method_name, since],
                        p5_connection)


@onereturnvalue
def snapsize(workstation_name, snapshotId, p5_connection=None):
    """
    Syntax: Workstation <name> snapsize [<snapshotId>]
    Description: Returns the allocated size in KBytes of data maintained for
    the named workstation.
    On link based snapshots, one or multiple <snapshotId> arguments (as
    returned by the snapshots method) can be given. The return value is then
    the allocated size for the current and all optional given snapshots summed
    up. On native snapshots (ZFS, BTRFS), this method accepts one or none
    <snapshotId> as parameter. If a snapshot ID is given, the logical size of
    that snapshot is returned, otherwise the size of the current state is
    returned. The return value does not reflect the required disk space of
    native snapshots. All returned sizes are in Kbyte.
    Note that this may be a lengthy operation, depending on the number of files
    and snapshots.
    Return Values:
    -On Success:    the number of KBytes
    """
    method_name = "snapsize"
    return exec_nsdchat([module_name, workstation_name, method_name,
                         snapshotId], p5_connection)


@onereturnvalue
def totalfiles(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> totalfiles
    Description: Returns the number of files transferred from the workstation
    <name> in the last backup operation
    Return Values:
    -On Success:    the number of files
    """
    method_name = "peerip"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def totalkbytes(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> totalkbytes
    Description: Returns the number of KBytes transferred from the workstation
    <name> in the last backup operation
    Return Values:
    -On Success:    the number of KBytes
    """
    method_name = "peerip"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def retaintime(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> retaintime
    Description: Returns the retention time setting for workstation snapshots.
    Return Values:
    -On Success:    the retention time in seconds
    """
    method_name = "peerip"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def template(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> template
    Description: Returns the template ID for workstation <name>.
    Return Values:
    -On Success:    the template ID
    """
    method_name = "template"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def configure(hostname, port, username, password, template="",
              p5_connection=None):
    """
    Syntax: Workstation configure <hostname> <port> <username> <password>
    [<template>]
    Description: Run this command on the P5 Backup2Go Server.
    Using the passed connection parameters <hostname> and <port>, tries to
    establish the connection to the remote workstation and, based on it's host
    ID, create or reuse the workstation record on the server.
    For the purpose of logging in to the server, the workstation will be seeded
    with a unique token, shared by the workstation and the server. This
    eliminates the need for storing the <username> and/or <password> for
    accessing the server on the workstation.
    If the optional <template> is given, the workstation is set to use the
    given template. Otherwise the workstation is set to use the generic
    template.
    Return Values:
    -On Success:    a positive integer as a string
                    (the name of the new local workstation)
    -On Failure:    the string "-3": the template could not be set
                    the string "-2": a wrong user name/password is given
                    the string "-1": there is a network connection problem
                                                (bad address and/or port)
    """
    method_name = "configure"
    return exec_nsdchat([module_name, method_name, hostname, port, username,
                         password, template], p5_connection)


@onereturnvalue
def disable(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> disable
    Description: Sets the workstation to the Disabled state
    Return Values:
    -On Success:    the string  "0"
    """
    method_name = "disable"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def enable(workstation_name, p5_connection=None):
    """
    Syntax: Workstation <name> enable
    Description: Sets the workstation to the Enabled state
    Return Values:
    -On Success:    the string  "1"
    """
    method_name = "enable"
    return exec_nsdchat([module_name, workstation_name, method_name],
                        p5_connection)


@onereturnvalue
def name(p5_connection=None):
    """
    Syntax: Workstation name
    Description: Returns the Workstation ID of the workstation where the
    command is executed
    Note:
    Unlike all the other workstation commands, this command must be called on
    the Workstation
    Return Values:
    -On Success:    the ID or the string “unknown”
    """
    method_name = "name"
    return exec_nsdchat([module_name, method_name], p5_connection)


class Workstation(P5Resource):
    def __init__(self, workstation_name, p5_connection=None):
        super().__init__(workstation_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: Workstation names
        Description: Returns the list of names of all workstations
        Return Values:
        -On Success:    the list of names
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Workstation, p5_connection)

    @onereturnvalue
    def describe(self):
        """
        Syntax: Workstation <name> describe
        Description: Returns a human-readable description of the workstation
        <name>. If the workstation does not have a description assigned, the
        command returns the string "<empty>"
        Return Values:
        -On Success:    the workstation description
        """
        method_name = "describe"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disabled(self):
        """
        Syntax: Workstation <name> disabled
        Description: Queries the workstations Disabled status
        Return Values:
        -On Success:    the string "1" (disabled) or "0" (enabled)
        """
        method_name = "disabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enabled(self):
        """
        Syntax: Workstation <name> enabled
        Description: Queries the workstation Enabled status
        Return Values:
        -On Success:    the string "1" (enabled) or "0" (disabled)
        """
        method_name = "enabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def hostid(self):
        """
        Syntax: Workstation <name> hostid
        Description: Returns the configured P5 machine-ID of the workstation
        <name>.
        Return Values:
        -On Success:    the workstation's machine ID
        """
        method_name = "hostid"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def lastbegin(self):
        """
        Syntax: Workstation<name> lastbegin
        Description: Returns the absolute time in seconds (Posix time) of the
        start of the last backup operation for the workstation <name>
        Return Values:
        -On Success:    the time in seconds (Posix time)
        """
        method_name = "lastbegin"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def lastend(self):
        """
        Syntax: Workstation<name> lastend
        Description: Returns the absolute time in seconds (Posix time) of the
        successful end of the last backup operation for the workstation <name>.
        This time may be older then the time returned by the lastbegin method
        indicating an incomplete (interrupted) backup.
        Return Values:
        -On Success:    the time in seconds (Posix time)
        """
        method_name = "lastend"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def lasterror(self):
        """
        Syntax: Workstation <name> lasterror
        Description: Returns the error message that resulted from the last
        backup run for the workstation <name>.
        The string "<empty>" is returned in case there is no last error.
        Return Values:
        -On Success:    the error message or the string "<empty>"
        """
        method_name = "lasterror"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def nextrun(self):
        """
        Syntax: Workstation <name> nextrun
        Description: Returns the absolute time in seconds (Posix time) of the
        next anticipated backup of the workstation
        Return Values:
        -On Success:    the time in seconds (Posix time)
        """
        method_name = "nextrun"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def peerip(self):
        """
        Syntax: Workstation <name> peerip
        Description: Returns the last known IP of the workstation <name>. If
        the workstation does not have an IP recorded so far (for example, it
        never got connected to the server), the command returns the string
        "<empty>"
        Return Values:
        -On Success:    the workstation IP address in standard dot notation
        """
        method_name = "peerip"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def snapshots(self, since=""):
        """
        Syntax: Workstation <name> snapshots [<since>]
        Description: Returns a list of snapshots maintained for the given
        workstation. The optional <since> argument may be given in seconds
        (Posix time) to address only snapshots since that date. Otherwise all
        known snapshots are returned.
        Return Values:
        -On Success:    a list of snapshots IDs
        """
        method_name = "snapshots"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, since])

    @onereturnvalue
    def snapsize(self, snapshotId):
        """
        Syntax: Workstation <name> snapsize [<snapshotId>]
        Description: Returns the allocated size in KBytes of data maintained
        for the named workstation. On link based snapshots, one or multiple
        <snapshotId> arguments (as returned by the snapshots method) can be
        given. The return value is then the allocated size for the current and
        all optional given snapshots summed up.
        On native snapshots (ZFS, BTRFS), this method accepts one or none
        <snapshotId> as parameter. If a snapshot ID is given, the logical size
        of that snapshot is returned, otherwise the size of the current state
        is returned. The return value does not reflect the required disk space
        of native snapshots. All returned sizes are in Kbyte.
        Note that this may be a lengthy operation, depending on the number of
        files and snapshots.
        Return Values:
        -On Success:    the number of KBytes
        """
        method_name = "snapsize"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, snapshotId])

    @onereturnvalue
    def totalfiles(self):
        """
        Syntax: Workstation <name> totalfiles
        Description: Returns the number of files transferred from the
        workstation <name> in the last backup operation
        Return Values:
        -On Success:    the number of files
        """
        method_name = "peerip"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def totalkbytes(self):
        """
        Syntax: Workstation <name> totalkbytes
        Description: Returns the number of KBytes transferred from the
        workstation <name> in the last backup operation
        Return Values:
        -On Success:    the number of KBytes
        """
        method_name = "peerip"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def retaintime(self):
        """
        Syntax: Workstation <name> retaintime
        Description: Returns the retention time setting for workstation
        snapshots.
        Return Values:
        -On Success:    the retention time in seconds
        """
        method_name = "peerip"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def template(self):
        """
        Syntax: Workstation <name> template
        Description: Returns the template ID for workstation <name>.
        Return Values:
        -On Success:    the template ID
        """
        method_name = "template"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def configure(hostname, port, username, password, template="",
                  p5_connection=None):
        """
        Syntax: Workstation configure <hostname> <port> <username> <password>
        [<template>]
        Description: Run this command on the P5 Backup2Go Server.
        Using the passed connection parameters <hostname> and <port>, tries to
        establish the connection to the remote workstation and, based on it's
        host ID, create or reuse the workstation record on the server.
        For the purpose of logging in to the server, the workstation will be
        seeded with a unique token, shared by the workstation and the server.
        This eliminates the need for storing the <username> and/or <password>
        for accessing the server on the workstation.
        If the optional <template> is given, the workstation is set to use the
        given template. Otherwise the workstation is set to use the generic
        template.
        Return Values:
        -On Success:    a positive integer as a string
                        (the name of the new local workstation)
        -On Failure:    the string "-3": the template could not be set
                        the string "-2": a wrong user name/password is given
                        the string "-1": there is a network connection problem
                                                    (bad address and/or port)
        """
        method_name = "configure"
        return exec_nsdchat([module_name, method_name, hostname, port,
                             username, password, template],
                            p5_connection)

    @onereturnvalue
    def disable(self):
        """
        Syntax: Workstation <name> disable
        Description: Sets the workstation to the Disabled state
        Return Values:
        -On Success:    the string  "0"
        """
        method_name = "disable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enable(self):
        """
        Syntax: Workstation <name> enable
        Description: Sets the workstation to the Enabled state
        Return Values:
        -On Success:    the string  "1"
        """
        method_name = "enable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def name(p5_connection=None):
        """
        Syntax: Workstation name
        Description: Returns the Workstation ID of the workstation where the
        command is executed
        Note:
        Unlike all the other workstation commands, this command must be called
        on the Workstation
        Return Values:
        -On Success:    the ID or the string “unknown”
        """
        method_name = "name"
        return exec_nsdchat([module_name, method_name], p5_connection)

    def __repr__(self):
        return ": ".join([module_name, self.name])
