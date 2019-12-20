# -*- coding: utf-8 -*-
'''
Module to provide SAP CAL (cloud application library) functionality to Salt

.. versionadded:: pending

:maintainer:    Xabier Arbulu Insausti <xarbulu@suse.com>
:maturity:      alpha
:depends:       ``shaptools`` Python module
:platform:      all

:configuration: This module requires the shaptools python module
'''


# Import Python libs
from __future__ import absolute_import, unicode_literals, print_function
import time

from salt import exceptions

# Import third party libs
try:
    from shaptools import cal
    HAS_SAPCAL = True
except ImportError:  # pragma: no cover
    HAS_SAPCAL = False

__virtualname__ = 'sapcal'


def __virtual__():  # pragma: no cover
    '''
    Only load this module if shaptools python module is installed
    '''
    if HAS_SAPCAL:
        return __virtualname__
    return (
        False,
        'The sap cal execution module failed to load: the shaptools python'
        ' library is not available.')


def is_installed(
        software_path,
        root_user,
        root_password):
    '''
    Install SAP CAL instance

    software_path
        Path to the folder where the SAP CAL ins
    root_user
        Root user name
    root_password
        Root user password

    Returns:
        bool: True if installed, False otherwise

    CLI Example:

    .. code-block:: bash

        salt '*' sapcal.is_installed your_path root linux
    '''
    return cal.CalInstance.is_installed(software_path, root_user, root_password)


def install(
        software_path,
        sid_adm_password,
        root_user,
        root_password,
        force=False):
    '''
    Install SAP CAL instance

    software_path
        Path to the folder where the SAP CAL ins
    sid_adm_password
        sidadm user password (minimum 8 characters)
    root_user
        Root user name
    root_password
        Root user password
    force
        Force a new installation

    Returns:
        bool: True if installed, False otherwise

    CLI Example:

    .. code-block:: bash

        salt '*' sapcal.install your_path mypassword root linux
    '''
    try:
        return cal.CalInstance.install(
            software_path, sid_adm_password, root_user, root_password, force)
    except cal.CalExecutionError as err:
        raise exceptions.CommandExecutionError(err)
