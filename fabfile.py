from fabric.api import task
from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import execute

from ade25.fabfiles import server
from ade25.fabfiles import project

from ade25.fabfiles import hotfix

env.use_ssh_config = True
env.forward_agent = True
env.port = '22222'
env.user = 'root'
env.hosts = ['z2']
env.webserver = '/opt/webserver/buildout.webserver'
env.code_root = '/opt/sites/msc/buildout.msc'
env.local_root = '/Users/sd/dev/msc/buildout.msc'
env.sitename = 'msc'
env.code_user = 'root'
env.prod_user = 'www'


@task
def deploy():
    """ Deploy current master to production server """
    project.site.update()
    project.site.restart()


@task
def deploy_full():
    """ Deploy current master to production and run buildout """
    project.site.update()
    project.site.build()
    project.site.restart()


@task
def rebuild():
    """ Deploy current master and run full buildout """
    project.site.update()
    project.site.build_full()
    project.site.restart()


@task
def get_data():
    """ Copy live database for local development """
    project.db.download_data()


@task
def bootstrap(site=None):
    """ Bootstrap project on target server """
    with cd('/opt/sites'):
        setup.generate_virtualenv(sitename='%s' % (env.sitename))
        run('git clone git@github.com:kreativkombinat/apc.git buildout.apc')
        run('cd buildout.apc; ../bin/python bootstrap.py -c deployment.cfg')
        run('cd buildout.apc; bin/buildout -c deployment.cfg')
