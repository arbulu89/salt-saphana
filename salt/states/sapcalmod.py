# -*- coding: utf-8 -*-
'''
State module to provide SAP CAL functionality to Salt

.. versionadded:: pending

:maintainer:    Xabier Arbulu Insausti <xarbulu@suse.com>
:maturity:      alpha
:depends:       python-shaptools
:platform:      all

:configuration: This module requires the python-shaptools module

:usage:

.. code-block:: yaml
    sap-cal-install:
      sapcal.installed:
        - software_path: '/root/sap_inst/51052481'
        - sid_adm_password: 'Qwerty1234'
        - root_user: 'root'
        - root_password: 's'
        - force: True
'''


# Import python libs
from __future__ import absolute_import, unicode_literals, print_function


# Import salt libs
from salt import exceptions
from salt.ext import six


__virtualname__ = 'sapcal'


def __virtual__():  # pragma: no cover
    '''
    Only load if the sap cal module is in __salt__
    '''
    return 'sapcal.is_installed' in __salt__


def is_installed(
        name,
        sid_adm_password,
        root_user,
        root_password,
        force=False):
    '''
    Install SAP CAL instance in the machine

    name:
        Path of the folder where the SAP CAL installation software is located
    sid_adm_password:
        sidadm password
    root_user:
        root user name
    root_password:
        Password of the root user
    force:
        Force a new installation
    '''
    software_path = name

    ret = {'name': '{}'.format(software_path),
           'changes': {},
           'result': False,
           'comment': ''}

    result = __salt__['sapcal.is_installed'](
        software_path=software_path,
        root_user=root_user,
        root_password=root_password)

    if result and not force:
        ret['result'] = True
        ret['comment'] = 'SAP instance is already installed'
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'SAP instance would be installed'
        return ret

    try:
        __salt__['sapcal.install'](
            software_path=software_path,
            sid_adm_password=sid_adm_password,
            root_user=root_user,
            root_password=root_password,
            force=force)
    except exceptions.CommandExecutionError as err:
        ret['comment'] = six.text_type(err)
        return ret

    ret['result'] = True
    ret['comment'] = 'SAP instance is available{}'.format(
        ' (reinstallation forced)' if force else '')

    return ret
