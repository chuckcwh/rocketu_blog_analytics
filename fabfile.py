from fabric.colors import green, yellow
from fabric.contrib.files import upload_template
from fabric.decorators import task
from fabric.operations import local
from fabric.api import *

env.hosts = ['54.187.17.251']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/blog_and_analytics.pem'
env.shell = "/bin/bash -l -i -c"
env.project_name = "rocketu_blog_analytics"

# @task
# def hello():
#     print(green("Hell ya"))
#
# @task
# def create_file(file_name):
#     local("touch ~/Desktop/{}.txt".format(file_name))
#
# @task
# def create_folder(path, file_name):
#     local("mkdir ~/{}/{}/".format(path, file_name))
#
# @task
# def ubuntu_hello():
#     with hide("stdout"):
#         output = run("lsb_release -a")
#         print(yellow(output))

def restart_app():
    sudo("service supervisor restart")
    sudo("service nginx restart")

@task
def deploy():
    with prefix("workon blog_analytics"):
        with cd("/home/ubuntu/rocketu_blog_analytics"):
            run("git pull origin master")
            run("pip install -r requirements.txt")
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")

    restart_app()

@task
def setup_postgres(database_name, password):
    sudo("adduser {}".format(database_name))
    sudo("apt-get install postgresql postgresql-contrib libpq-dev")

    with settings(sudo_user='postgres'):
        sudo("createuser {}".format(database_name))
        sudo("createdb {}".format(database_name))
        alter_user_statement = "ALTER USER {} WITH PASSWORD '{}';".format(database_name, password)
        sudo('psql -c "{}"'.format(alter_user_statement))

@task
def setup_nginx(project_name, server_name):
    upload_template("./deploy/nginx.conf",
                    "/etc/nginx/sites-enabled/{}.conf".format(project_name),
                    {'server_name': server_name},
                    use_sudo=True,
                    backup=False)

    restart_app()

@task
def setup_gunicorn(project_name):
    with prefix("workon blog_analytics"):
        with cd("/home/ubuntu/rocketu_blog_analytics"):
    # run("pip install gunicorn")
    # with cd("/home/ubuntu/{}".format(project_name)):
            upload_template("./deploy/gunicorn.conf.py",
                        "~/{}/gunicorn.conf.py".format(project_name),
                        use_sudo=True,
                        backup=False)




@task
def setup_supervisor(project_name):


    sudo("apt-get install supervisor")
    sudo("service supervisor restart")
    sudo("touch /etc/supervisor/conf.d/{}.conf".format(project_name))
    upload_template("./deploy/{}.conf".format(project_name),
                    "/etc/supervisor/conf.d/{}.conf".format(project_name),
                    use_sudo=True,
                    backup=False)

    restart_app()
