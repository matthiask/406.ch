from __future__ import print_function, unicode_literals

from fabric.api import env, execute, task
from fabric.contrib.project import rsync_project

from fabfile.config import local, cd, run


@task(default=True)
def deploy():
    local('flake8 .')
    execute('deploy.styles')
    execute('deploy.code')


@task
def styles():
    local('cd %(box_sass)s && grunt build')
    for part in ['bower_components', 'css']:
        rsync_project(
            local_dir='%(box_sass)s/%(part)s' % dict(env, part=part),
            remote_dir='%(box_domain)s/%(box_sass)s/' % env,
            delete=True,
            # upload=True,  # It's the default!
        )
    with cd('%(box_domain)s'):
        run('venv/bin/python manage.py collectstatic --noinput')


@task
def code():
    local('flake8 .')
    local('git push origin %(box_branch)s')
    with cd('%(box_domain)s'):
        run('git fetch')
        run('git reset --hard origin/%(box_branch)s')
        run('find . -name "*.pyc" -delete')
        run('venv/bin/pip install -r requirements/live.txt'
            ' --find-links file:///home/www-data/tmp/wheel/wheelhouse/')
        run('venv/bin/python manage.py migrate --noinput')
        run('venv/bin/python manage.py collectstatic --noinput')
        run('sctl restart %(box_domain)s:*')

    execute('versioning.fetch_live_remote')
