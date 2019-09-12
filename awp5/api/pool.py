# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Pool
This resource tracks volume pools. Volume pools are collections of labeled
media that can be used for archive and/or backup tasks.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.client import Client
from awp5.api.volume import Volume

module_name = "Pool"


def names(as_object=False, p5_connection=None):
    """
    Syntax: Pool names
    Description: Lists all configured media pools.
    Return Values:
    -On Success:    a list of pool names
                    the string "<empty>" if no pools have been configured
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if as_object is False:
        return result
    else:
        return resourcelist(result, Pool, p5_connection)


@onereturnvalue
def create(pool_name, option_value_list=None, as_object=False,
           p5_connection=None):
    """
    Syntax: Pool create <name> [<option> <value>]
    Description: Creates a media pool with the name <name>. The <name> of the
    pool may not include blanks or any special punctuation and/or national
    characters. If the pool <name> already exists in the P5 configuration an
    error will be thrown.
    Options supported by this command are:
    usage           one of Archive or Backup
    mediatype       one of TAPE or DISK
    blocksize       count 
    If no optional arguments are given, the newly created pool will be assigned
    Archive  for usage and TAPE for media type.
    The new option blocksize <count> allows to specify blocksize for all volumes
    labeled for this pool. The <count> parameter can be as low as 32768 (32K) 
    and as high as 524288 (512K) but it must be one of: 
    32768, 65536, 131072, 262144, 524288 
    The newly created pool will be configured for no parallelism i.e. it will
    use only one media-device for writing and/or reading the media. If you need
    to configure the pool for parallelism, please use the P5 Web-GUI.
    Example to create tape-archive media pool:
            Pool create MyPool usage Archive mediatype TAPE
    Return Values:
    -On Success:    the name of the created pool
    """
    method_name = "create"
    result = exec_nsdchat([module_name, method_name, pool_name,
                           option_value_list], p5_connection)
    if as_object is False:
        return result
    else:
        return resourcelist(result, Pool, p5_connection)


@onereturnvalue
def disabled(pool_name, p5_connection=None):
    """
    Syntax: Pool <name> disabled
    Description: Queries the pool Disabled status
    Return Values:
    -On Success:    the "1" (the pool is disabled) or "0" (not disabled)
    """
    method_name = "disabled"
    return exec_nsdchat([module_name, pool_name, method_name],
                        p5_connection)


@onereturnvalue
def drivecount(pool_name, count=None, p5_connection=None):
    """
    Syntax: Pool <name> drivecount <count>
    Description: Sets the drives per stream the pool is allowed to use
    Return Values:
    -On Success:    the drivecount as string
    """
    method_name = "drivecount"
    return exec_nsdchat([module_name, pool_name, method_name, count],
                        p5_connection)

                           
@onereturnvalue
def enabled(pool_name, p5_connection=None):
    """
    Syntax: Pool <name> enabled
    Description: Queries the pool Enabled status.
    Return Values:
    -On Success:    the string “1" (enabled) or "0" (not enabled)
    """
    method_name = "drivecount"
    return exec_nsdchat([module_name, pool_name, method_name], p5_connection)


@onereturnvalue
def mediatype(pool_name, p5_connection=None):
    """
    Syntax: Pool <name> mediatype
    Description: returns one of TAPE or DISK designating the media type of
    labeled volumes in the pool.
    Return Values:
    -On Success:    the media-type as a string
    """
    method_name = "mediatype"
    return exec_nsdchat([module_name, pool_name, method_name], p5_connection)


@onereturnvalue
def totalsize(pool_name, p5_connection=None):
    """
    Syntax: Pool <name> totalsize
    Description: Returns the estimated capacity for the pool <name> in kbytes.
    The true capacity is variable and depends on the wear and tear and the
    number of faulty blocks on the volume and degrades with time and usage.
    Return Values:
    -On Success:    the number of kbytes
    """
    method_name = "totalsize"
    return exec_nsdchat([module_name, pool_name, method_name], p5_connection)


@onereturnvalue
def usage(pool_name, p5_connection=None):
    """
    Syntax: Pool <name> usage
    Description: Returns either Archive or Backup
    Return Values:
    -On Success:    the usage as a string
    """
    method_name = "usage"
    return exec_nsdchat([module_name, pool_name, method_name], p5_connection)


@onereturnvalue
def usedsize(pool_name, p5_connection=None):
    """
    Syntax: Pool <name> usedsize
    Description: Returns the number of kbytes currently written to the pool
    <name>. If this method returns zero (0) then no data has been written to
    this pool.
    Return Values:
    -On Success:    the number of kbytes written
    """
    method_name = "usedsize"
    return exec_nsdchat([module_name, pool_name, method_name], p5_connection)


def volumes(pool_name, as_object=False, p5_connection=None):
    """
    Syntax: Pool <name> volumes
    Description: Lists all labeled volumes for the given pool
    Return Values:
    -On Success:    a list of volume ID's labeled for the named pool
                    the string "<empty>" if the pool has no volumes
    """
    method_name = "volumes"
    result = exec_nsdchat([module_name, pool_name, method_name],
                          p5_connection)
    if as_object is False:
        return result
    else:
        return resourcelist(result, Volume, p5_connection)


class Pool(P5Resource):
    def __init__(self, pool_name, p5_connection):
        super().__init__(pool_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: Pool names
        Description: Lists all configured media pools.
        Return Values:
        -On Success:    a list of pool names
                        the string "<empty>" if no pools have been configured
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if as_object is False:
            return result
        else:
            return resourcelist(result, Pool, p5_connection)

    @onereturnvalue
    def create(pool_name, option_value_list=None, as_object=False,
               p5_connection=None):
        """
        Syntax: Pool create <name> [<option> <value>]
        Description: Creates a media pool with the name <name>. The <name> of
        the pool may not include blanks or any special punctuation and/or
        national characters. If the pool <name> already exists in the P5
        configuration an error will be thrown.
        Options supported by this command are:
        usage           one of Archive or Backup
        mediatype       one of TAPE or DISK
        blocksize       count 
        If no optional arguments are given, the newly created pool will be
        assigned Archive  for usage and TAPE for media type.
        The new option blocksize <count> allows to specify blocksize for all 
        volumes labeled for this pool. The <count> parameter can be as low as 
        32768 (32K) and as high as 524288 (512K) but it must be one of: 
        32768, 65536, 131072, 262144, 524288 
        The newly created pool will be configured for no parallelism i.e. it
        will use only one media-device for writing and/or reading the media. If
        you need to configure the pool for parallelism, please use the P5
        Web-GUI.
        Example to create tape-archive media pool:
                Pool create MyPool usage Archive mediatype TAPE
        Return Values:
        -On Success:    the name of the created pool
        """
        method_name = "create"
        result = exec_nsdchat([module_name, method_name, pool_name,
                               option_value_list], p5_connection)
        if as_object is False:
            return result
        else:
            return resourcelist(result, Pool, p5_connection)

    @onereturnvalue
    def disabled(self):
        """
        Syntax: Pool <name> disabled
        Description: Queries the pool Disabled status
        Return Values:
        -On Success:    the "1" (the pool is disabled) or "0" (not disabled)
        """
        method_name = "disabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def drivecount(self, count=None):
        """
        Syntax: Pool <name> drivecount <count>
        Description: Sets the drives per stream the pool is allowed to use
        Return Values:
        -On Success:    the drivecount as string
        """
        method_name = "drivecount"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, count])

    @onereturnvalue
    def enabled(self):
        """
        Syntax: Pool <name> enabled
        Description: Queries the pool Enabled status.
        Return Values:
        -On Success:    the string “1" (enabled) or "0" (not enabled)
        """
        method_name = "enabled"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def mediatype(self):
        """
        Syntax: Pool <name> mediatype
        Description: returns one of TAPE or DISK designating the media type of
        labeled volumes in the pool.
        Return Values:
        -On Success:    the media-type as a string
        """
        method_name = "mediatype"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def totalsize(self):
        """
        Syntax: Pool <name> totalsize
        Description: Returns the estimated capacity for the pool <name> in
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
        Syntax: Pool <name> usage
        Description: Returns either Archive or Backup
        Return Values:
        -On Success:    the usage as a string
        """
        method_name = "usage"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def usedsize(self):
        """
        Syntax: Pool <name> usedsize
        Description: Returns the number of kbytes currently written to the pool
        <name>. If this method returns zero (0) then no data has been written
        to this pool.
        Return Values:
        -On Success:    the number of kbytes written
        """
        method_name = "usedsize"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def volumes(self, as_object=True):
        """
        Syntax: Pool <name> volumes
        Description: Lists all labeled volumes for the given pool
        Return Values:
        -On Success:    a list of volume ID's labeled for the named pool
                        the string "<empty>" if the pool has no volumes
        """
        method_name = "volumes"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                 method_name])
        if as_object is False:
            return result
        else:
            return resourcelist(result, Volume, self.p5_connection)

    def __repr__(self):
        return ": ".join([module_name, self.name])
