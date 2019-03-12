# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
The sync selection is used to prepare one or more directories for the sync
operation. You can use the resource methods to populate the selection (i.e. add
directories) and then submit the entire selection for immediate or scheduled
execution.
The sync selection is a temporary resource. It does not survive system crashes
and server shutdowns, nor does it need to be explicitly destroyed by the
caller. It goes out of scope by invoking the submit method, which effectively
passes the control to the Job manager. The owner of the sync selection resource
is thus the P5 system, so the caller does not need (nor should) perform any
other task with the same resource.
Usage:
To use the SyncSelection resource, you must first use the create method to
create a new instance. Having created an instance, use the adddirectory method
to fill-in the selection with directories to synchronize. Finally, submit the
selection for immediate or scheduled execution. After submission, the resource
goes out of scope and should not be used any more.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.job import Job
from awp5.api.syncplan import SyncPlan

module_name = "SyncSelection"


@onereturnvalue
def create(syncplan, as_object=False, p5_connection=None):
    """
    Syntax: SyncSelection create <plan>
    Description: Creates new temporary sync selection resource. The resource
    will be automatically deleted after the associated sync job has been
    submitted.
    The <plan> must be one of the registered synchronize plans. You can get the
    list of synchronize plans with the SyncPlan names CLI command
    Return Values:
    -On Success:    the name of the new resource. Use this name to
                    address the resource in all the other methods
    """
    method_name = "create"
    result = exec_nsdchat([module_name, method_name, syncplan], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, SyncSelection, p5_connection)


@onereturnvalue
def adddirectory(syncselection_name, path, p5_connection=None):
    """
    Syntax: SyncSelection <name> adddirectory <path>
    Description: Adds one new directory <path> to the sync selection <name>. It
    expects the absolute path to the directory to be synced. The directory must
    be located on the source client and under the source path as given in the
    sync plan used to create the sync selection object.
    Return Values:
    -On Success:    the directory path
    """
    method_name = "adddirectory"
    return exec_nsdchat([module_name, syncselection_name, method_name, path],
                        p5_connection)


@onereturnvalue
def addrecursive(syncselection_name, path, p5_connection=None):
    """
    Syntax: SyncSelection <name> addrecursive <path>
    Description: Adds a single new directory <path> to the sync selection
    <name> and recurses into the subfolders of that directory. It expects the
    absolute path to the directory to be synced. The directory must be located
    on the source client and under the source path as given in the sync plan
    used to create the sync selection object.
    Return Values:
    -On Success:    the directory path repeated
    """
    method_name = "addrecursive"
    return exec_nsdchat([module_name, syncselection_name, method_name, path],
                        p5_connection)


@onereturnvalue
def destroy(syncselection_name, p5_connection=None):
    """
    Syntax: SyncSelection <name> destroy
    Description: Explicitly destroys the sync selection. The <name> should not
    be used in any SyncSelection commands afterwards.
    Return Values:
    -On Success:    the string "0" (destroyed)
                    the string "1" (not destroyed)
    """
    method_name = "destroy"
    return exec_nsdchat([module_name, syncselection_name, method_name],
                        p5_connection)


@onereturnvalue
def onjobactivation(syncselection_name, command=None, p5_connection=None):
    """
    Syntax: SyncSelection <name> onjobactivation [<command>]
    Description: Registers the <command> to be executed just before the job is
    started by the submit method. The command itself can be any valid OS
    command plus variable number of arguments.
    The very first argument of the command (the program itself) can be
    prepended with the name of the P5 client where the command is to be
    executed on. If omitted, the command will be executed on the client which
    the SyncSelecttion object is created for.

    Examples:
    SyncSelection SyncSelection.0 onjobactivation "mickey:/var/myscript arg"
    will execute /var//myscript on the client "mickey" regardless what client
    the SyncSelection is created for. The program will be passed one argument:
    arg.
    SyncSelection SyncSelection.0 onjobactivation "/var/scripts/myscript"
    will execute /var/scripts/myscript on the client the SyncSelection is
    created for.
    SyncSelection SyncSelection.0 onjobactivation
                                             "localhost:/var/scripts/myscript"
    will execute /var/scripts/myscript on the P5 server.
    Return Values:
    -On Success:    the command string
    """
    method_name = "onjobactivation"
    return exec_nsdchat([module_name, syncselection_name, method_name,
                         command], p5_connection)


@onereturnvalue
def onjobcompletion(syncselection_name, command=None, p5_connection=None):
    """
    Syntax: SyncSelection <name> onjobcompletion [<value>]
    Description: Registers the <command> to be executed immediately after the
    job created by the submit method is completed. See onjobactivation for
    further information.
    Return Values:
    -On Success:    the command string
    """
    method_name = "onjobcompletion"
    return exec_nsdchat([module_name, syncselection_name, method_name,
                         command], p5_connection)


