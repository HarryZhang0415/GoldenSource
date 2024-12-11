import os
import socket

def identity(v):
    """
    Identity conversion function.

    :param v: A value
    :return: The value
    """
    return v

def env_get(*args, **kwargs):
    """
    Tried to get the environment variables passed in sequence and returns the first hit.
    The value is then converted using what is defined in the as_type argument
    If nothing is found, the default argument is returned.
    :param args: the environment variables to try, in order
    :param kwargs:
        as_type: conversion function applied to the value found
        default: the default value returned if nothing is found, empty string otherwise
    :return: The optionally converted environment variable if found, or the default value of provided, or an empty string
    """
    for var in args:
        val = os.environ.get(var)
        if val is not None:
            convert = kwargs.get('as_type', identity)
            return convert(val)
    return kwargs.get('default', '')

def get_host():
    DEV_PREFIX = ['dev1', 'dev2', 'dev3']
    UAT_PREFIX = ['uat1', 'uat2', 'uat3']
    PROD_PREFIX = ['prod1', 'prod2', 'prod3']

    hostname = socket.gethostname().lower()

    if any(prefix in hostname for prefix in PROD_PREFIX):
        return "PROD"
    elif any(prefix in hostname for prefix in UAT_PREFIX):
        return "UAT"
    elif any(prefix in hostname for prefix in DEV_PREFIX):
        return "DEV"
    else:
        return "DEV"