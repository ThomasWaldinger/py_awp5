# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Volume
This resource tracks volumes configured for data storage. A volume is an
instance of the physical media (tape, digital versatile disk, etc) prepared for
use by the P5 server. The preparation of media includes writing of the special
label on the beginning of media. By using this label, the P5 server can
uniquely identify the media in its volume database.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue

module_name = "Volume"


def names(as_object=False, p5_connection=None):
    """
    Syntax: Volume names
    Description: Returns a list of names of all volume resources
    Return Values:
    -On Success:    the list of volume names
                    the string "<empty>" if no volumes were configured
    """
    method_name = "names"
    str_list = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return str_list
    else:
        return resourcelist(str_list, Volume, p5_connection)


@onereturnvalue
def barcode(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> barcode
    Description: Returns the barcode of the volume <name>.
    Return Values:
    -On Success:    the barcode
                    the string "<empty>" if no barcode is present
    """
    method_name = "barcode"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def copyof(volume_name, p5_connection=None):
    """Syntax: Volume <name> copyof
    Description: Returns the volume name of the clone of this volume
    Return Values:
    -On Success:    the clone name or 0 (zero) if no clone exists
    """
    method_name = "copyof"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def dateexpires(volume_name, p5_connection=None):
    """Syntax: Volume <name> dateexpires
    Description: Returns the date when the volume will exxpire and can be
    relabeled in seconds since Jan 01, 1970 (Posix time).
    Return Values:
    -On Success:    the date in seconds (Posix time)
    """
    method_name = "dateexpires"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def dateused(volume_name, p5_connection=None):
    """Syntax: Volume <name> dateused
    Description: Returns the date when the volume was last used (for reading or
    for writing) in seconds since Jan 01, 1970 (Posix time).
    Return Values:
    -On Success:    the date in seconds (Posix time)
    """
    method_name = "dateused"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def disable(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> disable
    Description: Sets the volume to Disabled
    Return Values:
    -On Success:    the string "0"
    """
    method_name = "disable"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def disabled(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> disabled
    Description: Queries the volume Disabled status
    Return Values:
    -On Success:    the string "1" (the volume is disabled) or
                    the string "0" (not disabled)
    """
    method_name = "disabled"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def enabled(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> enabled
    Description: Queries the volume Enabled status.
    Return Values:
    -On Success:    the string "1" (enabled) or "0" (not enabled)
    """
    method_name = "enabled"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def enable(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> enable
    Description: Sets the volume to Enabled
    Return Values:
    -On Success:    the string "1"
    """
    method_name = "enable"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def isonline(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> isonline
    Description: Returns the string "1" if the volume is accessible, being
    either in the media changer or in one of the media drives.
    Return Values:
    -On Success:    the string "1"
    """
    method_name = "isonline"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def inventory(volume_name, outputfile, options=[],  p5_connection=None):
    """
    Syntax: Volume <name> inventory <output file> [<options>]
    Description: Outputs a list of the files contained on the Archive-Volume
    <name> into a file. The <output file> must be in the form
    client:absolute_path whereby client is the name of the P5 client where to
    store the file and absolute_path is the complete path to the file to hold
    the output. The client part is optional and defaults to localhost:
    The inventory command fills in the passed file with lines containing
    records separated by a TAB. If no <options> are given, the output file will
    by default contain the index paths of all the files saved by the given job
    <name>, one record per line. Additional <options> represent the attributes
    that will be output for each file in a tab-separated format. These
    attributes may be system attributes or any user-defined meta-data fields.

    Note: This command can only be applied to Archive tapes
    The supported system attributes are:

    ppath:
     size:
    handle:
    btime:
    mtime:
    ino:
    the physical path of the file on the filesystem
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
    delete them or otherwise post-process them) the  ppath attribute may be
    used, which, when given on the command line, will yield the physical path
    as-found on the client where the file resides. Note that not all index
    entries have corresponding physical paths. In such cases the value will be
    set to the string "<empty>".
    Return Values:
    -On Success:    the <client>:<output file>
    """
    method_name = "inventory"
    return exec_nsdchat([module_name, volume_name, method_name, outputfile,
                        options], p5_connection)


def jobs(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> jobs
    Description: Returns a list of job ids which accessed volume <name>
    The job ids can be used in a job command to get info about that job.
    Return Values:
    -On Success:    the job list
    """
    method_name = "jobs"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def label(volume_name, value="", p5_connection=None):
    """
    Syntax: Volume <name> label [<value>]
    Description: Returns a human-readable description of the volume <name>. If
    the optional argument <value> is given, it will set the label to the given
    value. If optional argument <value> contains spaces it should be inside
    {} braces
    Return Values:
    -On Success:    the volume label
    """
    method_name = "label"
    return exec_nsdchat([module_name, volume_name, method_name, value],
                        p5_connection)


@onereturnvalue
def location(volume_name, value="", p5_connection=None):
    """
    Syntax: Volume <name> location [<value>]
    Description: Returns the physical location of the volume <name>. If the
    optional argument <value> is given, it will set the offline location
    parameter to the given value. If optional argument <value> contains spaces
    it should be inside {} braces.
    The format of the location is passed as name-of-the-jukebox : slot
    Return Values:
    -On Success:    the location string
                    the string "<empty>" if the volume location is not set
    """
    method_name = "location"
    return exec_nsdchat([module_name, volume_name, method_name, value],
                        p5_connection)


@onereturnvalue
def mediatype(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> mediatype
    Description: Returns the type of media for the volume <name>. This is
    defined to be one of:
        - TAPE
        - DISK
        - OPTICAL
    Return Values:
    -On Success:    the media type
    """
    method_name = "mediatype"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def maxsize(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> maxsize
    Description: Returns the total number of kbytes which the volume <name> can
    hold.
    This is defined for the mediatype DISK. Other types of media, most notably
    TAPE do not have this size defined. If you attempt to get the maxsize of
    the TAPE media, you will get zero (0) as return value.
    Return Values:
    -On Success:    the size in kbytes
    """
    method_name = "maxsize"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def mode(volume_namle, value=None, p5_connection=None):
    """
    Syntax: Volume <name> mode [<value>]
    Description: Returns the current mode of the volume <name>. The mode can be
    one of:
        - Appendable
        - Closed
        - Readonly
        - Recyclable
        - Full
    If the optional argument <value> is given, it will set the mode to the
    given value.
    Return Values:
    -On Success:    the volume mode
    """
    method_name = "mode"
    return exec_nsdchat([module_name, volume_name, method_name, value],
                        p5_connection)


@onereturnvalue
def state(volume_name, value=None, p5_connection=None):
    """
    Syntax: Volume <name> state [<value>]
    Description: Returns the current state of the volume <name>. The state can
    be one of:
        - Ok
        - Suspect
        - OutOfSync
    If the optional argument <value> is given, it will set the state to the
    given value.
    Return Values:
    -On Success:    the volume state
    """
    method_name = "state"
    return exec_nsdchat([module_name, volume_name, method_name, value],
                        p5_connection)


@onereturnvalue
def totalsize(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> totalsize
    Description: Returns the estimated capacity for the volume <name> in
    kbytes. The true capacity is variable and depends on the wear and tear and
    the number of faulty blocks on the volume and degrades with time and usage.
    Return Values:
    -On Success:    the number of kbytes
    """
    method_name = "totalsize"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def usage(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> usage
    Description: Returns the current usage of the volume <name>. Currently, the
    following usage types are supported:
        - Archive   volume must be used for archive jobs
        - Backup    volume must be used for backup jobs
        - Import    volume is part of the imported media pool
    Return Values:
    -On Success:    the volume usage
    """
    method_name = "usage"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def usecount(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> usecount
    Description: Returns the number of uses for read and/or write operations.
    Return Values:
    -On Success:    the number of uses
    """
    method_name = "usecount"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


@onereturnvalue
def usedsize(volume_name, p5_connection=None):
    """
    Syntax: Volume <name> usedsize
    Description: Returns the number of kbytes currently written on the volume
    <name>. If this method returns zero (0) then no data has been written to
    this volume.
    Return Values:
    -On Success:    the number of kbytes written
    """
    method_name = "usedsize"
    return exec_nsdchat([module_name, volume_name, method_name], p5_connection)


class Volume(P5Resource):
    def __init__(self, volume_name, p5_connection=None):
        super().__init__(volume_name, p5_connection)

    @staticmethod
    def names(as_object=True, p5_connection=None):
        """
        Syntax: Volume names
        Description: Returns a list of names of all volume resources
        Return Values:
        -On Success:    the list of volume names
                        the string "<empty>" if no volumes were configured
        """
        method_name = "names"
        str_list = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return str_list
        else:
            return resourcelist(str_list, Volume, p5_connection)

    @onereturnvalue
    def barcode(self):
        """
        Syntax: Volume <name> barcode
        Description: Returns the barcode of the volume <name>.
        Return Values:
        -On Success:    the barcode
                        the string "<empty>" if no barcode is present
        """
        method_name = "barcode"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def copyof(self):
        """Syntax: Volume <name> copyof
        Description: Returns the volume name of the clone of this volume
        Return Values:
        -On Success:    the clone name or 0 (zero) if no clone exists
        """
        method_name = "copyof"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def dateexpires(self):
        """Syntax: Volume <name> dateexpires
        Description: Returns the date when the volume will exxpire and can be
        relabeled in seconds since Jan 01, 1970 (Posix time).
        Return Values:
        -On Success:    the date in seconds (Posix time)
        """
        method_name = "dateexpires"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])
                                                
    @onereturnvalue
    def dateused(self):
        """Syntax: Volume <name> dateused
        Description: Returns the date when the volume was last used (for
        reading or for writing) in seconds since Jan 01, 1970 (Posix time).
        Return Values:
        -On Success:    the date in seconds (Posix time)
        """
        method_name = "dateused"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disable(self):
        """
        Syntax: Volume <name> disable
        Description: Sets the volume to Disabled
        Return Values:
        -On Success:    the string "0"
        """
        method_name = "disable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def disabled(self):
        """
        Syntax: Volume <name> disabled
        Description: Queries the volume Disabled status
        Return Values:
        -On Success:    the string "1" (the volume is disabled) or
                        the string "0" (not disabled)
        """
        method_name = "disabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enabled(self):
        """
        Syntax: Volume <name> enabled
        Description: Queries the volume Enabled status.
        Return Values:
        -On Success:    the string "1" (enabled) or "0" (not enabled)
        """
        method_name = "enabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def enable(self):
        """
        Syntax: Volume <name> enable
        Description: Sets the volume to Enabled
        Return Values:
        -On Success:    the string "1"
        """
        method_name = "enable"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def isonline(self):
        """
        Syntax: Volume <name> isonline
        Description: Returns the string "1" if the volume is accessible, being
        either in the media changer or in one of the media drives.
        Return Values:
        -On Success:    the string "1"
        """
        method_name = "isonline"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def inventory(self, outputfile, options=None):
        """
        Syntax: Volume <name> inventory <output file> [<options>]
        Description: Outputs a list of the files contained on the
        Archive-Volume <name> into a file. The <output file> must be in the
        form client:absolute_path whereby client is the name of the P5 client
        where to store the file and absolute_path is the complete path to the
        file to hold the output. The client part is optional and defaults to
        localhost:
        The inventory command fills in the passed file with lines containing
        records separated by a TAB. If no <options> are given, the output file
        will by default contain the index paths of all the files saved by the
        given job <name>, one record per line. Additional <options> represent
        the attributes that will be output for each file in a tab-separated
        format. These attributes may be system attributes or any user-defined
        meta-data fields.

        Note: This command can only be applied to Archive tapes
        The supported system attributes are:

        ppath:
         size:
        handle:
        btime:
        mtime:
        ino:
        the physical path of the file on the filesystem
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
        them).
        In cases where files are still expected to be in the file system at the
        place they were at the point of archiving (for example somebody wants
        to delete them or otherwise post-process them) the  ppath attribute may
        be used, which, when given on the command line, will yield the physical
        path as-found on the client where the file resides. Note that not all
        index entries have corresponding physical paths. In such cases the
        value will be set to the string "<empty>".
        Return Values:
        -On Success:    the <client>:<output file>
        """
        method_name = "inventory"

        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, outputfile,
                                                options])

    def jobs(self):
        """
        Syntax: Volume <name> jobs
        Description: Returns a list of job ids which accessed volume <name>
        The job ids can be used in a job command to get info about that job.
        Return Values:
        -On Success:    the job list
        """
        method_name = "isonline"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def label(self, value=None):
        """
        Syntax: Volume <name> label [<value>]
        Description: Returns a human-readable description of the volume <name>.
        If the optional argument <value> is given, it will set the label to the
        given value. If optional argument <value> contains spaces it should be
        inside {} braces
        Return Values:
        -On Success:    the volume label
        """
        method_name = "label"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, value])

    @onereturnvalue
    def location(self, value=None):
        """
        Syntax: Volume <name> location [<value>]
        Description: Returns the physical location of the volume <name>. If the
        optional argument <value> is given, it will set the offline location
        parameter to the given value. If optional argument <value> contains
        spaces it should be inside {} braces.
        The format of the location is passed as name-of-the-jukebox : slot
        Return Values:
        -On Success:    the location string
                        the string "<empty>" if the volume location is not set
        """
        method_name = "location"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, value])

    @onereturnvalue
    def mediatype(self):
        """
        Syntax: Volume <name> mediatype
        Description: Returns the type of media for the volume <name>. This is
        defined to be one of:
            - TAPE
            - DISK
            - OPTICAL
        Return Values:
        -On Success:    the media type
        """
        method_name = "mediatype"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def maxsize(self):
        """
        Syntax: Volume <name> maxsize
        Description: Returns the total number of kbytes which the volume <name>
        can hold.
        This is defined for the mediatype DISK. Other types of media, most
        notably TAPE do not have this size defined. If you attempt to get the
        maxsize of the TAPE media, you will get zero (0) as return value.
        Return Values:
        -On Success:    the size in kbytes
        """
        method_name = "maxsize"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def mode(self, value=None):
        """
        Syntax: Volume <name> mode [<value>]
        Description: Returns the current mode of the volume <name>. The mode
        can be one of:
            - Appendable
            - Closed
            - Readonly
            - Recyclable
            - Full
        If the optional argument <value> is given, it will set the mode to the
        given value.
        Return Values:
        -On Success:    the volume mode
        """
        method_name = "mode"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, value])

    @onereturnvalue
    def state(self, value=None):
        """
        Syntax: Volume <name> state [<value>]
        Description: Returns the current state of the volume <name>. The state
        can be one of:
            - Ok
            - Suspect
            - OutOfSync
        If the optional argument <value> is given, it will set the state to the
        given value.
        Return Values:
        -On Success:    the volume state
        """
        method_name = "state"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, value])

    @onereturnvalue
    def totalsize(self):
        """
        Syntax: Volume <name> totalsize
        Description: Returns the estimated capacity for the volume <name> in
        kbytes. The true capacity is variable and depends on the wear and tear
        and the number of faulty blocks on the volume and degrades with time
        and usage.
        Return Values:
        -On Success:    the number of kbytes
        """
        method_name = "totalsize"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def usage(self):
        """
        Syntax: Volume <name> usage
        Description: Returns the current usage of the volume <name>. Currently,
        the following usage types are supported:
            - Archive   volume must be used for archive jobs
            - Backup    volume must be used for backup jobs
            - Import    volume is part of the imported media pool
        Return Values:
        -On Success:    the volume usage
        """
        method_name = "usage"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def usecount(self):
        """
        Syntax: Volume <name> usecount
        Description: Returns the number of uses for read and/or write
        operations.
        Return Values:
        -On Success:    the number of uses
        """
        method_name = "usecount"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def usedsize(self):
        """
        Syntax: Volume <name> usedsize
        Description: Returns the number of kbytes currently written on the
        volume <name>. If this method returns zero (0) then no data has been
        written to this volume.
        Return Values:
        -On Success:    the number of kbytes written
        """
        method_name = "usedsize"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def __repr__(self):
        return ": ".join([__class__.__name__, self.name])
