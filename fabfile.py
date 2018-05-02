from __future__ import unicode_literals

from fabric.api import env
import fh_fablib

env.box_project_name = 'mkweb'
env.box_domain = '406.ch'
env.box_database_local = '406_ch'
env.forward_agent = True

env.box_hardwired_environment = 'production'
env.box_environments = {
    'production': {
        'shortcut': 'p',
        'domain': '406.ch',
        'branch': 'master',
        'servers': [
            'www-data@feinheit06.nine.ch',
        ],
        'remote': 'production',
        'repository': '406',
        'database': '406_ch',
    },
}

fh_fablib.init(globals(), systemd=True)
