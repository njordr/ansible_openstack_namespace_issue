# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: os_assessment
short_description: This module will get info for hypervisors and VMs in an OpenStack estate
author:
    - "Giovanni Colapinto, giovanni.colapinto@paddypowerbetfair.com"
requirements:
    - "python >= 2.7.12"
    - "openstackdsk >= 0.17.2"

options:
    clouds:
        description:
            - name of the clouds to scan (it has to be a list also if it's a single name
        required: false
    all_clouds:
        description:
            - scan all clouds in clouds.yaml file
        required: false
    threads_nr:
        description:
            - number of thread to run for functionalities thread enabled
        required: false
'''

EXAMPLES = '''

- name: "Get OS Assessment"
  os_assessment:
    clouds:
        - ie2-osp10-inf
'''


from ansible.module_utils.os_client import os_client


class OSAssessment:
    def __init__(self):
        self._argument_spec = dict(
            clouds=dict(default=[], required=False, type='list'),
            all_clouds=dict(default=False, required=False, type='bool'),
            threads_nr=dict(default=10, required=False, type='int'),
        )
        self._module = AnsibleModule(argument_spec=self._argument_spec, supports_check_mode=False)

    def run_assessment(self):
        try:
            self._client = os_client(cloud_names=self._module.params.get('clouds'))
        except Exception as e:
            self._module.fail_json(msg='Cannot connect to openstack. Error: {}'.format(e))


def main():
    os_ass = OSAssessment()
    os_ass.run_assessment()


# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
