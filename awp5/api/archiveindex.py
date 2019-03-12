# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
ArchiveIndex
Queries P5 archive index databases and their parameters. Archive index
databases are used to track information about archived files, their location
on the storage media, user-defined meta-data and related information.
In the current version of the CLI, you only have limited write access to
archive index databases. You can modify some configuration details of the
existing databases and you can create new ones. If you need full control of
ArchiveIndex resources, please use the P5 Web GUI.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue

module_name = "ArchiveIndex"


def names(as_object=False, p5_connection=None):
    """
    Syntax: ArchiveIndex names
    Description: Returns the list of names of archive indexes.
    Return Values:
    -On Success:    a list of names. If no archive indexes are configured,
                    the command returns the string "<empty>"
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, ArchiveIndex, p5_connection)


@onereturnvalue
def create(archiveindex_name, description, as_object=False,
           p5_connection=None):
    """
    Syntax: ArchiveIndex create <name> <description>
    Description: Creates the <name> archive index database and its
    <description>. If an archive index with the same <name> already exists, an
    error is thrown. The <name> must not contain blanks, special punctuation
    characters nor any special national characters. The <description> may
    contain any text.
    Return Values:
    -On Success:    the name of the newly created index database
    """
    method_name = "create"
    result = exec_nsdchat([module_name, method_name, archiveindex_name,
                           description], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, ArchiveIndex, p5_connection)


@onereturnvalue
def backup(archiveindex_name, filename, p5_connection=None):
    """
    Syntax: ArchiveIndex <name> backup <filename>
    Description: Produces the backup of the <name> archive index and saves the
    backup file as <filename>.
    Return Values:
    -On Success:    the file name of the backup file
    """
    method_name = "backup"
    return exec_nsdchat([module_name, archiveindex_name, method_name,
                        filename], p5_connection)


@onereturnvalue
def restore(archiveindex_name, filename, p5_connection=None):
    """
    Syntax: ArchiveIndex <name> restore <filename>
    Description: Restores the archive database <name> from the given
    <filename>. The <filename> must be the one used to produce the backup of
    the database (see the backup methog).
    Return Values:
    -On Success:    the name of the backup file
    """
    method_name = "restore"
    return exec_nsdchat([module_name, archiveindex_name, method_name,
                        filename], p5_connection)


def addkey(archiveindex_name, key, key_type, attr_value_list=None,
           p5_connection=None):
    """
    Syntax: ArchiveIndex <name> addkey <key> <type> [<attr> <value>...]
    Description: Adds a user-defined key in the given index. The <key>
    identifier must not contain blanks, special punctuation characters nor any
    national characters. The length of the <key> identifier must not exceed 15
    characters. The <type> designates the data type reserved for the <key>. It
    must be one of:
            C       character key
            N       numeric key

    This command also accepts a variable number of user defined attributes and
    their values attached to the <key>.  Both <attr> and <value> may contain
    any characters, but the length of each of them is limited to 15 characters.
    These entries are optional and are not interpreted by P5 in any way, except
    for being stored in the key definition in the archive index.
    Return Values:
    -On Success:    the names of all the configured keys
    """
    method_name = "addkey"
    return exec_nsdchat([module_name, archiveindex_name, method_name, key,
                        key_type, attr_value_list], p5_connection)


def delkey(archiveindex_name, key, p5_connection=None):
    """
    Syntax: ArchiveIndex <name> delkey <key>
    Description: Deletes a user-defined key in the given index.
    Return Values:
    -On Success:    the names of all the deleted keys
    """
    method_name = "delkey"
    return exec_nsdchat([module_name, archiveindex_name, method_name, key],
                        p5_connection)


def keys(archiveindex_name, p5_connection=None):
    """
    Syntax: ArchiveIndex <name> keys
    Description: Reports all the user-defined meta keys for the index <name>.
    Meta keys are used to store user-given meta-data to selected elements of
    the archive index.
    Return Values:
    -On Success:    a list of keys
                    the string "<empty>" if no keys were defined
    """
    method_name = "keys"
    return exec_nsdchat([module_name, archiveindex_name, method_name],
                        p5_connection)


def keyget(archiveindex_name, key, attr=None, p5_connection=None):
    """
    Syntax: ArchiveIndex <name> keyget <key> [<attr>]
    Description: Returns the attributes for the given <key>. If no optional
    <attr> is supplied, all the defined attributes and their values as a list
    of key/value pairs is returned. If the <attr> is supplied, the value of the
    <attr> attribute is returned.
    Each <key> has at least the type one attribute.
    Please see the addkey method for description of the type attribute.
    Return Values:
    -On Success:    either a list of all the defined attributes and values for
                    the given <key>, or just the attribute value, depending
                    on the existence of the optional argument <attr>
    """
    method_name = "addkey"
    return exec_nsdchat([module_name, archiveindex_name, method_name, key,
                        attr], p5_connection)


@onereturnvalue
def keyhas(archiveindex_name, key, attr, p5_connection=None):
    """
    Syntax: ArchiveIndex <name> keyhas <key> <attr>
    Description: Checks whether the <key> has attribute <attr> defined
    Return Values:
    -On Success:    the string "1" if yes, or "0" otherwise
    """
    method_name = "keyhas"
    return exec_nsdchat([module_name, archiveindex_name, method_name, key,
                        attr], p5_connection)


@onereturnvalue
def keyset(archiveindex_name, key, attr, val, p5_connection=None):
    """
    Syntax: ArchiveIndex <name> keyset <key> <attr> <val>
    Description: Sets the value <val> of the user-given attribute <attr> for
    the given <key>. The value of the type attribute cannot be set. Please see
    the addkey method for a description of the type attribute.
    Return Values:
    -On Success:    the string "1" if the <attr> was set to the given value
                    <val> or
                    the string "0" if the key could not be set or if it
                    does not exist
    """
    method_name = "keyset"
    return exec_nsdchat([module_name, archiveindex_name, method_name, key,
                        attr, val], p5_connection)


@onereturnvalue
def inventory(archiveindex_name, outputfile, options_list=None,
              p5_connection=None):
    """
    Syntax: ArchiveIndex <name> inventory <output file> [<options>]
    Description: Outputs a list of the files contained in the Archive Index
    <name> into a file. The <output file> must be in the form
    ?client:?absolute_path whereby client is the name of the P5 client where to
    store the file and absolute_path is the complete path to the file to hold
    the output. The client part is optional and defaults to localhost:
    The inventory command fills in the passed file with lines containing
    records separated by a TAB. If no <options> are given, the output file will
    by default contain the index paths of all the files saved by the given job
    <name>, one record per line. Additional <options> represent the attributes
    that will be output for each file in a tab-separated format. These
    attributes may be system attributes or any user-defined meta-data fields.
    The supported system attributes are:

    ppath:
    volumes:

    size:
    handle:
    btime:
    mtime:
    ino:
    the physical path of the file on the filesystem
    a blank separated list of the volumes where the file is saved
    the size of the saved file
    the handle as required by the RestoreSelection
    the backup time of the file
    the file's modification time
    the inode number of the file

    The index path returned by the inventory command cannot be used to access
    files on the file system in general. There are special cases where this
    might be used for this purpose, but generally it is not supported. The idea
    behind this info is to have an overview or idea what is being stored in the
    index and not to consume it in some other fashion (i.e. address the files
    on the file system to post-process them).
    In cases where files are still expected to be in the file system at the
    place they were at the point of archiving (for example somebody wants to
    delete them or otherwise post-process them) the ppath attribute may be
    used, which, when given on the command line, will yield the physical path
    as-found on the client where the file resides. Note that not all index
    entries have corresponding physical paths. In such cases the value will be
    set to empty.
    Return Values:
    -On Success:    the <client>:<output file>
    """
    method_name = "inventory"
    return exec_nsdchat([module_name, archiveindex_name, method_name,
                         outputfile, options_list], p5_connection)


class ArchiveIndex(P5Resource):
    def __init__(self, archiveindex_name, p5_connection=None):
        super().__init__(archiveindex_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: ArchiveIndex names
        Description: Returns the list of names of archive indexes.
        Return Values:
        -On Success:    a list of names. If no archive indexes are configured,
                        the command returns the string "<empty>"
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, ArchiveIndex, p5_connection)

    @onereturnvalue
    def create(archiveindex_name, description, as_object=True,
               p5_connection=None):
        """
        Syntax: ArchiveIndex create <name> <description>
        Description: Creates the <name> archive index database and its
        <description>. If an archive index with the same <name> already exists,
        an error is thrown. The <name> must not contain blanks, special
        punctuation characters nor any special national characters. The
        <description> may contain any text.
        Return Values:
        -On Success:    the name of the newly created index database
        """
        method_name = "create"
        result = exec_nsdchat([module_name, method_name, archiveindex_name,
                               description], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, ArchiveIndex, p5_connection)

    @onereturnvalue
    def backup(self, filename):
        """
        Syntax: ArchiveIndex <name> backup <filename>
        Description: Produces the backup of the <name> archive index and saves
        the backup file as <filename>.
        Return Values:
        -On Success:    the file name of the backup file
        """
        method_name = "backup"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, filename])

    @onereturnvalue
    def restore(self, filename):
        """
        Syntax: ArchiveIndex <name> restore <filename>
        Description: Restores the archive database <name> from the given
        <filename>. The <filename> must be the one used to produce the backup
        of the database (see the backup methog).
        Return Values:
        -On Success:    the name of the backup file
        """
        method_name = "restore"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, filename])

    def addkey(self, key, key_type, attr_value_list=None):
        """
        Syntax: ArchiveIndex <name> addkey <key> <type> [<attr> <value>...]
        Description: Adds a user-defined key in the given index. The <key>
        identifier must not contain blanks, special punctuation characters nor
        any national characters. The length of the <key> identifier must not
        exceed 15 characters. The <type> designates the data type reserved for
        the <key>. It must be one of:
                C       character key
                N       numeric key

        This command also accepts a variable number of user defined attributes
        and their values attached to the <key>.  Both <attr> and <value> may
        contain any characters, but the length of each of them is limited to 15
        characters. These entries are optional and are not interpreted by P5 in
        any way, except for being stored in the key definition in the archive
        index.
        Return Values:
        -On Success:    the names of all the configured keys
        """
        method_name = "addkey"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, key, key_type,
                                                attr_value_list])

    def delkey(self, key):
        """
        Syntax: ArchiveIndex <name> delkey <key>
        Description: Deletes a user-defined key in the given index.
        Return Values:
        -On Success:    the names of all the deleted keys
        """
        method_name = "delkey"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, key])

    def keys(self):
        """
        Syntax: ArchiveIndex <name> keys
        Description: Reports all the user-defined meta keys for the index
        <name>. Meta keys are used to store user-given meta-data to selected
        elements of the archive index.
        Return Values:
        -On Success:    a list of keys
                        the string "<empty>" if no keys were defined
        """
        method_name = "keys"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def keyget(self, key, attr=None):
        """
        Syntax: ArchiveIndex <name> keyget <key> [<attr>]
        Description: Returns the attributes for the given <key>. If no optional
        <attr> is supplied, all the defined attributes and their values as a
        list of key/value pairs is returned. If the <attr> is supplied, the
        value of the <attr> attribute is returned.
        Each <key> has at least the type one attribute.
        Please see the addkey method for description of the type attribute.
        Return Values:
        -On Success:    either a list of all the defined attributes and values
                        for the given <key>, or just the attribute value,
                        depending on the existence of the optional argument
                        <attr>
        """
        method_name = "addkey"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, key, attr])

    @onereturnvalue
    def keyhas(self, key, attr):
        """
        Syntax: ArchiveIndex <name> keyhas <key> <attr>
        Description: Checks whether the <key> has attribute <attr> defined
        Return Values:
        -On Success:    the string "1" if yes, or "0" otherwise
        """
        method_name = "keyhas"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, key, attr])

    @onereturnvalue
    def keyset(self, key, attr, val):
        """
        Syntax: ArchiveIndex <name> keyset <key> <attr> <val>
        Description: Sets the value <val> of the user-given attribute <attr>
        for the given <key>. The value of the type attribute cannot be set.
        Please see the addkey method for a description of the type attribute.
        Return Values:
        -On Success:    the string "1" if the <attr> was set to the given value
                        <val> or
                        the string "0" if the key could not be set or if it
                        does not exist
        """
        method_name = "keyset"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, key, attr, val])

    @onereturnvalue
    def inventory(self, outputfile, options_list=None):
        """
        Syntax: ArchiveIndex <name> inventory <output file> [<options>]
        Description: Outputs a list of the files contained in the Archive Index
        <name> into a file. The <output file> must be in the form
        ?client:?absolute_path whereby client is the name of the P5 client
        where to store the file and absolute_path is the complete path to the
        file to hold the output. The client part is optional and defaults to
        localhost: The inventory command fills in the passed file with lines
        containing records separated by a TAB. If no <options> are given, the
        output file will by default contain the index paths of all the files
        saved by the given job <name>, one record per line. Additional
        <options> represent the attributes that will be output for each file in
        a tab-separated format. These attributes may be system attributes or
        any user-defined meta-data fields.
        The supported system attributes are:

        ppath:
        volumes:

        size:
        handle:
        btime:
        mtime:
        ino:
        the physical path of the file on the filesystem
        a blank separated list of the volumes where the file is saved
        the size of the saved file
        the handle as required by the RestoreSelection
        the backup time of the file
        the file's modification time
        the inode number of the file

        The index path returned by the inventory command cannot be used to
        access files on the file system in general. There are special cases
        where this might be used for this purpose, but generally it is not
        supported. The idea behind this info is to have an overview or idea
        what is being stored in the index and not to consume it in some other
        fashion (i.e. address the files on the file system to post-process
        them). In cases where files are still expected to be in the file system
        at the place they were at the point of archiving (for example somebody
        wants to delete them or otherwise post-process them) the ppath
        attribute may be used, which, when given on the command line, will
        yield the physical path as-found on the client where the file resides.
        Note that not all index entries have corresponding physical paths. In
        such cases the value will be set to empty.
        Return Values:
        -On Success:    the <client>:<output file>
        """
        method_name = "inventory"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, outputfile,
                                                options_list])

    def __repr__(self):
        return ": ".join([module_name, self.name])
