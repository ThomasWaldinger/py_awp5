# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
ArchiveSelection
The archive selection is used to prepare one or more files and/or directories
for the archive operation. You must create new archive selection resource for
each archive session. You can use the resource methods to populate the
selection (i.e. add files) and then submit the entire selection for immediate
or scheduled execution. The archive selection is a temporary resource. It does
not survive system crashes and server shutdowns, nor it needs to be explicitly
destroyed by the caller. It goes out of scope by invoking the "submit" method,
which effectively passes the control to the Job manager. The owner of the
archive selection resource is thus the P5 system, so the caller needs not (nor
it should) perform any other task with the same resource.
Usage:
To use the ArchiveSelection resource, use the create method to create a new
instance. After creation, use the addentry and/or adddirectory methods to
fill-in the selection with files and/or directories to archive. Finally, submit
the selection for immediate or scheduled execution. After submission, the
resource goes out of scope and should not be used any more.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.archiveentry import ArchiveEntry
from awp5.api.archiveplan import ArchivePlan
from awp5.api.job import Job

module_name = "ArchiveSelection"


@onereturnvalue
def create(client, plan, indexroot=None, as_object=False,
           p5_connection=None):
    """
    Syntax: ArchiveSelection create <client> <plan> [<indexroot>]
    Description: Creates a new temporary archive selection resource. The
    resource will be automatically deleted after the associated archive job has
    been submitted.
    The <client> must be the one of the registered client computers on the
    current P5 server. You can get the list of client computers with the Client
    names CLI command. All files added with the addentry method (below) must
    reside on this client.
    The <plan> must be one of the registered archive plans. You can get the
    list of archive plans with the ArchivePlan names CLI command.
    The optional <indexroot> argument, if given, will force all files in the
    archive selection to be indexed under the <indexroot> path.
    Return Values:
    -On Success:    the name of the new resource. Use this name to
                    address this resource in all other methods.
    """
    method_name = "create"
    result = exec_nsdchat([module_name, method_name, client, plan, indexroot],
                          p5_connection)
    if not as_objects:
        return result
    else:
        return resourcelist(result, ArchiveSelection, p5_connection)


