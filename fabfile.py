from fabric.api import cd, env, local, run, task


env.forward_agent = True
env.hosts = ['406.ch']


@task
def deploy():
    local('git push origin master')
    with cd('/var/www/mk/406'):
        run('git checkout master')  # yes.
        run('git pull')
        run('find . -name "*.pyc" -delete')
        run('venv/bin/pip install -r requirements/live.txt')
        run('venv/bin/python manage.py migrate')
        run('venv/bin/python manage.py syncdb')
        with cd('mkweb/static/406'):
            run(
                'GEM_HOME=/home/mk/_gems/ /home/mk/_gems/bin/compass'
                ' compile -s compressed')
        run('venv/bin/python manage.py collectstatic --noinput')
        run('sudo supervisorctl restart mk_406')
