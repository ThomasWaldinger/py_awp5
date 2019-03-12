# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Device
This resource tracks tape devices, including single tape drives, tape drives
within a jukebox and drives in a virtual jukebox.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue
from awp5.api.volume import Volume

module_name = "Device"


def names(as_object=False, p5_connection=None):
    """
    Syntax: Device names
    Description: Returns a list of single tape device resources.
    Return Values:
    -On Success:    the list of device names
                    the string "<empty>" if no devices are configured
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Device, p5_connection)


@onereturnvalue
def cleaning(device_name, value=None, p5_connection=None):
    """
    Syntax: Device <name> cleaning [value]
    Description: Sets or returns the value of the device cleaning flag. If the
    optional argument value is specified, it will be used to set the value of
    the flag. The argument must be 1 or 0 to set the cleaning flag on or off.
    If the optional argument is not specified it will return the current value
    of the flag.
    Return Values:
    -On Success:    the string "1" or "0"
    """
    method_name = "cleaning"
    value_option = ""
    if value:
        if value is True:
            value_option = "1"
        else:
            value_option = "0"
    return exec_nsdchat([module_name, device_name, method_name, value_option],
                        p5_connection)


@onereturnvalue
def inventory(device_name, as_object=False, p5_connection=None):
    """
    Syntax: Device <name> inventory
    Description: Performs an inventory for the device <name>, effectively
    updating the internal volume database. Note that this is always a mount
    inventory, not a bar code inventory.
    Returns the name of the currently loaded volume
    Return Values:
    -On Success:    the volume name
    """
    method_name = "inventory"
    result = exec_nsdchat([module_name, device_name, method_name],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Volume, p5_connection)


class Device(P5Resource):
    def __init__(self, device_name, p5_connection=None):
        super().__init__(device_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: Device names
        Description: Returns a list of single tape device resources.
        Return Values:
        -On Success:    the list of device names
                        the string "<empty>" if no devices are configured
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Device, p5_connection)

    @onereturnvalue
    def cleaning(self, value=None):
        """
        Syntax: Device <name> cleaning [value]
        Description: Sets or returns the value of the device cleaning flag. If
        the optional argument value is specified, it will be used to set the
        value of the flag. The argument must be 1 or 0 to set the cleaning flag
        on or off. If the optional argument is not specified it will return the
        current value of the flag.
        Return Values:
        -On Success:    the string "1" or "0"
        """
        method_name = "cleaning"
        value_option = ""
        if value:
            if value is True:
                value_option = "1"
            else:
                value_option = "0"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, value_option])

    @onereturnvalue
    def inventory(self, as_object=True):
        """
        Syntax: Device <name> inventory
        Description: Performs an inventory for the device <name>, effectively
        updating the internal volume database. Note that this is always a mount
        inventory, not a bar code inventory.
        Returns the name of the currently loaded volume
        Return Values:
        -On Success:    the volume name
        """
        method_name = "inventory"
        result = self.p5_connection.nsdchat_call([module_name, self.name,
                                                  method_name])
        if not as_object:
            return result
        else:
            return resourcelist(result, Volume, self.p5_connection)

    def __repr__(self):
        return ": ".join([module_name, self.name])
