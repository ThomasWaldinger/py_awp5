# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

import functools


def resourcelist(input_list, resource_class, p5connection):
    result_list = []
    if len(input_list):
        for entry in input_list:
            if entry !="<empty>" and entry !="unknown":
                result_list.append(resource_class(entry, p5connection))
    return result_list


def strings(input_list):
    result=[]
    for entry in input_list:
        if entry:
            if type(entry) != list:
                result.append("{}".format(entry))
            else:
                result.extend(strings(entry))
    return result


def singlevalue(input_list):
    no_of_values = len(input_list)
    if no_of_values == 0:
        return ""
    if no_of_values == 1:
        return input_list[0]
    else:
        return " ".join(input_list)


def defaultIfNotSet(val, default):
    if val:
        return val
    else:
        return default


def onereturnvalue(func):
    @functools.wraps(func)
    def wrapper_return_first_value(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            no_of_values = len(result)
            if no_of_values == 0:
                return ""
            if no_of_values == 1:
                return result[0]
            if no_of_values > 1:
                nonstringvaluepresent = False
                for val in result:
                    if type(val) != str:
                        nonstringvaluepresent = True
                if not nonstringvaluepresent:
                    result = " ".join(result)
                    return result
        return result
    return wrapper_return_first_value
