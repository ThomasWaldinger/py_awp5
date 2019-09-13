# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Jukebox
This resource tracks jukeboxes configured for data storage. Currently you do
not have much control over jukeboxes, except for getting the list of currently
loaded volumes, resetting the jukebox and performing a bar code or mount
inventory. Future versions of CLI will allow you to control jukebox resources
in a more advanced way.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.volume import Volume
from awp5.api.job import Job

module_name = "Jukebox"


def names(as_object=False, p5_connection=None):
    """
    Syntax: Jukebox names
    Description: Returns a list of names of all jukebox resources
    Return Values:
    -On Success:    list of jukebox names
                    the string "<empty>" If no jukeboxes are configured
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Jukebox, p5_connection)


@onereturnvalue
def inventory(jukebox_name, barcode=True, startSlot=None, endSlot=None,
              as_object=False, p5_connection=None):
    """
    Syntax: Jukebox <name> inventory [-barcode [<startSlot> [<endSlot>]]]
    Description: Performs an inventory of the jukebox <name>, effectively
    updating the internal volume database.
    If the optional -barcode argument is specified, it attempts a bar code
    inventory. If not, a mount inventory of the jukebox is scheduled.
    If the optional <startSlot> argument is given it is taken as the first slot
    for the inventory job. Otherwise, the first configured slot of the jukebox
    is taken. If the optional <endSlot> argument is given, it is taken as the
    last slot for the inventory job. Otherwise, the last configured slot of the
    jukebox is taken.
    Return Values:
    -On Success:    the job ID of the scheduled inventory job
    """
    method_name = "inventory"
    barcode_option = ""
    startSlot_option = ""
    endSlot_option = ""
    if barcode is True:
        barcode_option = "-barcode"
    if endSlot:
        if not startSlot:
            endSlot = None
    result = exec_nsdchat([module_name, jukebox_name, method_name,
                           barcode_option, startSlot, endSlot],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def label(jukebox_name, pool, slotid, as_object=False, p5_connection=None):
    """
    Syntax: Jukebox <name> label <pool> <slotID1> [<slotID2> … [<slotIDx>]]
    Description: Labels media in the given jukebox for the given POOL starting
    with slotID1, optionally including all of the slotIDs given on the command
    line. Example: Jukebox changer0  label My-Archive 1 5 9
    this command will label the volumes in slots 1, 5 and 9 for pool MyArchive.
    Note that only new/empty volumes can be labeled with this  command.
    Use the Job .. commands to monitor the ongoing label job.
    Return values: 
    -On Success:    the job Id of the label job 
    """
    method_name = "slotcount"
    result = exec_nsdchat([module_name, jukebox_name, method_name, pool,
                                  slotid], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def slotcount(jukebox_name, p5_connection=None):
    """
    Syntax: Jukebox <name> slotcount 
    Description: Returns number of media slots in the given jukebox. The slots
    in the Jukebox are addressed as 1 ... slotcount.
    Return Values:
    -On Success:    the number of media slots 
    """
    method_name = "slotcount"
    return exec_nsdchat([module_name, jukebox_name, method_name],
                        p5_connection)


@onereturnvalue
def reset(jukebox_name, p5_connection=None):
    """
    Syntax: Jukebox <name> reset
    Description: Performs a hardware jukebox reset, with forcefully emptying
    all jukebox drives. Use this method with caution since this command will
    perform an unconditional jukebox reset regardless of any jobs that may be
    using the jukebox resources.
    Return Values:
    -On Success:    the string "1"
    """
    method_name = "reset"
    return exec_nsdchat([module_name, jukebox_name, method_name],
                        p5_connection)


def volumes(jukebox_name, slot_id=[], as_object=False, p5_connection=None):
    """
    Syntax: Jukebox <name> volumes
    Description: Returns a list of all volumes currently loaded in the <name>
    jukebox. To update the list of the volumes in the jukebox, use the
    inventory method.
    Return Values:
    -On Success:    the list of volume names
    """
    method_name = "volumes"
    result = exec_nsdchat([module_name, jukebox_name, method_name, slot_id],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Volume, p5connection)


class Jukebox(P5Resource):
    def __init__(self, jukebox_name, p5_connection=None):
        super().__init__(jukebox_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: Jukebox names
        Description: Returns a list of names of all jukebox resources
        Return Values:
        -On Success:    list of jukebox names
                        the string "<empty>" If no jukeboxes are configured
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Jukebox, p5_connection)

    @onereturnvalue
    def inventory(self, barcode=True, startSlot=None, endSlot=None,
                  as_object=True):
        """
        Syntax: Jukebox <name> inventory [-barcode [<startSlot> [<endSlot>]]]
        Description: Performs an inventory of the jukebox <name>, effectively
        updating the internal volume database.
        If the optional -barcode argument is specified, it attempts a bar code
        inventory. If not, a mount inventory of the jukebox is scheduled.
        If the optional <startSlot> argument is given it is taken as the first
        slot for the inventory job. Otherwise, the first configured slot of the
        jukebox is taken. If the optional <endSlot> argument is given, it is
        taken as the last slot for the inventory job. Otherwise, the last
        configured slot of the jukebox is taken.
        Return Values:
        -On Success:    the job ID of the scheduled inventory job
        """
        method_name = "inventory"
        barcode_option = ""
        startSlot_option = ""
        endSlot_option = ""
        if barcode is True:
            barcode_option = "-barcode"
        if endSlot:
            if not startSlot:
                endSlot = None
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, barcode_option,
                                                  startSlot_option,
                                                  endSlot_option])
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, self.p5_connection)

@onereturnvalue
def label(self, pool, slotid, as_object=True):
    """
    Syntax: Jukebox <name> label <pool> <slotID1> [<slotID2> … [<slotIDx>]]
    Description: Labels media in the given jukebox for the given POOL starting
    with slotID1, optionally including all of the slotIDs given on the command
    line. Example: Jukebox changer0  label My-Archive 1 5 9
    this command will label the volumes in slots 1, 5 and 9 for pool MyArchive.
    Note that only new/empty volumes can be labeled with this  command.
    Use the Job .. commands to monitor the ongoing label job.
    Return values: 
    -On Success:    the job Id of the label job 
    """
    method_name = "slotcount"
    result = self.p5_connection.nsdchat_call([module_name, self.name, 
                                                     method_name, pool, slotid])
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)

    @onereturnvalue
    def slotcount(jukebox_name):
        """
        Syntax: Jukebox <name> slotcount 
        Description: Returns number of media slots in the given jukebox. The 
        slots in the Jukebox are addressed as 1 ... slotcount.
        Return Values:
        -On Success:    the number of media slots 
        """
        method_name = "slotcount"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def reset(self):
        """
        Syntax: Jukebox <name> reset
        Description: Performs a hardware jukebox reset, with forcefully
        emptying all jukebox drives. Use this method with caution since this
        command will perform an unconditional jukebox reset regardless of any
        jobs that may be using the jukebox resources.
        Return Values:
        -On Success:    the string "1"
        """
        method_name = "reset"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def volumes(self, slot_id=[], as_object=True):
        """
        Syntax: Jukebox <name> volumes
        Description: Returns a list of all volumes currently loaded in the
        <name> jukebox. To update the list of the volumes in the jukebox, use
        the inventory method.
        Return Values:
        -On Success:    the list of volume names
        """
        method_name = "volumes"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name, slot_id])
        if not as_object:
            return result
        else:
            return resourcelist(result, Volume, self.p5_connection)

    def __repr__(self):
        return ": ".join([module_name, self.name])
