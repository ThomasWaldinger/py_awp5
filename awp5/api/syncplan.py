# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
SyncPlan
Queries P5 synchronize plans and their parameters. Sync plans are used to group
various parameters of the synchronize operation, like time schedules and
various other details. P5 administrator defines sync plans according to the
custom site policies.
In the current version of the CLI, you only have read access to sync plans. You
can't modify any of the existing plans nor can you create new or delete
existing plans. SyncPlan resources are configured and maintained with P5 Web
GUI by the system administrator.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.client import Client
from awp5.api.job import Job

module_name = "SyncPlan"


def names(as_object=False, p5_connection=None):
    """
    Syntax: SyncPlan names
    Description: Returns a list of names of all sync plans
    Return Values:
    -On Success:    a list of names. If no sync plans have been configured
                    the command returns the string "<empty>"
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, SyncPlan, p5_connection)


@onereturnvalue
def describe(syncplan_name, p5_connection=None):
    """
    Syntax: SyncPlan <name> describe
    Description: Returns a human-readable description of the <name> plan.
    The <name> is one of the elements returned by the names method. If the
    element has no description assigned, the command returns string "<empty>".
    Return Values:
    -On Success:    the resource description. If no description has been
                    set, the command returns the string "<empty>"
    """
    method_name = "describe"
    return exec_nsdchat([module_name, syncplan_name, method_name],
                        p5_connection)


@onereturnvalue
def disabled(syncplan_name, p5_connection=None):
    """
    Syntax: SyncPlan <name> disabled
    Description: Queries the plan Disabled status
    Return Values:
    -On Success:  the  string "1" (the plan is disabled) or "0" (not disabled)
    """
    method_name = "disabled"
    return exec_nsdchat([module_name, syncplan_name, method_name],
                        p5_connection)


@onereturnvalue
def enabled(syncplan_name, p5_connection=None):
    """
    Syntax: SyncPlan <name> enabled
    Description: Queries the plan Enabled status
    Return Values:
    -On Success:    the string "1" (the plan is enabled) or "0" (not enabled)
    """
    method_name = "enabled"
    return exec_nsdchat([module_name, syncplan_name, method_name],
                        p5_connection)


@onereturnvalue
def sourcehost(syncplan_name, as_object=False, p5_connection=None):
    """
    Syntax: SyncPlan <name> sourcehost
    Description: Returns the name of the client where the source data is
    located.
    Return Values:
    -On Success:    the name of the client
    """
    method_name = "sourcehost"
    result = exec_nsdchat([module_name, syncplan_name, method_name],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Client, p5_connection)


@onereturnvalue
def sourcepath(syncplan_name, newpath=None, p5_connection=None):
    """
    Syntax: SyncPlan <name> sourcepath [newpath]
    Description: If no optional argment newpath specified, returns the path of
    the source directory on the client where the data is located. Otherwise
    sets the given new path.
    Return Values:
    -On Success:    the path to the directory
    """
    method_name = "sourcepath"
    return exec_nsdchat([module_name, syncplan_name, method_name,
                        newpath], p5_connection)


@onereturnvalue
def targethost(syncplan_name, as_object=False, p5_connection=None):
    """
    Syntax: SyncPlan <name> targethost
    Description: Returns the name of the client where the data should be synced
    to
    Return Values:
    -On Success:    the name of the client
    """
    method_name = "targethost"
    result = exec_nsdchat([module_name, syncplan_name, method_name],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Client, p5_connection)


@onereturnvalue
def targetpath(syncplan_name, newpath=None, p5_connection=None):
    """
    Syntax: SyncPlan <name> targetpath [newpath]
    Description: If no optional argument newpath specified, returns the path of
    the target directory on the client where the data is to be synced.
    Otherwise sets the given new path.
    Return Values:
    -On Success:    the path to the directory
    """
    method_name = "targetpath"
    return exec_nsdchat([module_name, syncplan_name, method_name,
                        newpath], p5_connection)


@onereturnvalue
def cancel(syncplan_name, p5_connection=None):
    """
    Syntax: SyncPlan <name> cancel
    Description: Cancels the plan <name> execution. Only running plans can be
    canceled. Plans scheduled but not running can be only stopped (see the stop
    method)
    Return Values:
    -On Success:    the string "1" (the plan was successfully canceled)
                    the string "0" (the plan was not canceled or running)
    """
    method_name = "cancel"
    return exec_nsdchat([module_name, syncplan_name, method_name],
                        p5_connection)


@onereturnvalue
def disable(syncplan_name, p5_connection=None):
    """
    Syntax: SyncPlan <name> disable
    Description: Sets the plan to the Disabled state
    Return Values:
    -On Success:    the string "0"
    """
    method_name = "disable"
    return exec_nsdchat([module_name, syncplan_name, method_name],
                        p5_connection)


@onereturnvalue
def enable(syncplan_name, p5_connection=None):
    """
    Syntax: SyncPlan <name> enable
    Description: Sets the plan to the Enabled state
    Return Values:
    -On Success:    the string "1"
    """
    method_name = "enable"
    return exec_nsdchat([module_name, syncplan_name, method_name],
                        p5_connection)


@onereturnvalue
def run(syncplan_name, delete=False, as_object=False, p5_connection=None):
    """
    Syntax: SyncPlan <name> run [delete 1]
    Description: Runs the sync plan immediately with optional delete pass on
    the target directory.
    Note: In order to run a Synchronize plan, a Synchronize event must be
    selected. The start method implicitly selects the next planned event to
    start the backup plan.
    Return Values:
    -On Success:    the sync job ID. Use this job ID to query the
                    status of the job by using Job resource.
                    Please see the Job resource description for details.
    """
    delete_option = ""
    if delete is True:
        delete_option = "-delete -1"
    method_name = "run"
    result = exec_nsdchat([module_name, syncplan_name, method_name,
                           delete_option], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def submit(syncplan_name, now=True, as_object=False, p5_connection=None):
    """
    Syntax: SyncPlan <name> submit [<now>]
    Description: Submits the sync plan for execution. You can optionally
    override plan execution times by using the verbatim string now or the
    integer value zero for the <now> argument.
    Plan must be configured for auto-start since CLI just overrides the
    scheduled starting time. This command cannot be used to start a plan which
    is not set to auto-start or which does not have any events configured.
    Return Values:
    -On Success:    the sync job ID. Use this job ID to query the
                    status of the job by using Job resource.
                    Please see the Job Resource description for details.
    """
    method_name = "submit"
    now_option = ""
    if now is True:
        now_option = "now"
    result = exec_nsdchat([module_name, syncplan_name, method_name,
                           now_option], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def stop(syncplan_name, p5_connection=None):
    """
    Syntax: SyncPlan <name> stop
    Description: Removes the plan <name> from the scheduler
    Return Values:
    -On Success:    the string "1" (the plan was successfully removed)
                    the string "0" (the plan was not removed or running)
    """
    method_name = "stop"
    return exec_nsdchat([module_name, syncplan_name, method_name],
                        p5_connection)


class SyncPlan(P5Resource):
    def __init__(self, syncplan_name, p5_connection=None):
        super().__init__(syncplan_name, p5_connection)

    def names(p5_connection=None, as_object=True):
        """
        Syntax: SyncPlan names
        Description: Returns a list of names of all sync plans
        Return Values:
        -On Success:    a list of names. If no sync plans have been configured
                        the command returns the string "<empty>"
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, SyncPlan, p5_connection)

    @onereturnvalue
    def describe(self):
        """
        Syntax: SyncPlan <name> describe
        Description: Returns a human-readable description of the <name> plan.
        The <name> is one of the elements returned by the names method. If the
        element has no description assigned, the command returns string
        "<empty>".
        Return Values:
        -On Success:    the resource description. If no description has been
                        set, the command returns the string "<empty>"
        """
        method_name = "describe"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disabled(self):
        """
        Syntax: SyncPlan <name> disabled
        Description: Queries the plan Disabled status
        Return Values:
        -On Success:    the  string "1" (the plan is disabled) or "0" (not
                        disabled)
        """
        method_name = "disabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enabled(self):
        """
        Syntax: SyncPlan <name> enabled
        Description: Queries the plan Enabled status
        Return Values:
        -On Success:    the string "1" (the plan is enabled) or "0" (not
                        enabled)
        """
        method_name = "enabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def sourcehost(self, as_object=True):
        """
        Syntax: SyncPlan <name> sourcehost
        Description: Returns the name of the client where the source data is
        located.
        Return Values:
        -On Success:    the name of the client
        """
        method_name = "sourcehost"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name])
        if not as_object:
            return result
        else:
            return resourcelist(result, Client, self.p5_connection)

    @onereturnvalue
    def sourcepath(self, newpath=None):
        """
        Syntax: SyncPlan <name> sourcepath [newpath]
        Description: If no optional argment newpath specified, returns the path
        of the source directory on the client where the data is located.
        Otherwise sets the given new path.
        Return Values:
        -On Success:    the path to the directory
        """
        method_name = "sourcepath"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, newpath])

    @onereturnvalue
    def targethost(self, as_object=True):
        """
        Syntax: SyncPlan <name> targethost
        Description: Returns the name of the client where the data should be
        synced to
        Return Values:
        -On Success:    the name of the client
        """
        method_name = "targethost"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name])
        if not as_object:
            return result
        else:
            return resourcelist(result, Client, self.p5_connection)

    @onereturnvalue
    def targetpath(self, newpath=None):
        """
        Syntax: SyncPlan <name> targetpath [newpath]
        Description: If no optional argument newpath specified, returns the
        path of the target directory on the client where the data is to be
        synced. Otherwise sets the given new path.
        Return Values:
        -On Success:    the path to the directory
        """
        method_name = "targetpath"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, newpath])

    @onereturnvalue
    def cancel(self):
        """
        Syntax: SyncPlan <name> cancel
        Description: Cancels the plan <name> execution. Only running plans can
        be canceled. Plans scheduled but not running can be only stopped (see
        the stop method)
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
        Syntax: SyncPlan <name> disable
        Description: Sets the plan to the Disabled state
        Return Values:
        -On Success:    the string "0"
        """
        method_name = "disable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enable(self):
        """
        Syntax: SyncPlan <name> enable
        Description: Sets the plan to the Enabled state
        Return Values:
        -On Success:    the string "1"
        """
        method_name = "enable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def run(self, delete=False, as_object=True):
        """
        Syntax: SyncPlan <name> run [delete 1]
        Description: Runs the sync plan immediately with optional delete pass
        on the target directory.
        Note: In order to run a Synchronize plan, a Synchronize event must be
        selected. The start method implicitly selects the next planned event to
        start the backup plan.
        Return Values:
        -On Success:    the sync job ID. Use this job ID to query the
                        status of the job by using Job resource.
                        Please see the Job resource description for details.
        """
        delete_option = ""
        if delete is True:
            delete_option = "-delete -1"
        method_name = "run"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, delete_option])
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, self.p5_connection)

    @onereturnvalue
    def submit(self, now=True, as_object=True):
        """
        Syntax: SyncPlan <name> submit [<now>]
        Description: Submits the sync plan for execution. You can optionally
        override plan execution times by using the verbatim string now or the
        integer value zero for the <now> argument.
        Plan must be configured for auto-start since CLI just overrides the
        scheduled starting time. This command cannot be used to start a plan
        which is not set to auto-start or which does not have any events
        configured.
        Return Values:
        -On Success:    the sync job ID. Use this job ID to query the
                        status of the job by using Job resource.
                        Please see the Job Resource description for details.
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
        Syntax: SyncPlan <name> stop
        Description: Removes the plan <name> from the scheduler
        Return Values:
        -On Success:    the string "1" (the plan was successfully removed)
                        the string "0" (the plan was not removed or running)
        """
        method_name = "stop"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def __repr__(self):
        return ": ".join([__class__.__name__, self.name])
