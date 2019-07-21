import time

import click
import logging
import sys
import os

from .. import core
import boto3

ec2 = boto3.client('ec2')

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command('build', help='Build Yocto project in EC2')
@click.option('--instance-id', required=True)
@click.option('--project-root', required=True)
@click.option('--script-path', required=True)
@click.option('--sdcard-image', required=True)
@click.option('--local', default='./', help='images file destination', metavar='<string>')
def build(instance_id, project_root, script_path, sdcard_image, local):
    try:
        project_root = project_root.rstrip('\\')

        ec2_instance = start_ec2(instance_id)

        host = ec2_instance.public_ip_address
        click.secho("Your EC2 IP: {}".format(host), fg='white', bold=True)

        _core = core.Core()
        con = _core.con(host)
        click.secho("Verifying connection to host", fg='white', bold=True)
        verify_connection(con)
        build_yocto(con=con, project_root=project_root, script_path=script_path)
        download_linux_images(con=con, local=local, image_file=sdcard_image)
    except Exception as exc:
        click.secho("{}".format(exc), fg='red', bold=True)
    except KeyboardInterrupt as exc:
        click.secho("Oops. Good bye.".format(exc), fg='green', bold=True)
    finally:
        stop_ec2(instance_id)
        sys.exit(1)


def build_yocto(con, project_root, script_path):
    click.secho('Working Dir: {}'.format(project_root))
def build_yocto(con, project_dir, script_path):
    click.secho('Working Dir: {}'.format(project_dir))
    click.secho('Build linux images...')
    click.secho('Copy {} to {}'.format(script_path, project_dir))
    con.put(script_path, '{}/build_script.sh'.format(project_dir))
    click.secho('RUN the build script...')
    con.run(
        'cd {project_dir} && chmod a+x build_script.sh && source build_script.sh'.format(project_dir=project_dir))


def download_linux_images(con, local, image_file):
    click.secho('Download image...')
    head, tail = os.path.split(image_file)
    local_file = '{}/{}'.format(local, tail)
    con.get('{}'.format(image_file), local_file)
    click.secho('You can checkout the image at {}'.format(local_file))


def download_project_tarball(con, local, project_dir):
    click.secho('Create project tarball...')
    head, dir_name = os.path.split(project_dir)
    tar_file = {dir_name}.tar.gz
    con.run('tar -czvf {tar_file} {project_dir}'.format(tar_file=tar_file, project_dir=project_dir))

    click.secho('Download the tarball...')
    local_file = '{}/{}'.format(local, tar_file)
    con.get('{tar_file}'.format(tar_file), local_file)
    click.secho('Done.')


def start_ec2(instance_id):
    click.secho('Start your EC2: {} ...'.format(instance_id))

    ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
    waiter = ec2.get_waiter('instance_status_ok')

    click.secho('Waiting for EC2 {} running'.format(instance_id))
    waiter.wait(InstanceIds=[instance_id])
    click.secho('Your EC2 is ready'.format(instance_id))

    client = boto3.resource('ec2')
    instance = client.Instance(id=instance_id)

    return instance


def stop_ec2(instance_id):
    click.secho('Stop your EC2: {} ...'.format(instance_id))
    ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
    waiter = ec2.get_waiter('instance_stopped')
    click.secho('Waiting for EC2 {} stopping'.format(instance_id))
    waiter.wait(InstanceIds=[instance_id])
    click.secho('Your EC2 stopped'.format(instance_id))


def verify_connection(con):
    con.run('hostname')
