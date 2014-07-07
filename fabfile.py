import os
from fabric.api import cd, env, lcd, local, run, task


CONFIG = {
    'host': 'www-data@feinheit04.nine.ch',
    'project': 'mkweb',
    'branch': 'master',
}


CONFIG.update({
    'sass': '{project}/static/{project}'.format(**CONFIG),
    'service': '406.ch:*',
    'folder': '406.ch/',
})


env.forward_agent = True
env.hosts = [CONFIG['host']]


def _configure(fn):
    def _dec(string, *args, **kwargs):
        return fn(string.format(**CONFIG), *args, **kwargs)
    return _dec


local = _configure(local)
cd = _configure(cd)
lcd = _configure(lcd)
run = _configure(run)


@task
def install(req):
    if not os.path.isdir('venv'):
        if os.path.exists('venv'):
            print 'venv exists, but is not a folder. Aborting.'
            return

        local('virtualenv venv')

    local('venv/bin/pip install -r requirements/{}.txt'.format(req))


@task
def dev():
    import socket
    from threading import Thread
    jobs = [
        Thread(target=watch_styles),
        Thread(target=runserver),
    ]
    try:
        socket.create_connection(('localhost', 6379), timeout=0.1).close()
    except socket.error:
        jobs.append(Thread(target=lambda: local('redis-server')))
    [j.start() for j in jobs]
    [j.join() for j in jobs]


@task(alias='ws')
def watch_styles():
    with lcd('{sass}'):
        local('grunt')


@task(alias='rs')
def runserver(port=8038):
    local('venv/bin/python -Wall manage.py runserver 0.0.0.0:{}'.format(port))


@task
def deploy_styles():
    with lcd('{sass}'):
        local('grunt build')
    local('rsync -avz {sass}/css {host}:{folder}static/{project}/')
    local('rsync -avz {sass}/bower_components {host}:{folder}static/{project}/')


@task
def deploy_code():
    local('flake8 .')
    local('git push origin {branch}')
    with cd('{folder}'):
        run('git fetch')
        run('git reset --hard origin/{branch}')
        run('find . -name "*.pyc" -delete')
        run('venv/bin/pip install -r requirements/live.txt')
        run('venv/bin/python manage.py syncdb')
        run('venv/bin/python manage.py migrate')
        run('venv/bin/python manage.py collectstatic --noinput')
        run('sctl restart {service}')


@task
def deploy():
    deploy_styles()
    deploy_code()
