# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
ArchiveEntry
The archive entry represents one archived file. It is an opaque handle which P5
uses to quickly locate the file on the archive media and it's metadata in the
archive index database.
The archive entry is generated for each file added to the archive selection.
Please see the ArchiveSelection resource description for details upon creation.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.archiveindex import ArchiveIndex
from awp5.api.client import Client

module_name = "ArchiveEntry"


@onereturnvalue
def handle(client, path, database=None, as_object=False, p5_connection=None):
    """
    Syntax: ArchiveEntry handle <client> <path> [<database>]
    Description: Returns the properly formatted archive entry handle which can
    be used for restoring files archived over the P5 web GUI.
    The <client> is the name of the P5 client where the <path> resides.
    The <path> is the absolute platform-native path to a file. No checking is
    performed on the file. If the passed <path> contains blanks, be sure to
    enclose it in curly braces: {/some/path with blanks/file}.
    Furthermore, if the <path> contains { and/or } chars themselves, you must
    escape them with a backslash '\' character.
    The optional <database> declares the name of the database where the file
    has been indexed. If omitted, the standard Default-Archive database is
    used. If no such database could be found in the current P5 configuration,
    an error is triggered.
    Return Values:
    -On Success:    the handle of the entry
    """
    method_name = "handle"
    result = exec_nsdchat([module_name, method_name, client, path, database],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, ArchiveEntry, p5_connection)


def btime(archiveentry_handle, p5_connection=None):
    """
    Syntax: ArchiveEntry <handle> btime
    Description: Returns the list of backup/archive times in seconds (Posix
    time) for each instance of the given archive entry.
    Return Values:
    -On Success:    the list of backup times
    """
    method_name = "btime"
    return exec_nsdchat([module_name, archiveentry_handle, method_name],
                        p5_connection)


def mtime(archiveentry_handle, p5_connection=None):
    """
    Syntax: ArchiveEntry <handle> mtime
    Description: Returns the list of modification times in seconds (Posix time)
    for each instance of the given archive entry.
    Return Values:
    -On Success:    the list of modification times
    """
    method_name = "mtime"
    return exec_nsdchat([module_name, archiveentry_handle, method_name],
                        p5_connection)


def meta(archiveentry_handle, key=None, p5_connection=None):
    """
    Syntax: ArchiveEntry <handle> meta [<key>]
    Description: Returns defined meta-data keys and their values for the given
    archive entry. If the optional <key> argument is given, it is assumed to be
    one of the meta columns defined for the particular index database where the
    archive entry has been indexed.
    Return Values:
    -On Success:    with <key> argument: the value of the given meta key
                    without <key> argument:
                    the list of all the meta keys and their values
    """
    method_name = "meta"
    return exec_nsdchat([module_name, archiveentry_handle, method_name,
                        key], p5_connection)


def setmeta(archiveentry_handle, key_value_list, p5_connection=None):
    """
    Syntax: ArchiveEntry <handle> setmeta [<key> <value> [<key> <value>].. ]
    Description: Sets the defined meta-data key/value pair for the given
    archive entry. Key argument is assumed to be one of the meta columns
    defined for the particular index database where the archive entry has been
    indexed.
    Return Values:
    -On Success:    the newly set key/value pair
    """
    method_name = "setmeta"
    return exec_nsdchat([module_name, archiveentry_handle, method_name,
                        key_value_list], p5_connection)


def size(archiveentry_handle, p5_connection=None):
    """
    Syntax: ArchiveEntry <handle> size
    Description: Returns the list of sizes in bytes for each instance of the
    given archive entry.
    Return Values:
    -On Success:    the list of file sizes
    """
    method_name = "size"
    return exec_nsdchat([module_name, archiveentry_handle, method_name],
                        p5_connection)