@onereturnvalue
def addfrom(archiveselection_name, inputfile, outputfile, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> addfrom <input file> <output file>
    Description: Loads the Archive Selection entries from the external file
    <input file>. The file must be formatted with one entry per line, each
    entry in the format of:
    <path>TAB<key1>TAB<value1>TAB<key2>TAB<value2>...
    The <path> needs to be resolvable on the client for which the selection is
    created and the <input file> needs to reside on that client.
    The <path> may be followed by zero or more key/value pairs representing
    metadata that will be assigned to the file. All keys must be known in the
    index referenced by the archive selection. Unknown keys will be silently
    skipped.
    The <output file> is created by this command, it contains all accepted
    files with their ArchiveEntry handles used to reference the files later.
    The file format is one file per line in the format of:
    <path>TAB<handle>
    Note that unlike ArchiveSelection addentry, this method will add folders as
    empty nodes. This means:
        - folders are added without content, metadata in that case is assigned
        only to the folder
        - If files are added into a non existing folder in the archive, the
        folder is created without attributes or metadata.
    Return Values:
    -On Success:    the number of added key/value pairs
    """
    method_name = "addfrom"
    return exec_nsdchat([module_name, archiveselection_name, method_name,
                         inputfile, outputfile], p5_connection)


@onereturnvalue
def addentry(archiveselection_name, path, key_value_list=None, as_object=False,
             p5_connection=None):
    """
    Syntax: ArchiveSelection <name> addentry <path>
            [<key> <value> [<key> <value>].. ]
    Description: Adds a single new <path> to the archive selection <name>. It
    expects the absolute path to the file or directory to be archived. The file
    or directory must be located on the client <client> given at the resource
    creation time (see the create method).
    The path will be stripped of the leading directory part and the name will
    be inserted into the index at the indexroot destination as defined in
    create. If the passed <path> contains blanks, be sure to enclose it in
    curly braces: {/some/path with blanks/file}. Furthermore, if the <path>
    contains { and/or } chars themselves, you must escape them with a backslash
    '\' character.
    To each path, you can assign an arbitrary number of <key> and <value>
    pairs. Those are saved in the archive index and can be used for searches
    during restore (see RestoreSelection).
    Each key allows a string value of unlimited length. If the value contains
    blanks, it should be enclosed in curly braces. If the value itself contains
    curly braces, you must escape them with '\' character.
    In case the ArchiveSelection is set to incremental level and the given
    entry is already part of the Archive, the entry is not added and an string
    string <empty> is returned.

    Return Values:
    -On Success:    the name of the new ArchiveEntry resource.
                    This name must be used with ArchiveEntry methods
                    to get the status and other meta-information for the
                    entry after the archive operation has been completed.
                    Please see the ArchiveEntry resource description
    """
    method_name = "addentry"
    result = exec_nsdchat([module_name, archiveselection_name, method_name,
                           path, key_value_list], p5_connection)
    if not as_objects:
        return result
    else:
        return resourcelist(result, ArchiveEntry, p5_connection)


@onereturnvalue
def addentryabs(archiveselection_name, path, key_value_list=None,
                as_object=False, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> addentryabs <path>
            [<key> <value> [<key> <value>].. ]
    Description: Adds one new <path> to the archive selection <name>. It
    expects the absolute path to the file or directory to be archived. The file
    or directory must be located on the client <client> given at the resource
    creation time (see the create method).
    The entry path will be added 1:1 into the index. Any prefixes and
    alternative index destinations are ignored. If the passed <path> contains
    blanks, be sure to enclose it in curly braces:
    {/some/path with blanks/file}. Furthermore, if the <path> contains
    { and/or } chars themselves, you must escape them with a backslash '\'
    character.
    To each path, you can assign an arbitrary number of <key> and <value>
    pairs. Those are saved in the archive index and can be used for searches
    during restore (see RestoreSelection).
    Each key allows a string value of unlimited length. If the value contains
    blanks, it should be enclosed in curly braces. If the value itself contains
    curly braces, you must escape them with '\' character.
    Return Values:
    -On Success:    the name of the new ArchiveEntry resource.
                    This name must be used with ArchiveEntry methods
                    to get the status and other meta-information of the
                    entry after the archive operation has been completed.
                    Please see the ArchiveEntry resource description
    """
    method_name = "addentryabs"
    result = exec_nsdchat([module_name, archiveselection_name, method_name,
                           path, key_value_list], p5_connection)
    if not as_objects:
        return result
    else:
        return resourcelist(result, ArchiveEntry, p5_connection)


@onereturnvalue
def adddirectory(archiveselection_name, path, key_value_list=None,
                 as_object=False, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> adddirectory <path>
            [<key> <value> [<key> <value>].. ]
    Description: Adds a new directory <path> to the archive selection <name>.
    It expects the absolute path to the directory to be archived. The directory
    must be located on the client <client> given at the resource creation time
    (see the create method).
    The path will be stripped of the leading directory part and the name will
    be inserted into the index at the indexroot destination as defined in
    create.
    Note that this method will only add the directory node to the archive
    selection and that only a directory node itself will be archived. If you
    want to archive both the directory and its contents recursively, use the
    ArchiveSelection addentry method.
    See the addentry method description for explanation of other method
    arguments.
    Return Values:
    -On Success:    see the addentry description for return values
    """
    method_name = "adddirectory"
    result = exec_nsdchat([module_name, archiveselection_name, method_name,
                           path, key_value_list], p5_connection)
    if not as_objects:
        return result
    else:
        return resourcelist(result, ArchiveEntry, p5_connection)


@onereturnvalue
def adddirectoryabs(archiveselection_name, path, key_value_list=None,
                    as_object=False, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> adddirectoryabs <path>
            [<key> <value> [<key> <value>].. ]
    Description: Adds a new directory <path> to the archive selection <name>.
    It expects the absolute path to the directory to be archived. The directory
    must be located on the client <client> given at the resource creation time
    (see the create method).
    The directory path will be added 1:1 into the index. Any prefixes and
    alternative index destinations are ignored.
    Note that this method will only add the directory node to the archive
    selection and that only a directory node itself will be archived. If you
    want to archive both the directory and its contents recursively, use the
    ArchiveSelection addentry method.
    See the addentry method description for explanation of other method
    arguments.
    Return Values:
    -On Success:    see the addentry method for return values
    """
    method_name = "adddirectoryabs"
    result = exec_nsdchat([module_name, archiveselection_name, method_name,
                           path, key_value_list], p5_connection)
    if not as_objects:
        return result
    else:
        return resourcelist(result, ArchiveEntry, p5_connection)


@onereturnvalue
def addfile(archiveselection_name, path, key_value_list=None,
            as_object=False, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> addfile <path>
            [<key> <value> [<key> <value>].. ]
    Description: Adds a new file <path> to the archive selection <name>. It
    expects the absolute path to the file to be archived. The file must be
    located on the client <client> given at the resource creation time (see the
    create method).
    The path will be stripped of the leading directory part and the name will
    be inserted into the index at the indexroot destination as defined in
    create.
    See the addentry method description for explanation of other method
    arguments.
    Return Values:
    -On Success:    see the addentry method for return values
    """
    method_name = "addfile"
    result = exec_nsdchat([module_name, archiveselection_name, method_name,
                           path, key_value_list], p5_connection)
    if not as_objects:
        return result
    else:
        return resourcelist(result, ArchiveEntry, p5_connection)


@onereturnvalue
def addfileabs(archiveselection_name, path, key_value_list=None,
               as_object=False, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> addfileabs <path>
            [<key> <value> [<key> <value>].. ]
    Description: Adds a new file <path> to the archive selection <name>. It
    expects the absolute path to the file to be archived. The file must be
    located on the client <client> given at the resource creation time (see the
    create method).
    The directory path will be added 1:1 into the index. Any prefixes and
    alternative index destinations are ignored.
    See the addentry method description for explanation of other method
    arguments.
    Return Values:
    -On Success:    see the addentry method for return values
    """
    method_name = "addfileabs"
    result = exec_nsdchat([module_name, archiveselection_name, method_name,
                           path, key_value_list], p5_connection)
    if not as_objects:
        return result
    else:
        return resourcelist(result, ArchiveEntry, p5_connection)


@onereturnvalue
def describe(archiveselection_name, title=None, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> describe [title]
    Description: If a title is given, the title is set as the description in
    the job monitor.
    The method returns the current description
    Return Values:
    -On Success:    the descriptions string as used in the job monitor
    """
    method_name = "describe"
    return exec_nsdchat([module_name, archiveselection_name, method_name,
                         title], p5_connection)


@onereturnvalue
def destroy(archiveselection_name, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> destroy
    Description: Explicitly destroys the archive selection. The <name> should
    not be used in any ArchiveSelection commands afterwards.
    Return Values:
    -On Success:    the string "0" (destroyed)
                    the string "1" (not destroyed)
    """
    method_name = "destroy"
    return exec_nsdchat([module_name, archiveselection_name, method_name],
                        p5_connection)


@onereturnvalue
def entries(archiveselection_name, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> entires
    Description: Returns the number of entries in the selection object.
    Return Values:
    -On Success:    the number of entries
    """
    method_name = "size"
    return exec_nsdchat([module_name, archiveselection_name, method_name],
                        p5_connection)


@onereturnvalue
def level(archiveselection_name, level_value=None, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> [level]
    Description: Returns the level of the ArchiveSelection.
    If the optional level value is given, that level is set.
    The level must be either “full” or “increment”.
    Return Values:
    -On Success:    the string “full” or “increment”
    """
    method_name = "level"
    return exec_nsdchat([module_name, archiveselection_name, method_name,
                         level_value], p5_connection)


@onereturnvalue
def size(archiveselection_name, p5_connection=None):
    """
    Syntax: ArchiveSelection <name> size
    Description: Returns the number of entries in the selection object.
    This method is deprecated, please use ArchiveSelection entries instead.
    Return Values:
    -On Success:    the number of entries
    """
    method_name = "size"
    return exec_nsdchat([module_name, archiveselection_name, method_name],
                        p5_connection)


@onereturnvalue
def submit(archiveselection_name, now=True, as_object=False,
           p5_connection=None):
    """
    Syntax: ArchiveSelection <name> submit [<now>]
    Description: Submits the archive selection for execution. You can
    optionally override plan execution times by giving the <now> as one of the
    strings "1", "t", "true", "True", "y", "yes", or "Yes".
    This command implicitly destroys the ArchiveSelection object for the user
    and transfers the ownership of the internal underlying object to the job
    scheduler. You should not attempt to use the <name> afterwards.
    Return Values:
    -On Success:    the archive job ID. Use this job ID to query the
                    status of the job by using Job resource.
                    Please see the Job resource description for details.
    """
    method_name = "submit"
    now_option = ""
    if now is True:
        now_option = "1"
    result = exec_nsdchat([module_name, archiveselection_name, method_name,
                           now_option], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def onjobactivation(archiveselection_name, p5_connection=None, command=None):
    """
    Syntax: ArchiveSelection <name> onjobactivation <command>]
    Description: Registers the <command> to be executed just before the job is
    started by the submit method. The command itself can be any valid OS
    command plus variable number of arguments.
    The very first argument of the command (the program itself) can be
    prepended with the name of the P5 client where the command is to be
    executed on. If omitted, the command will be executed on the client which
    the ArchiveSelection object is created for.

    Examples:
    ArchiveSelection 10002 onjobactivation "mickey:/var/scripts/myscript arg"
    will execute /var/scripts/myscript on the client "mickey" regardless of the
    client the ArchiveSelection is created for. The program will be passed one
    argument: arg.
    ArchiveSelection 10002 onjobactivation "/var/scripts/myscript"
    will execute /var/scripts/myscript on the client the ArchiveSelection is
    created for.
    ArchiveSelection 10002 onjobactivation "localhost:/var/scripts/myscript"
    will execute /var/scripts/myscript on the P5 server.
    Return Values:
    -On Success:    the command string
    """
    method_name = "onjobactivation"
    return exec_nsdchat([module_name, archiveselection_name, method_name,
                         command], p5_connection)


@onereturnvalue
def onjobcompletion(archiveselection_name, p5_connection=None, command=None):
    """
    Syntax: ArchiveSelection <name> onjobcompletion <command>
    Description: Registers the <command> to be executed immediately after the
    job created by the submit method is completed. See onjobactivation for
    further information.
    Return Values:
    -On Success:    the command string
    """
    method_name = "onjobcompletion"
    return exec_nsdchat([module_name, archiveselection_name, method_name,
                         command], p5_connection)


@onereturnvalue
def onfiledeletion(archiveselection_name, p5_connection=None, command=None):
    """
    Syntax: ArchiveSelection <name> onfiledeletion <command>
    Description: Registers the <command> to be executed immediately after the
    files are deleted through a job created by the submit method. See
    onjobactivation for further information.
    Return Values:
    -On Success:    the command string
    """
    method_name = "onfiledeletion"
    return exec_nsdchat([module_name, archiveselection_name, method_name,
                         command], p5_connection)


class ArchiveSelection(P5Resource):
    def __init__(self, archiveselection_name, p5_connection=None):
        super().__init__(archiveselection_name, p5_connection)

    @onereturnvalue
    def create(client, plan, indexroot=None, as_objects=True, p5_connection=None):
        """
        Syntax: ArchiveSelection create <client> <plan> [<indexroot>]
        Description: Creates a new temporary archive selection resource. The
        resource will be automatically deleted after the associated archive job
        has been submitted.
        The <client> must be the one of the registered client computers on the
        current P5 server. You can get the list of client computers with the
        Client names CLI command. All files added with the addentry method
        (below) must reside on this client.
        The <plan> must be one of the registered archive plans. You can get the
        list of archive plans with the ArchivePlan names CLI command.
        The optional <indexroot> argument, if given, will force all files in
        the archive selection to be indexed under the <indexroot> path.
        Return Values:
        -On Success:    the name of the new resource. Use this name to
                        address this resource in all other methods.
        """
        method_name = "create"
        result = exec_nsdchat([module_name, method_name, client, plan,
                               indexroot], p5_connection)
        if not as_objects:
            return result
        else:
            return resourcelist(result, ArchiveSelection, p5_connection)

    @onereturnvalue
    def addfrom(self, inputfile, outputfile):
        """
        Syntax: ArchiveSelection <name> addfrom <input file> <output file>
        Description: Loads the Archive Selection entries from the external file
        <input file>. The file must be formatted with one entry per line, each
        entry in the format of:
        <path>TAB<key1>TAB<value1>TAB<key2>TAB<value2>...
        The <path> needs to be resolvable on the client for which the selection
        is created and the <input file> needs to reside on that client.
        The <path> may be followed by zero or more key/value pairs representing
        metadata that will be assigned to the file. All keys must be known in
        the index referenced by the archive selection. Unknown keys will be
        silently skipped.
        The <output file> is created by this command, it contains all accepted
        files with their ArchiveEntry handles used to reference the files
        later. The file format is one file per line in the format of:
        <path>TAB<handle>
        Note that unlike ArchiveSelection addentry, this method will add
        folders as empty nodes. This means:
            - folders are added without content, metadata in that case is
            assigned only to the folder
            - If files are added into a non existing folder in the archive, the
            folder is created without attributes or metadata.
        Return Values:
        -On Success:    the number of added key/value pairs
        """
        method_name = "addfrom"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, inputfile,
                                                outputfile])

    @onereturnvalue
    def addentry(self, path, key_value_list=None, as_object=True):
        """
        Syntax: ArchiveSelection <name> addentry <path>
                [<key> <value> [<key> <value>].. ]
        Description: Adds a single new <path> to the archive selection <name>.
        It expects the absolute path to the file or directory to be archived.
        The file or directory must be located on the client <client> given at
        the resource creation time (see the create method).
        The path will be stripped of the leading directory part and the name
        will be inserted into the index at the indexroot destination as defined
        in create.
        If the passed <path> contains blanks, be sure to enclose it in curly
        braces: {/some/path with blanks/file}. Furthermore, if the <path>
        contains { and/or } chars themselves, you must escape them with a
        backslash '\' character.
        To each path, you can assign an arbitrary number of <key> and <value>
        pairs. Those are saved in the archive index and can be used for
        searches during restore (see RestoreSelection).
        Each key allows a string value of unlimited length. If the value
        contains blanks, it should be enclosed in curly braces. If the value
        itself contains curly braces, you must escape them with '\' character.
        In case the ArchiveSelection is set to incremental level and the given
        entry is already part of the Archive, the entry is not added and an
        empty string is returned.

        Return Values:
        -On Success:    the name of the new ArchiveEntry resource.
                        This name must be used with ArchiveEntry methods
                        to get the status and other meta-information for the
                        entry after the archive operation has been completed.
                        Please see the ArchiveEntry resource description
        """
        method_name = "addentry"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, path,
                                                  key_value_list_option])
        if not as_objects:
            return result
        else:
            return resourcelist(result, ArchiveEntry, self.p5_connection)

    @onereturnvalue
    def addentryabs(self, path, key_value_list=None, as_object=True):
        """
        Syntax: ArchiveSelection <name> addentryabs <path>
                [<key> <value> [<key> <value>].. ]
        Description: Adds one new <path> to the archive selection <name>. It
        expects the absolute path to the file or directory to be archived. The
        file or directory must be located on the client <client> given at the
        resource creation time (see the create method).
        The entry path will be added 1:1 into the index. Any prefixes and
        alternative index destinations are ignored.
        If the passed <path> contains blanks, be sure to enclose it in curly
        braces: {/some/path with blanks/file}. Furthermore, if the <path>
        contains { and/or } chars themselves, you must escape them with a
        backslash '\' character.
        To each path, you can assign an arbitrary number of <key> and <value>
        pairs. Those are saved in the archive index and can be used for
        searches during restore (see RestoreSelection).
        Each key allows a string value of unlimited length. If the value
        contains blanks, it should be enclosed in curly braces. If the value
        itself contains curly braces, you must escape them with '\' character.
        Return Values:
        -On Success:    the name of the new ArchiveEntry resource.
                        This name must be used with ArchiveEntry methods
                        to get the status and other meta-information of the
                        entry after the archive operation has been completed.
                        Please see the ArchiveEntry resource description
        """
        method_name = "addentryabs"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, path,
                                                  key_value_list_option])
        if not as_objects:
            return result
        else:
            return resourcelist(result, ArchiveEntry, self.p5_connection)

    @onereturnvalue
    def adddirectory(self, path, key_value_list=None, as_object=True):
        """
        Syntax: ArchiveSelection <name> adddirectory <path>
                [<key> <value> [<key> <value>].. ]
        Description: Adds a new directory <path> to the archive selection
        <name>. It expects the absolute path to the directory to be archived.
        The directory must be located on the client <client> given at the
        resource creation time (see the create method).
        The path will be stripped of the leading directory part and the name
        will be inserted into the index at the indexroot destination as defined
        in create.
        Note that this method will only add the directory node to the archive
        selection and that only a directory node itself will be archived. If
        you want to archive both the directory and its contents recursively,
        use the ArchiveSelection addentry method.
        See the addentry method description for explanation of other method
        arguments.
        Return Values:
        -On Success:    see the addentry description for return values
        """
        method_name = "adddirectory"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, path,
                                                  key_value_list_option])
        if not as_objects:
            return result
        else:
            return resourcelist(result, ArchiveEntry, self.p5_connection)

    @onereturnvalue
    def adddirectoryabs(self, path, key_value_list=None, as_object=True):
        """
        Syntax: ArchiveSelection <name> adddirectoryabs <path>
                [<key> <value> [<key> <value>].. ]
        Description: Adds a new directory <path> to the archive selection
        <name>. It expects the absolute path to the directory to be archived.
        The directory must be located on the client <client> given at the
        resource creation time (see the create method).
        The directory path will be added 1:1 into the index. Any prefixes and
        alternative index destinations are ignored.
        Note that this method will only add the directory node to the archive
        selection and that only a directory node itself will be archived. If
        you want to archive both the directory and its contents recursively,
        use the ArchiveSelection addentry method.
        See the addentry method description for explanation of other method
        arguments.
        Return Values:
        -On Success:    see the addentry method for return values
        """
        method_name = "adddirectoryabs"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, path,
                                                  key_value_list_option])
        if not as_objects:
            return result
        else:
            return resourcelist(result, ArchiveEntry, self.p5_connection)

    @onereturnvalue
    def addfile(self, path, key_value_list=None, as_object=True):
        """
        Syntax: ArchiveSelection <name> addfile <path>
                [<key> <value> [<key> <value>].. ]
        Description: Adds a new file <path> to the archive selection <name>. It
        expects the absolute path to the file to be archived. The file must be
        located on the client <client> given at the resource creation time (see
        the create method).
        The path will be stripped of the leading directory part and the name
        will be inserted into the index at the indexroot destination as defined
        in create.
        See the addentry method description for explanation of other method
        arguments.
        Return Values:
        -On Success:    see the addentry method for return values
        """
        method_name = "addfile"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, path,
                                                  key_value_list_option])
        if not as_objects:
            return result
        else:
            return resourcelist(result, ArchiveEntry, self.p5_connection)

    @onereturnvalue
    def addfileabs(self, path, key_value_list=None, as_object=True):
        """
        Syntax: ArchiveSelection <name> addfileabs <path>
                [<key> <value> [<key> <value>].. ]
        Description: Adds a new file <path> to the archive selection <name>. It
        expects the absolute path to the file to be archived. The file must be
        located on the client <client> given at the resource creation time
        (see the create method).
        The directory path will be added 1:1 into the index. Any prefixes and
        alternative index destinations are ignored.
        See the addentry method description for explanation of other method
        arguments.
        Return Values:
        -On Success:    see the addentry method for return values
        """
        method_name = "addfileabs"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, path,
                                                  key_value_list_option])
        if not as_objects:
            return result
        else:
            return resourcelist(result, ArchiveEntry, self.p5_connection)

    @onereturnvalue
    def describe(self, title=None):
        """
        Syntax: ArchiveSelection <name> describe  [title]
        Description: If a title is given, the title is set as the description
        in the job monitor. The method returns the current description
        Return values:
        -On success:	the descriptions string as used in the job monitor
        """
        method_name = "describe"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, title])

    @onereturnvalue
    def destroy(self):
        """
        Syntax: ArchiveSelection <name> destroy
        Description: Explicitly destroys the archive selection. The <name>
        should not be used in any ArchiveSelection commands afterwards.
        Return Values:
        -On Success:    the string "0" (destroyed)
                        the string "1" (not destroyed)
        """
        method_name = "destroy"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def entries(self):
        """
        Syntax: ArchiveSelection <name> entries
        Description: Returns the number of entries in the selection object.
        Return Values:
        -On Success:    the number of entries
        """
        method_name = "entries"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def level(self, level_value=None):
        """
        Syntax: ArchiveSelection <name> [level]
        Description: Returns the level of the ArchiveSelection.
        If the optional level value is given, that level is set.
        The level must be either “full” or “increment”.
        Return Values:
        -On Success:    the string “full” or “increment”
        """
        method_name = "level"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, level_value])

    @onereturnvalue
    def size(self):
        """
        Syntax: ArchiveSelection <name> size
        Description: Returns the number of entries in the selection object.
        This method is deprecated, please use ArchiveSelection entries instead.
        Return Values:
        -On Success:    the number of entries
        """
        method_name = "size"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def submit(self, archiveselection_name, now=True, as_object=True):
        """
        Syntax: ArchiveSelection <name> submit [<now>]
        Description: Submits the archive selection for execution. You can
        optionally override plan execution times by giving the <now> as one of
        the strings "1", "t", "true", "True", "y", "yes", or "Yes".
        This command implicitly destroys the ArchiveSelection object for the
        user and transfers the ownership of the internal underlying object to
        the job scheduler. You should not attempt to use the <name> afterwards.
        Return Values:
        -On Success:    the archive job ID. Use this job ID to query the
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

    @onereturnvalue
    def onjobactivation(self, command=None):
        """
        Syntax: ArchiveSelection <name> onjobactivation <command>]
        Description: Registers the <command> to be executed just before the job
        is started by the submit method. The command itself can be any valid OS
        command plus variable number of arguments.
        The very first argument of the command (the program itself) can be
        prepended with the name of the P5 client where the command is to be
        executed on.
        If omitted, the command will be executed on the client which the
        ArchiveSelection object is created for.

        Examples:
        ArchiveSelection 10002 onjobactivation
                                            "mickey:/var/scripts/myscript arg"
        will execute /var/scripts/myscript on the client "mickey" regardless of
        the client the ArchiveSelection is created for. The program will be
        passed one argument: arg.
        ArchiveSelection 10002 onjobactivation "/var/scripts/myscript"
        will execute /var/scripts/myscript on the client the ArchiveSelection
        is created for.
        ArchiveSelection 10002 onjobactivation
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
        Syntax: ArchiveSelection <name> onjobcompletion <command>
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
    def onfiledeletion(self, command=None):
        """
        Syntax: ArchiveSelection <name> onfiledeletion <command>
        Description: Registers the <command> to be executed immediately after
        the files are deleted through a job created by the submit method. See
        onjobactivation for further information.
        Return Values:
        -On Success:    the command string
        """
        method_name = "onjobcompletion"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, command])

    def __repr__(self):
        return ": ".join([module_name, self.name])
