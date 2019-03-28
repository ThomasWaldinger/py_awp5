# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
RestoreSelection

The restore selection is used to prepare one or more files for the restore
operation. You must create new restore selection resource for each new restore
session. You can use the resource methods to populate the selection (i.e. add
files) and then submit the entire selection for immediate or scheduled
execution.
The restore selection is a temporary resource. It does not survive system
crashes and server shutdowns, nor it needs to be explicitly destroyed by the
caller. It goes out of scope by invoking the submit method, which effectively
passes the control to the Job manager. The owner of the archive selection
resource is thus the P5 system, so the caller needs not (nor it should) perform
any other task with the same resource.
Usage:
To use the RestoreSelection, you must first use the create method to create new
instance. After the creation, you use the addentry and/or findentry methods to
fill-in the selection with files to restore. Finally, you must submit the
selection for immediate or scheduled execution. After the submission, the
resource goes out of scope and should not be used any more.
"""

from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.archiveplan import ArchivePlan
from awp5.api.job import Job
from awp5.api.volume import Volume

module_name = "RestoreSelection"


@onereturnvalue
def create(client, relocate=None, as_object=False, p5_connection=None):
    """
    Syntax: RestoreSelection create <client> [<relocate>]
    Description: Creates a new temporary restore selection resource. The
    resource will be automatically deleted after the associated archive job has
    been submitted.
    The <client> must be one of the registered client computers on the current
    P5 server. Restored files will be placed on the named client. You can get
    the list of client computers with the Client names CLI command.
    The <relocate> overrides default restore location. If this option is given,
    it must point to a directory on the <client> file system. All files will be
    placed in this directory instead of their original location. The <relocate>
    directory must exist on the client.
    Return Values:
    -On Success:    the name of the new resource. Use this name to
                    address the resource in all other methods.
    """
    method_name = "create"
    result = exec_nsdchat([module_name, method_name, client, relocate],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, RestoreSelection, p5_connection)


@onereturnvalue
def addentry(restoreselection_name, archiveentry, path=None,
             p5_connection=None):
    """
    Syntax: RestoreSelection <name> addentry <archiveentry> [<path>]
    Description: Adds a new entry <archiveentry> to the restore selection
    <name>. The <archiveentry> is a handle to the archived file as returned by
    the ArchiveSelection addentry.
    By providing the optional path argument, it is possible to specify the
    target path of the restored file.
    Return Values:
    -On Success:    the path to the file to be restored
                    Note: the returned path is not translated to match
                    the optional <relocate> argument given at resource
                    creation.
    """
    method_name = "addentry"
    return exec_nsdchat([module_name, restoreselection_name, method_name,
                         archiveentry, path], p5_connection)


@onereturnvalue
def addfrom(restoreselection_name, inputfile,
             p5_connection=None):
    """
    Description: Loads the Restore Selection entries from the external file
    <input file>. The file must be formatted with one entry per line, each
    entry in the format of:
    <archiveentry>[TAB<relocate path>]
    The <archiveentry> is a handle to the archived file as returned by
    ArchiveSelection addentry.
    In case a <relocate path> is given, the archived file or folder is
    restored at the given path. Otherwise the relocate path as given in the
    RestoreSelection is used.
    Return Values:
    -On Success:    The count of entries that will be restored
    """
    method_name = "addfrom"
    return exec_nsdchat([module_name, restoreselection_name, method_name,
                         inputfile], p5_connection)


@onereturnvalue
def describe(restoreselection_name, title=None, p5_connection=None):
    """
    Syntax: RestoreSelection <name> describe [title]
    Description: If a title is given, the title is set as description in the
    job monitor.
    The method returns the current description
    Return Values:
    -On Success:    the description string as used in the job monitor
    """
    method_name = "describe"
    return exec_nsdchat([module_name, restoreselection_name, method_name,
                         title], p5_connection)


@onereturnvalue
def destroy(restoreselection_name, p5_connection=None):
    """
    Syntax: RestoreSelection <name> destroy
    Description: Explicitly destroys the restore selection. The <name> should
    not be used in any RestoreSelection commands afterwards
    Return Values:
    -On Success:    the string "0" (destroyed) or "1" (not destroyed)
    """
    method_name = "destroy"
    return exec_nsdchat([module_name, restoreselection_name, method_name],
                        p5_connection)


@onereturnvalue
def entries(restoreselection_name, p5_connection=None):
    """
    Syntax: RestoreSelection <name> entries
    Description: Returns the number of entries belonging to the restore
    selection <name>.
    Return Values:
    -On Success:    the number of entries
    """
    method_name = "entries"
    return exec_nsdchat([module_name, restoreselection_name, method_name],
                        p5_connection)


@onereturnvalue
def findentry(restoreselection_name, plan, expr, p5_connection=None):
    """
    Syntax: RestoreSelection <name> findentry <plan> {<expr>}
    Description: Fills in the restore selection object by searching the archive
    entries archived with the archive <plan>.
    The <expr> contains the search expression used to locate records. The
    <expr> has the following generic format:
          <key1> <op1> <val1> && <key2> <op2> <val2> …
    The <key> is the name of the key as passed during archiving of the entry in
    ArchiveSelection <name> addentry or ArchiveSelection <name> adddirectory
    methods.
    The <op> is the logical operation applied to the value. The <val> is the
    value associated with the key. The following logical operations are
    supported:
            "=="  key equals the value
            "*="  key starts with value
    Examples:
       {author *= marco && state == italy}
    To search for files or folders by filename, the key name must be used.
       {name == myfile.pdf}
    or
       {name *= 'my file'}
    When entering expressions, please put curly braces around the complete
    expression. Values in expressions can be enclosed in single quotes, in case
    the value contains one or more blanks, it must be enclosed in single
    quotes.
    NOTE: Only entries that are located on known or accessible volumes are
    reported. If an entry is found in the index but is located on inaccessible
    volume (the volume is disabled, not currently mounted in some tape drive or
    not found in any known media changer), it is not included in the selection.
    Return Values:
    -On Success:    the number of entries in the selection
    """
    method_name = "findentry"
    return exec_nsdchat([module_name, restoreselection_name, method_name, plan,
                         expr], p5_connection)


@onereturnvalue
def onfilecreation(restoreselection_name, command=None, p5_connection=None):
    """
    Syntax: RestoreSelection <name> onfilecreation <command>
    Description: Registers the <command> to be executed immediately after the
    files are created through a job created by the submit method. See
    onobjectactivation for further information.
    Return Values:
    -On Success:    the command string
    """
    method_name = "onfilecreation"
    return exec_nsdchat([module_name, restoreselection_name, method_name,
                         command], p5_connection)


@onereturnvalue
def onjobactivation(restoreselection_name, command=None, p5_connection=None):
    """
    Syntax: RestoreSelection <name> onjobactivation <command>]
    Description: Registers the <command> to be executed just before the job is
    started by the [submit] method. The command itself can be any valid OS
    command plus variable number of arguments.
    The very first argument of the command (the program itself) can be
    prepended with the name of the P5 client where the command is to be
    executed on.
    If omitted, the command will be executed on the client which the
    RestoreSelection object is created for.

    Examples:
    RestoreSelection RestoreSelection.0 onjobactivation
                                            "mickey:/var/scripts/myscript arg"
    will execute /var/scripts/myscript on the client "mickey" regardless what
    client the RestoreSelection is created for. The program will be passed one
    argument: arg.
    RestoreSelection RestoreSelection.0 onjobactivation "/var/scripts/myscript"
    will execute /var/scripts/myscript on the client the RestoreSelection is
    created for.
    RestoreSelection RestoreSelection.0 onjobactivation
                                            "localhost:/var/scripts/myscript"
    will execute /var/scripts/myscript on the P5 server.
    Return Values:
    -On Success:    the command string
    """
    method_name = "onjobactivation"
    return exec_nsdchat([module_name, restoreselection_name, method_name,
                         command], p5_connection)


@onereturnvalue
def onjobcompletion(restoreselection_name, command=None, p5_connection=None):
    """
    Syntax: RestoreSelection <name> onjobcompletion <command>
    Description: Registers the <command> to be executed immediately after the
    job created by the submit method is completed. See onobjectactivation for
    further information.
    Return Values:
    -On Success:    the command string
    """
    method_name = "onjobcompletion"
    return exec_nsdchat([module_name, restoreselection_name, method_name,
                         command], p5_connection)


@onereturnvalue
def size(restoreselection_name, p5_connection=None):
    """
    Syntax: RestoreSelection <name> size
    Description: Returns the summed up size in bytes of all files to restore.
    Return Values:
    -On Success:    the size in bytes
    """
    method_name = "size"
    return exec_nsdchat([module_name, restoreselection_name, method_name],
                        p5_connection)


@onereturnvalue
def submit(restoreselection_name, when=None, as_object=False,
           p5_connection=None):
    """
    Syntax: RestoreSelection <name> submit [<when>]
    Description: Submits the restore selection for execution. The execution is
    started immediately, unless the <when> is given. In that case, the
    execution will be scheduled at the given time. The <when> is the date in
    seconds since Jan 01, 1970 (Posix time).
    Return Values:
    -On Success:    the restore job ID. Use this job ID to query the status
                    of the job by using Job resource.
                    See the Job resource description for details.
    """
    method_name = "submit"
    result = exec_nsdchat([module_name, restoreselection_name, method_name,
                           when], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


def volumes(restoreselection_name, as_object=False, p5_connection=None):
    """
    Syntax: RestoreSelection <name> volumes
    Description: Returns the media volume ID where the entries belonging to the
    restore selection <name> have been archived. An entry can be stored on one
    or more volumes or even many times on the same volume (see the Volume
    resource for more information) during the archive operation, depending on
    the plan configuration.
    Return Values:
    -On Success:    a list of volume ID's containing all the entries
    """
    method_name = "volumes"
    result = exec_nsdchat([module_name, restoreselection_name, method_name],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Volume, p5_connection)


class RestoreSelection(P5Resource):
    def __init__(self, restoreselection_name, p5_connection=None):
        super().__init__(restoreselection_name, p5_connection)

    @onereturnvalue
    def create(client, relocate=None, as_object=True, p5_connection=None):
        """
        Syntax: RestoreSelection create <client> [<relocate>]
        Description: Creates a new temporary restore selection resource. The
        resource will be automatically deleted after the associated archive job
        has been submitted.
        The <client> must be one of the registered client computers on the
        current P5 server. Restored files will be placed on the named client.
        You can get the list of client computers with the Client names CLI
        command.
        The <relocate> overrides default restore location. If this option is
        given, it must point to a directory on the <client> file system. All
        files will be placed in this directory instead of their original
        location. The <relocate> directory must exist on the client.
        Return Values:
        -On Success:    the name of the new resource. Use this name to
                        address the resource in all other methods.
        """
        method_name = "create"
        result = exec_nsdchat([module_name, method_name, client, relocate],
                              p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, RestoreSelection, p5_connection)

    @onereturnvalue
    def addentry(self, archiveentry, path=None):
        """
        Syntax: RestoreSelection <name> addentry <archiveentry> [<path>]
        Description: Adds a new entry <archiveentry> to the restore selection
        <name>. The <archiveentry> is a handle to the archived file as returned
        by the ArchiveSelection addentry.
        By providing the optional path argument, it is possible to specify the
        target path of the restored file.
        Return Values:
        -On Success:    the path to the file to be restored
                        Note: the returned path is not translated to match
                        the optional <relocate> argument given at resource
                        creation.
        """
        method_name = "addentry"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, archiveentry,
                                                path])

    @onereturnvalue
    def addfrom(self, inputfile):
        """
        Description: Loads the Restore Selection entries from the external file
        <input file>. The file must be formatted with one entry per line, each
        entry in the format of:
        <archiveentry>[TAB<relocate path>]
        The <archiveentry> is a handle to the archived file as returned by
        ArchiveSelection addentry.
        In case a <relocate path> is given, the archived file or folder is
        restored at the given path. Otherwise the relocate path as given in the
        RestoreSelection is used.
        Return Values:
        -On Success:    The count of entries that will be restored
        """
        method_name = "addfrom"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, inputfile])
    @onereturnvalue
    def describe(self, title=None):
        """
        Syntax: RestoreSelection <name> describe [title]
        Description: If a title is given, the title is set as description in
        the job monitor.
        The method returns the current description
        Return Values:
        -On Success:    the description string as used in the job monitor
        """
        method_name = "describe"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, title])

    @onereturnvalue
    def destroy(self):
        """
        Syntax: RestoreSelection <name> destroy
        Description: Explicitly destroys the restore selection. The <name>
        should not be used in any RestoreSelection commands afterwards
        Return Values:
        -On Success:    the string "0" (destroyed) or "1" (not destroyed)
        """
        method_name = "destroy"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def entries(self):
        """
        Syntax: RestoreSelection <name> entries
        Description: Returns the number of entries belonging to the restore
        selection <name>.
        Return Values:
        -On Success:    the number of entries
        """
        method_name = "entries"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def findentry(self, plan, expr):
        """
        Syntax: RestoreSelection <name> findentry <plan> {<expr>}
        Description: Fills in the restore selection object by searching the
        archive entries archived with the archive <plan>.
        The <expr> contains the search expression used to locate records. The
        <expr> has the following generic format:
              <key1> <op1> <val1> && <key2> <op2> <val2> …
        The <key> is the name of the key as passed during archiving of the
        entry in ArchiveSelection <name> addentry or ArchiveSelection <name>
        adddirectory methods.
        The <op> is the logical operation applied to the value. The <val> is
        the value associated with the key. The following logical operations are
        supported:
                "=="  key equals the value
                "*="  key starts with value
        Examples:
           {author *= marco && state == italy}
        To search for files or folders by filename, the key name must be used.
           {name == myfile.pdf}
        or
           {name *= 'my file'}
        When entering expressions, please put curly braces around the complete
        expression. Values in expressions can be enclosed in single quotes, in
        case the value contains one or more blanks, it must be enclosed in
        single quotes.
        NOTE: Only entries that are located on known or accessible volumes are
        reported. If an entry is found in the index but is located on
        inaccessible volume (the volume is disabled, not currently mounted in
        some tape drive or not found in any known media changer), it is not
        included in the selection.
        Return Values:
        -On Success:    the number of entries in the selection
        """
        method_name = "findentry"
        return exec_nsdchat([module_name, self.name, method_name, plan, expr])

    @onereturnvalue
    def onfilecreation(self, command=None):
        """
        Syntax: RestoreSelection <name> onfilecreation <command>
        Description: Registers the <command> to be executed immediately after
        the files are created through a job created by the submit method. See
        onobjectactivation for further information.
        Return Values:
        -On Success:    the command string
        """
        method_name = "onfilecreation"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, command])

    @onereturnvalue
    def onjobactivation(self, command=None):
        """
        Syntax: RestoreSelection <name> onjobactivation <command>]
        Description: Registers the <command> to be executed just before the job
        is started by the [submit] method. The command itself can be any valid
        OS command plus variable number of arguments.
        The very first argument of the command (the program itself) can be
        prepended with the name of the P5 client where the command is to be
        executed on.
        If omitted, the command will be executed on the client which the
        RestoreSelection object is created for.

        Examples:
        RestoreSelection RestoreSelection.0 onjobactivation
                                            "mickey:/var/scripts/myscript arg"
        will execute /var/scripts/myscript on the client "mickey" regardless
        what client the RestoreSelection is created for. The program will be
        passed one argument: arg.
        RestoreSelection RestoreSelection.0 onjobactivation
                                                        "/var/scripts/myscript"
        will execute /var/scripts/myscript on the client the RestoreSelection
        is created for.
        RestoreSelection RestoreSelection.0 onjobactivation
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
        Syntax: RestoreSelection <name> onjobcompletion <command>
        Description: Registers the <command> to be executed immediately after
        the job created by the submit method is completed. See
        onobjectactivation for further information.
        Return Values:
        -On Success:    the command string
        """
        method_name = "onjobcompletion"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, command])

    @onereturnvalue
    def size(self):
        """
        Syntax: RestoreSelection <name> size
        Description: Returns the summed up size in bytes of all files to
        restore.
        Return Values:
        -On Success:    the size in bytes
        """
        method_name = "size"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def submit(self, when=None, as_object=True):
        """
        Syntax: RestoreSelection <name> submit [<when>]
        Description: Submits the restore selection for execution. The execution
        is started immediately, unless the <when> is given. In that case, the
        execution will be scheduled at the given time. The <when> is the date
        in seconds since Jan 01, 1970 (Posix time).
        Return Values:
        -On Success:    the restore job ID. Use this job ID to query the status
                        of the job by using Job resource.
                        See the Job resource description for details.
        """
        method_name = "submit"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, when])
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, self.p5_connection)

    def volumes(self, as_object=True):
        """
        Syntax: RestoreSelection <name> volumes
        Description: Returns the media volume ID where the entries belonging to
        the restore selection <name> have been archived. An entry can be stored
        on one or more volumes or even many times on the same volume (see the
        Volume resource for more information) during the archive operation,
        depending on the plan configuration.
        Return Values:
        -On Success:    a list of volume ID's containing all the entries
        """
        method_name = "volumes"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name])
        if not as_object:
            return result
        else:
            return resourcelist(result, Volume, self.p5_connection)

    def __repr__(self):
        return ": ".join([module_name, self.name])