@onereturnvalue
def status(archiveentry_handle, p5_connection=None):
    """
    Syntax: ArchiveEntry <handle> status
    Description: Returns the status of the archived entry. An archive entry can
    have number of internal statuses, depending on the stage of the archive
    and/or restore process. Currently, the following statuses are supported:
        • indexed   found in the archive index
        • unknown   not found in the archive index
    The indexed status means that the entry has been processed (archived) and
    its meta data may be obtained from the index database.
    The unknown status means that the entry has not (yet) been found in the
    index, which is normal for files still waiting to be archived.
    If the status of an entry returns unknown, then all of the subsequent entry
    methods described below will return invalid values.
    Return Values:
    -On Success:    one of the supported statuses
    """
    method_name = "status"
    return exec_nsdchat([module_name, archiveentry_handle, method_name],
                        p5_connection)


def volume(archiveentry_handle, p5_connection):
    """
    Syntax: ArchiveEntry <handle> volume
    Description: Returns the media volume ID where the entry <name> has been
    archived. An entry can be stored on one or more volumes or even many times
    on the same volume (see the Volume resource for more information) during
    the archive operation, depending on the plan configuration.
    Return Values:
    -On Success:    the ID of the volume if the entry was stored on only
                    one volume,
                    or a list of volume ID's if the entry was stored on
                    multiple volumes
    """
    method_name = "volume"
    return exec_nsdchat([module_name, archiveentry_handle, method_name],
                        p5_connection)


@onereturnvalue
def clippath(archiveentry_handle, newpath=None, p5_connection=None):
    """
    Syntax: ArchiveEntry <handle> clippath [newpath]
    Description: If newpath is not given, the command will return the path of
    an existing clip or the string "unknown" if there is no clip available.
    If newpath is given as empty string "", it will clean/delete the previous
    clip (if any) and return the string "unknown" as a result.
    If newpath is given as a path to an existing file, this file will be set as
    the entry's clip. The file itself will be moved (not copied!) into the clip
    storage of the corresponding index and the absolute path of of the clip
    will be returned.
    Return Values:
    -On Success:    the path to the existing clip
                    or the string "unknown" if not found
    """
    method_name = "clippath"
    return exec_nsdchat([module_name, archiveentry_handle, method_name],
                        p5_connection)


@onereturnvalue
def clipurl(archiveentry_handle, host, port, p5_connection=None):
    """
    Syntax: ArchiveEntry <handle> clipurl <host> <port>
    Description: Returns a URL of the clip of the file as
         http://host:client/url-to-the-clip
    <host> and <port> refer to the host address and port of the P5 server host.
    Return Values:
    -On Success:    the URL as a string
    """
    method_name = "clipurl"
    return exec_nsdchat([module_name, archiveentry_handle, method_name, host,
                        port])


