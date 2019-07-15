import time

import click
import logging
import sys

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
@click.option('--DISTRO', required=True)
@click.option('--MACHINE', required=True)
@click.option('--IMAGE', required=True)
@click.option('--local', default='./', help='images file destination', metavar='<string>')
def build(instance_id, project_root, distro, machine, image, local):
    try:
        ec2_instance = start_ec2(instance_id)

        host = ec2_instance.public_ip_address
        click.secho("Your EC2 IP: {}".format(host), fg='white', bold=True)

        _core = core.Core()
        con = _core.con(host)
        click.secho("Verifying connection to host", fg='white', bold=True)
        verify_connection(con)
        build_yocto(con=con, project_root=project_root, distro=distro, machine=machine, image=image)
        download_linux_images(con, local, image)

        stop_ec2(instance_id)

    except Exception as exc:
        click.secho("{}".format(exc), fg='red', bold=True)
        stop_ec2(instance_id)
        sys.exit(1)
    except KeyboardInterrupt as exc:
        click.secho("Oops. Good bye.".format(exc), fg='green', bold=True)
        stop_ec2(instance_id)
        sys.exit(1)


def build_yocto(con, project_root, distro, machine, image):
    click.secho('Working Dir: {}'.format(project_root))
    click.secho('Build linux images...')
    res = con.run(
        'cd {project_root} && DISTRO={DISTRO} MACHINE={MACHINE} source fsl-setup-release.sh -b build/ && bitbake {LINUX_IMAGE}'.format(
            project_root=project_root, DISTRO=distro, MACHINE=machine, LINUX_IMAGE=image))
    return res


def download_linux_images(con, local, image):
    con.run('cd {}'.format('./tmp/deploy/images'))
    click.secho('Download image...')
    con.get('{}.sdcard.bz2'.format(image), local)


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

    # Do a dryrun first to verify permissions
    ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
    waiter = ec2.get_waiter('instance_stopped')
    click.secho('Waiting for EC2 {} stopping'.format(instance_id))
    waiter.wait(InstanceIds=[instance_id])
    click.secho('Your EC2 stopped'.format(instance_id))


def verify_connection(con):
    con.run('hostname')
