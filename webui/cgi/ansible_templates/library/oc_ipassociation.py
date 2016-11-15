#!/usr/bin/python
# Copyright (c) 2013, 2014-2016 Oracle and/or its affiliates. All rights reserved.

DOCUMENTATION = '''
---
module: oc_ipassociation
short_description: Short Desc
description:
    - Long Desc
version_added: ""
options:
    action:
        description:
            - Action to be executed against the oracle cloud object
        required: false
        default: list
        choices: ['create', 'list', 'update', 'delete']
    endpoint:
        description:
            - Oracle Cloud Endpoint
        required: true
        default: null
    user:
        description:
            - Oracle cloud user only required is cookie is not present.
        required: false
        default: null
    password:
        description:
            - Oracle cloud password only required is cookie is not present.
        required: false
        default: null
    cookie:
        description:
            - Oracle cloud authentication cookie.
        required: false
        default: null
    resourcename:
        description:
            - Resource name associated with object we are working with.
        required: false
        default: null
requirements: [oraclecomputecloud]
author: "Andrew Hopkinson (Oracle Cloud Solutions A-Team)"
notes:
    - Simple notes
...
'''

EXAMPLES = '''
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Eder Zechim (Exalogic A-Team)"
__copyright__ = "Copyright (c) 2013, 2014-2016  Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "oc_ipassociation"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import os
import sys

from oc.authenticate import authenticate
from oc.create_ip_association import createIPAssociation
from oc.list_ip_associations import listIPAssociations
from oc.delete_ip_association import deleteIPAssociation

# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action         = dict(default='list', choices=['create', 'list', 'update', 'delete']),
                    endpoint       = dict(required=True, type='str'),
                    user           = dict(required=False, type='str'),
                    password       = dict(required=False, type='str'),
                    cookie         = dict(required=False, type='str'),
                    resourcename   = dict(required=True, type='str'),
                    account        = dict(required=False, type='str'),
                    name           = dict(required=False, type='str'),
                    vcable         = dict(required=False, type='str'),
                    ip             = dict(required=False, type='str'),
                    parentpool     = dict(required=False, type='str'),
                    reservation    = dict(required=False, type='str')
            )
    )

    endpoint = module.params['endpoint']
    user = module.params['user']
    password = module.params['password']
    cookie = module.params['cookie']
    if cookie is None and user is not None and password is not None:
        cookie = authenticate(endpoint, user, password)
    resourcename = module.params['resourcename']
    account = module.params['account']
    name = module.params['name']
    vcable = module.params['vcable']
    ip = module.params['ip']
    parentpool = module.params['parentpool']
    reservation = module.params['reservation']

    if module.params['action'] == 'create':
        jsonobj = createIPAssociation(endpoint, resourcename, cookie, name, vcable, parentpool, reservation)
        module.exit_json(changed=True, list=jsonobj)
    elif module.params['action'] == 'list':
        jsonobj = listIPAssociations(endpoint, resourcename, cookie)
        module.exit_json(changed=True, list=jsonobj)
    elif module.params['action'] == 'delete':
        jsonobj = deleteIPAssociation(endpoint, resourcename, cookie)
        module.exit_json(changed=True, list=jsonobj)
    else:
        module.fail_json(msg="Unknown action")

    return


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *
# Main function to kick off processing
if __name__ == "__main__":
    main()
