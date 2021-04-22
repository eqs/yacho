# -*- coding: utf-8 -*-
import os
import click
from .config import load_sketchbook_config
from .build import build_site


@click.group()
def cli():
    pass


@cli.command()
def create():
    pass


@cli.command()
@click.option('-d', default='.', help='path to sketchbook dir')
def build(d):
    assert os.path.isdir(d)
    path = os.path.join(d, 'yacho.sketchbook.toml')
    cfg = load_sketchbook_config(path)
    build_site(cfg)


if __name__ == '__main__':
    cli()
