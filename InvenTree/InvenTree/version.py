""" Version information for InvenTree.
Provides information on the current InvenTree version
"""

import subprocess
import django
import re

import common.models


INVENTREE_SW_VERSION = "0.1.8 pre"

# Increment this number whenever there is a significant change to the API that any clients need to know about
INVENTREE_API_VERSION = 2


def inventreeInstanceName():
    """ Returns the InstanceName settings for the current database """
    return common.models.InvenTreeSetting.get_setting("INVENTREE_INSTANCE", "")


def inventreeVersion():
    """ Returns the InvenTree version string """
    return INVENTREE_SW_VERSION


def inventreeVersionTuple():
    """ Return the InvenTree version string as (maj, min, sub) tuple """

    match = re.match(r"^.*(\d+)\.(\d+)\.(\d+).*$", INVENTREE_SW_VERSION)

    return [int(g) for g in match.groups()]


def versionTupleToInt(version):
    """
    Convert a version tuple (x, y, z) to an integer.
    This simple integer can then be used for direct version comparison
    """

    n = version[0] * 1000 * 1000
    n += version[1] * 1000
    n += version[2]

    return n
    

def inventreeApiVersion():
    return INVENTREE_API_VERSION


def inventreeDjangoVersion():
    """ Return the version of Django library """
    return django.get_version()


def inventreeCommitHash():
    """ Returns the git commit hash for the running codebase """

    try:
        return str(subprocess.check_output('git rev-parse --short HEAD'.split()), 'utf-8').strip()
    except FileNotFoundError:
        return None


def inventreeCommitDate():
    """ Returns the git commit date for the running codebase """

    try:
        d = str(subprocess.check_output('git show -s --format=%ci'.split()), 'utf-8').strip()
        return d.split(' ')[0]
    except FileNotFoundError:
        return None
