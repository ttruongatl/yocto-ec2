# -*- coding: utf-8 -*-
import click
import logging
import ipaddress
from fabric import Connection
import sys
import os.path
from pkg_resources import resource_filename


class Core(object):
    def __init__(self, *args, **kwargs):
        self.connection = None
        self.host_key_file = os.path.expanduser('~/.ssh/id_rsa')
        return super().__init__(*args, **kwargs)

    def con(self, host):
        try:
            host = ipaddress.ip_address(host)
            host_connection_string = 'ubuntu@{host}'.format(host=host)

            click.secho('connecting to {}'.format(host_connection_string), fg='white', bold=True)

            with Connection(host_connection_string, connect_kwargs={"key_filename": self.host_key_file},
                            connect_timeout=30) as con:
                self.connection = con
                return con
        except Exception as exc:
            click.secho("{}".format(exc), fg='red', bold=True)
            sys.exit(1)