@onereturnvalue
def submit(syncselection_name, now=True, as_object=False, p5_connection=None):
    """
    Syntax: SyncSelection <name> submit [<now>]
    Description: Submits the sync selection for execution. You can optionally
    override plan execution times by giving the <now> as one of the strings
    "1", "t", "true", "True", "y", "yes", or "Yes".
    This command implicitly destroys the SyncSelection object for the user and
    transfers the ownership of the internal underlying object to the job
    scheduler. You should not attempt to use the <name> afterwards.
    Return Values:
    -On Success:    the sync job ID. Use this job ID to query the
                    status of the job by using Job resource.
                    Please see the Job resource description for details.
    """
    method_name = "submit"
    now_option = ""
    if now is True:
        now_option = "1"
    result = exec_nsdchat([module_name, syncselection_name, method_name,
                           now_option], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


class SyncSelection(P5Resource):
    def __init__(self, syncselection_name, p5_connection=None):
        super().__init__(syncselection_name, p5_connection)

    @onereturnvalue
    def create(syncplan=None, as_object=True, p5_connection=None):
        """
        Syntax: SyncSelection create <plan>
        Description: Creates new temporary sync selection resource. The
        resource will be automatically deleted after the associated sync job
        has been submitted.
        The <plan> must be one of the registered synchronize plans. You can get
        the list of synchronize plans with the SyncPlan names CLI command
        Return Values:
        -On Success:    the name of the new resource. Use this name to
                        address the resource in all the other methods
        """
        method_name = "create"
        result = exec_nsdchat([module_name, method_name, syncplan],
                              p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, SyncSelection, p5_connection)

    @onereturnvalue
    def adddirectory(self, path):
        """
        Syntax: SyncSelection <name> adddirectory <path>
        Description: Adds one new directory <path> to the sync selection
        <name>. It expects the absolute path to the directory to be synced. The
        directory must be located on the source client and under the source
        path as given in the sync plan used to create the sync selection
        object.
        Return Values:
        -On Success:    the directory path
        """
        method_name = "adddirectory"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, path])

    @onereturnvalue
    def addrecursive(self, path):
        """
        Syntax: SyncSelection <name> addrecursive <path>
        Description: Adds a single new directory <path> to the sync selection
        <name> and recurses into the subfolders of that directory. It expects
        the absolute path to the directory to be synced. The directory must be
        located on the source client and under the source path as given in the
        sync plan used to create the sync selection object.
        Return Values:
        -On Success:    the directory path repeated
        """
        method_name = "addrecursive"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, path])

    @onereturnvalue
    def destroy(self):
        """
        Syntax: SyncSelection <name> destroy
        Description: Explicitly destroys the sync selection. The <name> should
        not be used in any SyncSelection commands afterwards.
        Return Values:
        -On Success:    the string "0" (destroyed)
                        the string "1" (not destroyed)
        """
        method_name = "destroy"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def onjobactivation(self, command=None):
        """
        Syntax: SyncSelection <name> onjobactivation [<command>]
        Description: Registers the <command> to be executed just before the job
        is started by the submit method. The command itself can be any valid OS
        command plus variable number of arguments.
        The very first argument of the command (the program itself) can be
        prepended with the name of the P5 client where the command is to be
        executed on. If omitted, the command will be executed on the client
        which the SyncSelecttion object is created for.

        Examples:
        SyncSelection SyncSelection.0 onjobactivation
                                                    "mickey:/var/myscript arg"
        will execute /var//myscript on the client "mickey" regardless what
        client the SyncSelection is created for. The program will be passed one
        argument: arg.
        SyncSelection SyncSelection.0 onjobactivation "/var/scripts/myscript"
        will execute /var/scripts/myscript on the client the SyncSelection is
        created for.
        SyncSelection SyncSelection.0 onjobactivation
                                            "localhost:/var/scripts/myscript"
        will execute /var/scripts/myscript on the P5 server.
        Return Values:
        -On Success:    the command string
        """
        method_name = "onjobactivation"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, command])

    @onereturnvalue
    def onjobcompletion(self, command=None):
        """
        Syntax: SyncSelection <name> onjobcompletion [<value>]
        Description: Registers the <command> to be executed immediately after
        the job created by the submit method is completed. See onjobactivation
        for further information.
        Return Values:
        -On Success:    the command string
        """
        method_name = "onjobcompletion"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, command])

    @onereturnvalue
    def submit(self, as_object=True, now=True):
        """
        Syntax: SyncSelection <name> submit [<now>]
        Description: Submits the sync selection for execution. You can
        optionally override plan execution times by giving the <now> as one of
        the strings "1", "t", "true", "True", "y", "yes", or "Yes".
        This command implicitly destroys the SyncSelection object for the user
        and transfers the ownership of the internal underlying object to the
        job scheduler. You should not attempt to use the <name> afterwards.
        Return Values:
        -On Success:    the sync job ID. Use this job ID to query the
                        status of the job by using Job resource.
                        Please see the Job resource description for details.
        """
        method_name = "submit"
        now_option = ""
        if now is True:
            now_option = "1"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, now_option])
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, self.p5_connection)

    def __repr__(self):
        return ": ".join([module_name, self.name])