class ArchiveEntry(P5Resource):
    def __init__(self, archiveentry_name, p5_connection=None):
        super().__init__(archiveentry_name, p5_connection)

    @onereturnvalue
    def handle(client, path, database=None, as_object=True,
               p5_connection=None):
        """
        Syntax: ArchiveEntry handle <client> <path> [<database>]
        Description: Returns the properly formatted archive entry handle which
        can be used for restoring files archived over the P5 web GUI.
        The <client> is the name of the P5 client where the <path> resides.
        The <path> is the absolute platform-native path to a file. No checking
        is performed on the file. If the passed <path> contains blanks, be sure
        to enclose it in curly braces: {/some/path with blanks/file}.
        Furthermore, if the <path> contains { and/or } chars themselves, you
        must escape them with a backslash '\' character.
        The optional <database> declares the name of the database where the
        file has been indexed. If omitted, the standard Default-Archive
        database is used. If no such database could be found in the current P5
        configuration, an error is triggered.
        Return Values:
        -On Success:    the handle of the entry
        """
        method_name = "handle"
        result = exec_nsdchat([module_name, method_name, client, path,
                               database], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, ArchiveEntry, p5_connection)

    def btime(self):
        """
        Syntax: ArchiveEntry <handle> btime
        Description: Returns the list of backup/archive times in seconds (Posix
        time) for each instance of the given archive entry.
        Return Values:
        -On Success:    the list of backup times
        """
        method_name = "btime"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def mtime(self):
        """
        Syntax: ArchiveEntry <handle> mtime
        Description: Returns the list of modification times in seconds (Posix
        time) for each instance of the given archive entry.
        Return Values:
        -On Success:    the list of modification times
        """
        method_name = "mtime"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def meta(self, key=None):
        """
        Syntax: ArchiveEntry <handle> meta [<key>]
        Description: Returns defined meta-data keys and their values for the
        given archive entry. If the optional <key> argument is given, it is
        assumed to be one of the meta columns defined for the particular index
        database where the archive entry has been indexed.
        Return Values:
        -On Success:    with <key> argument: the value of the given meta key
                        without <key> argument:
                        the list of all the meta keys and their values
        """
        method_name = "meta"
        key_option = ""
        if key:
            key_option = key
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, key_option])

    def setmeta(self, key_value_list):
        """
        Syntax: ArchiveEntry <handle> setmeta [<key> <value> [<key> <value>]..]
        Description: Sets the defined meta-data key/value pair for the given
        archive entry. Key argument is assumed to be one of the meta columns
        defined for the particular index database where the archive entry has
        been indexed.
        Return Values:
        -On Success:    the newly set key/value pair
        """
        method_name = "setmeta"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, key_value_list])

    def size(self):
        """
        Syntax: ArchiveEntry <handle> size
        Description: Returns the list of sizes in bytes for each instance of
        the given archive entry.
        Return Values:
        -On Success:    the list of file sizes
        """
        method_name = "size"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def status(self):
        """
        Syntax: ArchiveEntry <handle> status
        Description: Returns the status of the archived entry. An archive entry
        can have number of internal statuses, depending on the stage of the
        archive and/or restore process. Currently, the following statuses are
        supported:
            • indexed   found in the archive index
            • unknown   not found in the archive index
        The indexed status means that the entry has been processed (archived)
        and its meta data may be obtained from the index database.
        The unknown status means that the entry has not (yet) been found in the
        index, which is normal for files still waiting to be archived.
        If the status of an entry returns unknown, then all of the subsequent
        entry methods described below will return invalid values.
        Return Values:
        -On Success:    one of the supported statuses
        """
        method_name = "status"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def volume(self):
        """
        Syntax: ArchiveEntry <handle> volume
        Description: Returns the media volume ID where the entry <name> has
        been archived. An entry can be stored on one or more volumes or even
        many times on the same volume (see the Volume resource for more
        information) during the archive operation, depending on the plan
        configuration.
        Return Values:
        -On Success:    the ID of the volume if the entry was stored on only
                        one volume,
                        or a list of volume ID's if the entry was stored on
                        multiple volumes
        """
        method_name = "volume"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def clippath(self, newpath=None):
        """
        Syntax: ArchiveEntry <handle> clippath [newpath]
        Description: If newpath is not given, the command will return the path
        of an existing clip or the string "unknown" if there is no clip
        available. If newpath is given as empty string "", it will clean/delete
        the previous clip (if any) and return the string "unknown" as a result.
        If newpath is given as a path to an existing file, this file will be
        set as the entry's clip. The file itself will be moved (not copied!)
        into the clip storage of the corresponding index and the absolute path
        of of the clip will be returned.
        Return Values:
        -On Success:    the path to the existing clip
                        or the string "unknown" if not found
        """
        method_name = "clippath"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, newpath])

    @onereturnvalue
    def clipurl(self, host, port):
        """
        Syntax: ArchiveEntry <handle> clipurl <host> <port>
        Description: Returns a URL of the clip of the file as
        http://host:client/url-to-the-clip
        <host> and <port> refer to the host address and port of the P5 server
        host.
        Return Values:
        -On Success:    the URL as a string
        """
        method_name = "clipurl"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, host, port])

    def __repr__(self):
        return ": ".join([module_name, self.name])
