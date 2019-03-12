# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Backup2Go Templates / Workstation Groups
Queries Backup2Go templates configured on the Backup2Go Server and queries and
controls their parameters. These commands are to be executed on the Backup2Go
server.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue

module_name = "Backup2Go"


def names(as_object=False, p5_connection=None):
    """
    Syntax: Backup2Go names
    Description: Returns the list of names of all the Backup2Go templates
    Return Values:
    -On Success:    the list of names
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Backup2Go, p5_connection)


@onereturnvalue
def describe(template_name, p5_connection=None):
    """
    Syntax: Backup2Go <name> describe
    Description: Returns a human-readable description of the template <name>.
    If the template does not have a description assigned, the command returns
    the string "<empty>"
    Return Values:
    -On Success:    the workstation description
    """
    method_name = "describe"
    return exec_nsdchat([module_name, template_name, method_name],
                        p5_connection)


@onereturnvalue
def disabled(template_name, p5_connection=None):
    """
    Syntax: Backup2Go <name> disabled
    Description: Queries Backup2Go template Disabled status
    Return Values:
    -On Success:    the string "1" (disabled) or "0" (not disabled)
    """
    method_name = "disabled"
    return exec_nsdchat([module_name, template_name, method_name],
                        p5_connection)


@onereturnvalue
def enabled(template_name, p5_connection=None):
    """
    Syntax: Backup2Go <name> enabled
    Description: Queries the template Enabled status.
    Return Values:
    -On Success:    the string "1" (enabled) or "0" (not enabled)
    """
    method_name = "enabled"
    return exec_nsdchat([module_name, template_name, method_name],
                        p5_connection)


@onereturnvalue
def disable(template_name, p5_connection=None):
    """
    Syntax: Backup2Go <name> disable
    Description: Sets the template to the Disabled state
    Return Values:
    -On Success:    the string  "0"
    """
    method_name = "disable"
    return exec_nsdchat([module_name, template_name, method_name],
                        p5_connection)


@onereturnvalue
def enable(template_name, p5_connection=None):
    """
    Syntax: Backup2Go <name> enable
    Description: Sets the template to the Enabled state
    Return Values:
    -On Success:    the string  "1"
    """
    method_name = "enable"
    return exec_nsdchat([module_name, template_name, method_name],
                        p5_connection)


@onereturnvalue
def cleanup(template_name, snapshots=False, trashes=False, p5_connection=None):
    """
    Syntax: Backup2Go cleanup [snapshots] [trashes]
    Description: Purges selected Backup2Go areas. It does not wait for the
    completion of the command. Instead, it schedules an internally queued job
    and does the work in the background.
    Return Values:
    -On Success:    the string "ok"
    """
    method_name = "cleanup"
    snapshots_option = ""
    trashes_option = ""
    if snapshots:
        snapshots_option = "snapshots"
    if trashes:
        trashes_option = "trashes"
    return exec_nsdchat([module_name, method_name, snapshots_option,
                         trashes_option], p5_connection)


@onereturnvalue
def maxrunning(template_name, count=None, p5_connection=None):
    """
    Syntax: Backup2Go <name> maxrunning [<count>]
    Description: Set up or report the maximum number of active workstations for
    the given template.
    Return Values:
    -On Success:    the number of active workstations,
                            the string "-1" for unlimited
    """
    method_name = "maxrunning"
    return exec_nsdchat([module_name, template_name, method_name, count],
                        p5_connection)


class Backup2Go(P5Resource):
    def __init__(self, template_name, p5_connection):
        super().__init__(template_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: Backup2Go names
        Description: Returns the list of names of all the Backup2Go templates
        Return Values:
        -On Success:    the list of names
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Backup2Go, p5_connection)

    @onereturnvalue
    def describe(self):
        """
        Syntax: Backup2Go <name> describe
        Description: Returns a human-readable description of the template
        <name>. If the template does not have a description assigned, the
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
        Syntax: Backup2Go <name> disabled
        Description: Queries Backup2Go template Disabled status
        Return Values:
        -On Success:    the string "1" (disabled) or "0" (not disabled)
        """
        method_name = "disabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enabled(self):
        """
        Syntax: Backup2Go <name> enabled
        Description: Queries the template Enabled status.
        Return Values:
        -On Success:    the string "1" (enabled) or "0" (not enabled)
        """
        method_name = "enabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disable(self):
        """
        Syntax: Backup2Go <name> disable
        Description: Sets the template to the Disabled state
        Return Values:
        -On Success:    the string  "0"
        """
        method_name = "disable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enable(self):
        """
        Syntax: Backup2Go <name> enable
        Description: Sets the template to the Enabled state
        Return Values:
        -On Success:    the string  "1"
        """
        method_name = "enable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def cleanup(snapshots=False, trashes=False, p5_connection=None):
        """
        Syntax: Backup2Go cleanup [snapshots] [trashes]
        Description: Purges selected Backup2Go areas. It does not wait for the
        completion of the command. Instead, it schedules an internally queued
        job and does the work in the background.
        Return Values:
        -On Success:    the string "ok"
        """
        method_name = "cleanup"
        snapshots_option = ""
        trashes_option = ""
        if snapshots:
            snapshots_option = "snapshots"
        if trashes:
            trashes_option = "trashes"
        return exec_nsdchat([module_name, method_name, snapshots_option,
                             trashes_option], p5_connection)

    @onereturnvalue
    def maxrunning(self, count=None):
        """
        Syntax: Backup2Go <name> maxrunning [<count>]
        Description: Set up or report the maximum number of active workstations
        for the given template.
        Return Values:
        -On Success:    the number of active workstations,
                                the string "-1" for unlimited
        """
        method_name = "maxrunning"
        count_option = ""
        if count:
            count_option = count
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, count_option])

    def __repr__(self):
        return ": ".join([module_name, self.name])
