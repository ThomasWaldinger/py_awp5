# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
License Information
The returned resource names are internal names of license components that are
combined to form a product license.
A product license, like for instance a Backup Module AWB100, consists of
    1 BackupPlan: 	the Backup functionality
    1 Client: 		a Server Agent
    1 Device:		a Media Tape License for a single Tape Drive
The set of internal resources does not reflect the exact number or type of
installed licenses, it gives a summary of installed license resources.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue

module_name = "License"


def resources(as_object=False, p5_connection=None):
    """
    Syntax: License resources
    Description: Returns the list of names of all License resources
    Return Values:
    -On Success:    the list of names
    """
    method_name = "resources"
    str_list = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return str_list
    else:
        return resourcelist(str_list, LicenseResource, p5_connection)


@onereturnvalue
def free(resource_name, p5_connection=None):
    """
    Syntax: License <resource> free
    Description: For the given resource, returns whether there are free
    licenses available.
    Return Values:
    -On Success:    the string "-1" for unlimited free licenses
                    the string  "0" for no free license
                    or a positive count for the number of free licenses
    Note: Trial licenses and license resources that are not countable will
    return the string "-1", if available.
    """
    method_name = "free"
    return exec_nsdchat([module_name, resource_name, method_name],
                        p5_connection)


class LicenseResource(P5Resource):
    def __init__(self, resource_name, p5_connection=None):
        super().__init__(resource_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: License resources
        Description: Returns the list of names of all License resources
        Return Values:
        -On Success:    the list of names
        """
        method_name = "resources"
        str_list = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return str_list
        else:
            return resourcelist(str_list, LicenseResource, p5_connection)

    @onereturnvalue
    def free(self):
        """
        Syntax: License <resource> free
        Description: For the given resource, returns whether there are free
        licenses available.
        Return Values:
        -On Success:    the string "-1" for unlimited free licenses
                        the string  "0" for no free license
                        or a positive count for the number of free licenses
        Note: Trial licenses and license resources that are not countable will
        return the string "-1", if available.
        """
        method_name = "free"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                               method_name])

    def __repr__(self):
        return ": ".join([__class__.__name__, self.name])
