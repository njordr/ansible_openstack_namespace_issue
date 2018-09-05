import os
import openstack

import sys


def _create_connection_from_config(cloud_names=None, all_clouds=False):
    '''Connect to openstack using configuration from clouds.yaml
    Args:
        cloud_names (list): list of cloud names to connect to
        all_clluds (bool): True to connect too all the clouds in clouds.yaml (cloud_names will be ignored)
    Returns:
        Dict with connection objects (cloud name as key, connection object as value)
    '''
    connections = {}

    if all_clouds:
        try:
            config = openstack.config.loader.OpenStackConfig()
            clouds = config.get_cloud_names()
        except Exception:
            raise
    else:
        clouds = cloud_names

    for cloud in clouds:
        try:
            conn = openstack.connect(cloud=cloud)
            conn.authorize()
        except Exception as e:
            raise RuntimeError('Cannot connect to cloud {}. Error: {}. sys.path: {}'.format(cloud, e, sys.path))

        connections[cloud] = conn

    return connections


def _create_connection_from_creds(creds):
    '''Connect to openstack using credentials passed as parameters
    Args:
        creds (dict): credentials (see Examples below for the format)
    Returns:
        Dict with connection objects (cloud name as key, connection object as value)
    Examples:
        {
            'auth_url': 'https://ie2-osp10-lab.lab.betfair:13000/v3',
            'username': 'admin',
            'password': 'XXXXXXXXXX',
            'project_name': 'admin',
            'cloud': 'my_cloud', # this will be only use as key in the dictionary returned
        }
    '''
    connections = {}

    for cloud in creds:
        try:
            conn = openstack.connect(**cloud)
            conn.authorize()
        except Exception as e:
            sys.stderr.write('Cannot connect to cloud {}. Error: {}'.format(cloud, e))
            conn = None

        connections[cloud['cloud']] = conn

    return connections


def os_client(cloud_names=None, all_clouds=False, creds=None):
    '''Create one or more connections to openstack
    Args:
        cloud_names (list): the names of the cloud you want to connect to. If not specified as parameter, you can use environment var OS_CLOUD (if multiple names, comma separeted list) or set all_clouds to True to use all the clouds defined in clouds.yaml. If creds is used, the names will be used only as keys in the dictionary returned
        all_clouds (bool): True will use all the clouds defined in clouds.yaml file
        creds (list): list of credentials to connect to openstack (look at the Example section for a sample dict format). each cred dict will be use for the cloud at the same index in cloud_name

    Returns:
        dict with all the clouds and a connection object if the connection succed, otherwise None as connection object

    Example:
        This is an example of the creds list:
        [
            {
                'auth_url': 'https://ie2-osp10-lab.lab.betfair:13000/v3',
                'username': 'admin',
                'password': 'XXXXXXXXXX',
                'project_name': 'admin',
                'cloud': 'my_cloud', # this will be only use as key in the dictionary returned
            }
        ]
    '''
    if creds is None:
        if cloud_names is None and not all_clouds:
            try:
                cloud_names = os.environ['OS_CLOUD']
                cloud_names = cloud_names.split(',')
            except Exception:
                raise RuntimeError('Cloud name not defined. Please specify it as a parameter or set ENV var OS_CLOUD')

        try:
            client = _create_connection_from_config(cloud_names=cloud_names, all_clouds=all_clouds)
        except Exception:
            raise
    else:
        try:
            client = _create_connection_from_creds(creds=creds)
        except Exception:
            raise

    return client
