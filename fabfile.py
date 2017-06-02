"""
This file contains the configuration for the fabric scripts.
The scripts support multiple environments.

Within the fabric commands string formatting is applied with the env object
as argument.

The environment specific values are available as box_<key>
e.g. '%(box_branch)s'.

Usage::
    run('git clone -b %(box_branch)s %(box_repository_url)s %(box_domain)s')
"""

from __future__ import unicode_literals

from fabric.api import env
import fh_fablib

# env.box_environment contains the currently active environment.

# Default values available in all environments
env.box_project_name = 'mkweb'
env.box_domain = '406.ch'
env.box_database_local = '406_ch'
env.box_staticfiles = '%(box_project_name)s/static/%(box_project_name)s' % env
env.box_static_src = env.box_staticfiles
env.box_python = 'python3'
env.forward_agent = True

# Remove this for multi-env support
env.box_hardwired_environment = 'production'

# Environment specific values.
env.box_environments = {
    'production': {
        'shortcut': 'p',
        'domain': '406.ch',
        'branch': 'master',
        'servers': [
            'www-data@feinheit06.nine.ch',
        ],
        'remote': 'production',  # git remote alias for the server.
        'repository': '406',
        'database': '406_ch',
    },
    'staging': {
        'shortcut': 's',
        'domain': 'stage.fcz.ch',
        'branch': 'develop',
        'servers': [
            'www-data@feinheit04.nine.ch',
        ],
        'remote': 'staging',
        'repository': 'fcz_ch',
        'database': 'stage_fcz_ch',
    },
}


fh_fablib.init(globals())
