# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
ArchivePlan
Manages P5 archive plan(s) and their parameters. Archive plans are used to
group various parameters of the archive operation, like the selected index
database, the pool of media, a time schedule and various other details. The P5
administrator defines archive plans according to the custom site policies. A
user who wishes to archive files must select one of the predefined archive
plans. In the current version of the CLI, you only have limited write access to
archive plans. You can modify some configuration details of existing plans and
you can create new archive plans. If you need full control of ArchivePlan
resources, please use the P5 Web GUI.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.client import Client
from awp5.api.pool import Pool
from awp5.api.job import Job

module_name = "ArchivePlan"


def names(as_object=False, p5_connection=None):
    """
    Syntax: ArchivePlan names
    Description: Returns the list of names of all configured archive plans
    Return Values:
    -On Success:    the list of plan names. If no plans have been
                    configured,  the command returns the string
                    "<empty>"
    """
    method_name = "names"
    str_list = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return str_list
    else:
        return resourcelist(str_list, ArchivePlan, p5_connection)


@onereturnvalue
def describe(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> describe
    Description: Returns a human-readable description of the archive plan
    <name>.
    Return Values:
    -On Success:    the plan description. If no description has been set
                    the command returns the string "<empty>"
    """
    method_name = "describe"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def enabled(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> enabled
    Description: Queries the plan Enabled status
    Return Values:
    -On Success:    the string "1" (plan is enabled) or "0" (not enabled)
    """
    method_name = "enabled"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def disabled(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> disabled
    Description: Queries the plan Disabled status
    Return Values:
    -On Success:    the string "1" (the plan is disabled) or "0" (not disabled)
    """
    method_name = "disabled"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def incrlevel(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> incrlevel
    Description: Queries the plan incremental status
    Return Values:
    -On Success:    the string "1" (plan is incremental)
                    or "0" (plan runs full)
    """
    method_name = "incrlevel"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def autostart(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> autostart
    Description: Returns the autostart setting for the Archive plan <name>. If
    the Archive plan is set to autostart, the returned value is "1", otherwise
    it is ""0".
    Return Values:
    -On Success:    the string "1" (plan is set to autostart)
                    the string "0" (plan is not set to autostart)
    """
    method_name = "autostart"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def create(description, as_object=False, p5_connection=None):
    """
    Syntax: ArchivePlan create <description>
    Description: Creates a new archive plan with the given <description>. If an
    archive plan with the same <description> already exists, an error is
    thrown. The newly created plan might be further configured for operation by
    using the database, pool and/or copypool methods described below.
    If not further configured, the newly generated plan will per-default use
    the Default-Archive pool and the Default-Archive database.
    Return Values:
    -On Success:    the name of the newly created plan
    """
    method_name = "create"
    result = exec_nsdchat([module_name, method_name, description],
                          p5_connection)
    if as_object:
        result = resourcelist(result, ArchivePlan, p5_connection)
    return result


@onereturnvalue
def cancel(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> cancel
    Description: Cancels the execution of plan <name>. Only running plans can
    be canceled. Plans scheduled but not running can be stopped only (see the
    stop method)
    Return Values:
    -On Success:    the string "1" (the plan was successfully canceled)
                    the string "0" (plan was not canceled or is not running)
    """
    method_name = "cancel"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def database(archiveplan_name, value="", p5_connection=None):
    """
    Syntax: ArchivePlan <name> database [<value>]
    Description: Returns or sets the name of the index database resource
    associated with the archive plan <name>
    If the optional <value> argument is not given, the name of the currently
    configured database will be returned.
    If the optional <value> argument is given, it will be taken as the name of
    an existing archive index database, and the plan <name> will be configured
    to use the given database. If the referenced database is not configured or
    disabled, an error will be thrown.
    Also, if the given database is not an archive index, an error will be
    thrown. You can use the ArchiveIndex resource commands to inspect and/or
    create archive index databases.
    Note that ArchivePlan requires that a database is set. Otherwise, the
    archive job for this plan will fail.
    Return Values:
    -On Success:    the name of the archive index database. If none has
                    been set, the command returns the string  "<empty>"
    """
    method_name = "database"
    return exec_nsdchat([module_name, archiveplan_name, method_name, value],
                        p5_connection)


@onereturnvalue
def deletefiles(archiveplan_name, value="", p5_connection=None):
    """
    Syntax: ArchivePlan <name> deletefiles [<value>]
    Description: Returns or sets the option to delete files after successfully
    completing the archive job.
    If optional <value> argument is omitted, returns the current setting.
    If <value> is given (as "true", "yes" or "1"), enables this option. To also
    delete the folder structure, use the deleteall command.
    Return Values:
    -On Success:    the string "1" (the plan is set to delete files)
                    the string "0" (the plan is set not to delete files)
    """
    method_name = "deletefiles"
    return exec_nsdchat([module_name, archiveplan_name, method_name, value],
                        p5_connection)


@onereturnvalue
def deleteall(archiveplan_name, value="", p5_connection=None):
    """
    Syntax: ArchivePlan <name> deleteall [<value>]
    Description: Returns or sets the option to delete both files and folders
    after successfully completing archive plan job.
    If optional <value> argument is omitted, returns the current setting.
    If <value> is given (as "true", "yes" or "1"), enables this option.
    Return Values:
    -On Success:    the string "1" (the plan is set to delete files and
                    folders)
                    the string "0" (the plan is set to not delete anything)
    """
    method_name = "deleteall"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def disable(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> disable
    Description: Sets the plan to the Disabled state
    Return Values:
    -On Success:    the string "0"
    """
    method_name = "disable"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def enable(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> enable
    Description: Sets the plan to the "Enabled" state
    Return Values:
    -On Success:    the string "1"
    """
    method_name = "enable"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def pool(archiveplan_name, value="", as_object=False, p5_connection=None):
    """
    Syntax: ArchivePlan <name> pool [<value>]
    Description: Returns the name of the media pool associated with the archive
    plan <name>. If the optional <value> argument is not given, the name of the
    currently configured pool will be returned.
    If the optional <value> argument is given it will be taken as the name of
    an existing media pool, and the plan <name> will be configured to use the
    given pool. If the referenced media pool is not configured, an error will
    be thrown. Also, if the referenced media pool is not set up for archive
    operation, an error will be thrown. You can use the Pool resource commands
    to inspect and/or create media pools.
    Note that ArchivePlan must have the media pool set. Otherwise, the archive
    job configured to use this plan will fail.
    Return Values:
    -On Success:    the name of the primary media pool. If not configured,
                    it returns the string "<empty>"
    """
    method_name = "pool"
    result = exec_nsdchat([module_name, archiveplan_name, method_name, value],
                          p5_connection)
    if as_object:
        result = resourcelist(result, Pool, p5_connection)
    return result


@onereturnvalue
def run(archiveplan_name, delete=False, as_object=False, p5_connection=None):
    """
    Syntax: ArchivePlan <name> run [-delete 1]
    Description: Runs the archive plan immediately with an optional delete pass
    on the target directory/ies.
    Note: use the returned job ID to query the status of the job by using the
    Job resource. Please see the Job resource description for more details.
    Return Values:
    -On Success:    the archive job ID.
    """
    delete_option = ""
    if delete is True:
        delete_option = "-delete -1"
    method_name = "run"
    result = exec_nsdchat([module_name, archiveplan_name, method_name,
                           delete_option], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def stop(archiveplan_name, p5_connection=None):
    """
    Syntax: ArchivePlan <name> stop
    Description: Removes the plan <name> from the scheduler
    Return Values:
    -On Success:    the string "1" (the plan was successfully removed)
                    the string "0" (the plan was not removed or is running)
    """
    method_name = "stop"
    return exec_nsdchat([module_name, archiveplan_name, method_name],
                        p5_connection)


@onereturnvalue
def submit(archiveplan_name, now=True, as_object=False, p5_connection=None):
    """
    Syntax: ArchivePlan <name> submit [<now>]
    Description: Submits the archive plan for execution. You can optionally
    override plan execution times by using the verbatim string now or the
    integer value zero for the <now> argument.
    The returned job ID can be used to query the status of the job by using the
    Job resource. Please see the Job resource description for more details.
    Note: In order to run an Archive plan, an archive event must be selected.
    The start method thus selects the next planned archive event to start the
    archive plan.
    Return Values:
    -On Success:    the archive job ID
    """
    method_name = "submit"
    now_option = ""
    if now is True:
        now_option = "now"
    result = exec_nsdchat([module_name, archiveplan_name, method_name,
                           now_option], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def verify(archiveplan_name, client, job, p5_connection=None):
    """
    Syntax: ArchivePlan <name> verify <client> <job>
    Description: Re-runs the verify, clip generation and deletion (the post-
    archive tasks) of files located on the <client> computer and archived with
    the <job> ID.
    Return Values:
    -On Success:    the verify job ID. Use this job ID to query the status of
                    the job by using Job resource. Please see the Job
                    resource description for more details
    """
    method_name = "verify"
    return exec_nsdchat([module_name, archiveplan_name, method_name, client,
                        job], p5_connection)


class ArchivePlan(P5Resource):
    def __init__(self, archiveplan_name, p5_connection=None):
        super().__init__(archiveplan_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: ArchivePlan names
        Description: Returns the list of names of all configured archive plans
        Return Values:
        -On Success:    the list of plan names. If no plans have been
                        configured,  the command returns the string
                        "<empty>"
        """
        method_name = "names"
        str_list = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return str_list
        else:
            return resourcelist(str_list, ArchivePlan, p5_connection)

    @onereturnvalue
    def describe(self):
        """
        Syntax: ArchivePlan <name> describe
        Description: Returns a human-readable description of the archive plan
        <name>.
        Return Values:
        -On Success:    the plan description. If no description has been set
                        the command returns the string "<empty>"
        """
        method_name = "describe"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enabled(self):
        """
        Syntax: ArchivePlan <name> enabled
        Description: Queries the plan Enabled status
        Return Values:
        -On Success:    the string "1" (plan is enabled) or "0" (not enabled)
        """
        method_name = "enabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disabled(self):
        """
        Syntax: ArchivePlan <name> disabled
        Description: Queries the plan Disabled status
        Return Values:
        -On Success:    the string "1" (the plan is disabled) or "0" (not
        disabled)
        """
        method_name = "disabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def incrlevel(self):
        """
        Syntax: ArchivePlan <name> incrlevel
        Description: Queries the plan incremental status
        Return Values:
        -On Success:    the string "1" (plan is incremental)
                        or "0" (plan runs full)
        """
        method_name = "incrlevel"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def autostart(self):
        """
        Syntax: ArchivePlan <name> autostart
        Description: Returns the autostart setting for the Archive plan <name>.
        If the Archive plan is set to autostart, the returned value is "1",
        otherwise it is "0".
        Return Values:
        -On Success:    the string "1" (plan is set to autostart)
                        the string "0" (plan is not set to autostart)
        """
        method_name = "autostart"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def create(description, as_object=True, p5_connection=None):
        """
        Syntax: ArchivePlan create <description>
        Description: Creates a new archive plan with the given <description>.
        If an archive plan with the same <description> already exists, an error
        is thrown.
        The newly created plan might be further configured for operation by
        using the database, pool and/or copypool methods described below.
        If not further configured, the newly generated plan will per-default
        use the Default-Archive pool and the Default-Archive database.
        Return Values:
        -On Success:    the name of the newly created plan
        """
        method_name = "create"
        result = exec_nsdchat([module_name, method_name, description],
                              p5_connection)
        if as_object:
            result = resourcelist(result, ArchivePlan, p5_connection)
        return result

    @onereturnvalue
    def cancel(self):
        """
        Syntax: ArchivePlan <name> cancel
        Description: Cancels the execution of plan <name>. Only running plans
        can be canceled. Plans scheduled but not running can be stopped only
        (see the stop method)
        Return Values:
        -On Success:    the string "1" (the plan was successfully canceled)
                        the string "0" (plan was not canceled or is not
                        running)
        """
        method_name = "cancel"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def database(self, value=""):
        """
        Syntax: ArchivePlan <name> database [<value>]
        Description: Returns or sets the name of the index database resource
        associated with the archive plan <name>
        If the optional <value> argument is not given, the name of the
        currently configured database will be returned.
        If the optional <value> argument is given, it will be taken as the name
        of an existing archive index database, and the plan <name> will be
        configured to use the given database. If the referenced database is not
        configured or disabled, an error will be thrown.
        Also, if the given database is not an archive index, an error will be
        thrown. You can use the ArchiveIndex resource commands to inspect
        and/or create archive index databases.
        Note that ArchivePlan requires that a database is set. Otherwise, the
        archive job for this plan will fail.
        Return Values:
        -On Success:    the name of the archive index database. If none has
                        been set, the command returns the string  "<empty>"
        """
        method_name = "database"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, value])

    @onereturnvalue
    def deletefiles(self, value=""):
        """
        Syntax: ArchivePlan <name> deletefiles [<value>]
        Description: Returns or sets the option to delete files after
        successfully completing the archive job.
        If optional <value> argument is omitted, returns the current setting.
        If <value> is given (as "true", "yes" or "1"), enables this option. To
        also delete the folder structure, use the deleteall command.
        Return Values:
        -On Success:    the string "1" (the plan is set to delete files)
                        the string "0" (the plan is set not to delete files)
        """
        method_name = "deletefiles"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, value])

    @onereturnvalue
    def deleteall(self, value=""):
        """
        Syntax: ArchivePlan <name> deleteall [<value>]
        Description: Returns or sets the option to delete both files and
        folders after successfully completing archive plan job.
        If optional <value> argument is omitted, returns the current setting.
        If <value> is given (as "true", "yes" or "1"), enables this option.
        Return Values:
        -On Success:    the string "1" (the plan is set to delete files and
                        folders)
                        the string "0" (the plan is set to not delete anything)
        """
        method_name = "deleteall"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disable(self):
        """
        Syntax: ArchivePlan <name> disable
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
        Syntax: ArchivePlan <name> enable
        Description: Sets the plan to the "Enabled" state
        Return Values:
        -On Success:    the string "1"
        """
        method_name = "enable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def pool(self, value="", as_object=False):
        """
        Syntax: ArchivePlan <name> pool [<value>]
        Description: Returns the name of the media pool associated with the
        archive plan <name>. If the optional <value> argument is not given, the
        name of the currently configured pool will be returned.
        If the optional <value> argument is given it will be taken as the name
        of an existing media pool, and the plan <name> will be configured to
        use the given pool. If the referenced media pool is not configured, an
        error will be thrown. Also, if the referenced media pool is not set up
        for archive operation, an error will be thrown. You can use the Pool
        resource commands to inspect and/or create media pools.
        Note that ArchivePlan must have the media pool set. Otherwise, the
        archive job configured to use this plan will fail.
        Return Values:
        -On Success:    the name of the primary media pool. If not configured,
                        it returns the string "<empty>"
        """
        method_name = "pool"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, value])
        if as_object:
            result = resourcelist(result, Pool, self.p5_connection)
        return result

    @onereturnvalue
    def run(self, delete=False, as_object=True):
        """
        Syntax: ArchivePlan <name> run [-delete 1]
        Description: Runs the archive plan immediately with an optional delete
        pass on the target directory/ies.
        Note: use the returned job ID to query the status of the job by using
        the Job resource. Please see the Job resource description for more
        details.
        Return Values:
        -On Success:    the archive job ID.
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
    def stop(self):
        """
        Syntax: ArchivePlan <name> stop
        Description: Removes the plan <name> from the scheduler
        Return Values:
        -On Success:    the string "1" (the plan was successfully removed)
                        the string "0" (the plan was not removed or is running)
        """
        method_name = "stop"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def submit(self, now=True, as_object=True):
        """
        Syntax: ArchivePlan <name> submit [<now>]
        Description: Submits the archive plan for execution. You can optionally
        override plan execution times by using the verbatim string now or the
        integer value zero for the <now> argument.
        The returned job ID can be used to query the status of the job by using
        the Job resource. Please see the Job resource description for more
        details.
        Note: In order to run an Archive plan, an archive event must be
        selected. The start method thus selects the next planned archive event
        to start the archive plan.
        Return Values:
        -On Success:    the archive job ID
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
    def verify(self, client, job):
        """
        Syntax: ArchivePlan <name> verify <client> <job>
        Description: Re-runs the verify, clip generation and deletion (the
        post-archive tasks) of files located on the <client> computer and
        archived with the <job> ID.
        Return Values:
        -On Success:    the verify job ID. Use this job ID to query the status
                        of the job by using Job resource. Please see the Job
                        resource description for more details
        """
        method_name = "verify"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, client, job])

    def __repr__(self):
        return ": ".join([__class__.__name__, self.name])
