# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
BackupPlan
Queries P5 backup plans and their associated parameters. Backup plans are used
to group various parameters of the backup operation, like the pool of media,
time schedules and other details. The P5 administrator defines backup plans
according to the custom site policies.
In the current version of the CLI, the backup plans can only be queried but not
changed, nor can plans be added or deleted. To configure and maintain backup
plan resources, use the standard system administrator account in the
P5 Web GUI.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.client import Client
from awp5.api.job import Job

module_name = "BackupPlan"


def names(as_object=False, p5_connection=None):
    """
    Syntax: BackupPlan names
    Description: Returns a list of names of all the BackupPlan resources
    Return Values:
    -On Success:    a list of names. If no backup plans have been
                    configured, the command returns the string
                    "<empty>"
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, BackupPlan, p5_connection)


@onereturnvalue
def describe(backupplan_name, p5_connection=None):
    """
    Syntax: BackupPlan <name> describe
    Description: Returns a human-readable description for the <name> plan. The
    <name> is one of the elements returned by the names method. If the element
    does not have a description assigned, the command returns the string
    "<empty>".
    Return Values:
    -On Success:    the resource description. If no description has been set
                    the command returns the string "<empty>"
    """
    method_name = "describe"
    return exec_nsdchat([module_name, backupplan_name, method_name],
                        p5_connection)


@onereturnvalue
def disabled(backupplan_name, p5_connection=None):
    """
    Syntax: BackupPlan <name> disabled
    Description: Queries the Disabled status
    Return Values:
    -On Success:    the string "1" (the plan is disabled) or "0" (not disabled)
    """
    method_name = "disabled"
    return exec_nsdchat([module_name, backupplan_name, method_name],
                        p5_connection)


@onereturnvalue
def enabled(backupplan_name, p5_connection=None):
    """
    Syntax: BackupPlan <name> enabled
    Description: Queries the Enabled status
    Return Values:
    -On Success:    the string "1" (the plan is enabled) or "0" (not enabled)
    """
    method_name = "enabled"
    return exec_nsdchat([module_name, backupplan_name, method_name],
                        p5_connection)


@onereturnvalue
def cancel(backupplan_name, p5_connection=None):
    """
    Syntax: BackupPlan <name> cancel
    Description: Cancels execution of the plan <name>. Only running plans can
    be canceled. Plans scheduled but not running can be only stopped (see the
    stop method)
    Return Values:
    -On Success:    the string "1" (the plan was successfully canceled)
                    the string "0" (the plan was not canceled or running)
    """
    method_name = "cancel"
    return exec_nsdchat([module_name, backupplan_name, method_name],
                        p5_connection)


@onereturnvalue
def disable(backupplan_name, p5_connection=None):
    """
    Syntax: BackupPlan <name> disable
    Description: Sets the plan to Disabled
    Return Values:
    -On Success:    the string "0"
    """
    method_name = "disable"
    return exec_nsdchat([module_name, backupplan_name, method_name],
                        p5_connection)


@onereturnvalue
def enable(backupplan_name, p5_connection=None):
    """
    Syntax: BackupPlan <name> enable
    Description: Sets the plan to Enabled
    Return Values:
    -On Success:    the string "1"
    """
    method_name = "enable"
    return exec_nsdchat([module_name, backupplan_name, method_name],
                        p5_connection)


@onereturnvalue
def submit(backupplan_name, now=True, p5_connection=None, as_object=False):
    """
    Syntax: BackupPlan <name> submit [<now>]
    Description: Submits the backup plan for execution. You can optionally
    override plan execution times by using the verbatim string now or the
    integer value zero for the <now> argument.
    The returned job ID can be used to query the status of the job by using the
    Job resource. Please see the Job resource description for more details.
    Note: In order to run a backup plan, a backup event must be selected. The
    start method implicitly selects the next planned backup event to start the
    backup plan.
    Return Values:
    -On Success:    the backup job ID
    """
    method_name = "submit"
    now_option = ""
    if now is True:
        now_option = "now"
    result = exec_nsdchat([module_name, backupplan_name, method_name,
                           now_option], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def stop(backupplan_name, p5_connection=None):
    """
    Syntax: BackupPlan <name> stop
    Description: Removes the plan <name> from the scheduler
    Return Values:
    -On Success:    the string "1" (the plan was successfully removed)
                    the string "0" (the plan was not removed or is running)
    """
    method_name = "stop"
    return exec_nsdchat([module_name, backupplan_name, method_name],
                        p5_connection)


class BackupPlan(P5Resource):
    def __init__(self, backupplan_name, p5_connection=None):
        super().__init__(backupplan_name, p5_connection)

    def names(as_objects=True, p5_connection=None):
        """
        Syntax: BackupPlan names
        Description: Returns a list of names of all the BackupPlan resources
        Return Values:
        -On Success:    a list of names. If no backup plans have been
                        configured, the command returns the string
                        "<empty>"
        """
        method_name = "names"
        if not as_object:
            return result
        else:
            return resourcelist(result, BackupPlan, p5_connection)

    @onereturnvalue
    def describe(self):
        """
        Syntax: BackupPlan <name> describe
        Description: Returns a human-readable description for the <name> plan.
        The <name> is one of the elements returned by the names method. If the
        element does not have a description assigned, the command returns the
        string "<empty>".
        Return Values:
        -On Success:    the resource description. If no description has been
                        set the command returns the string "<empty>"
        """
        method_name = "describe"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disabled(self):
        """
        Syntax: BackupPlan <name> disabled
        Description: Queries the Disabled status
        Return Values:
        -On Success:    the string "1" (the plan is disabled) or "0" (not
        disabled)
        """
        method_name = "disabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enabled(self):
        """
        Syntax: BackupPlan <name> enabled
        Description: Queries the Enabled status
        Return Values:
        -On Success:    the string "1" (the plan is enabled) or "0" (not
        enabled)
        """
        method_name = "enabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def cancel(self):
        """
        Syntax: BackupPlan <name> cancel
        Description: Cancels execution of the plan <name>. Only running plans
        can be canceled. Plans scheduled but not running can be only stopped
        (see the stop method)
        Return Values:
        -On Success:    the string "1" (the plan was successfully canceled)
                        the string "0" (the plan was not canceled or running)
        """
        method_name = "cancel"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disable(self):
        """
        Syntax: BackupPlan <name> disable
        Description: Sets the plan to Disabled
        Return Values:
        -On Success:    the string "0"
        """
        method_name = "disable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enable(self):
        """
        Syntax: BackupPlan <name> enable
        Description: Sets the plan to Enabled
        Return Values:
        -On Success:    the string "1"
        """
        method_name = "enable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def submit(self, now=True, as_object=True):
        """
        Syntax: BackupPlan <name> submit [<now>]
        Description: Submits the backup plan for execution. You can optionally
        override plan execution times by using the verbatim string now or the
        integer value zero for the <now> argument.
        The returned job ID can be used to query the status of the job by using
        the Job resource. Please see the Job resource description for more
        details.
        Note: In order to run a backup plan, a backup event must be selected.
        The start method implicitly selects the next planned backup event to
        start the backup plan.
        Return Values:
        -On Success:    the backup job ID
        """
        method_name = "submit"
        now_option = ""
        if now is True:
            now_option = "now"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, now_option])
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, self.p5_connection)

    @onereturnvalue
    def stop(self):
        """
        Syntax: BackupPlan <name> stop
        Description: Removes the plan <name> from the scheduler
        Return Values:
        -On Success:    the string "1" (the plan was successfully removed)
                        the string "0" (the plan was not removed or is running)
        """
        method_name = "stop"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def __repr__(self):
        return ": ".join([__class__.__name__, self.name])
