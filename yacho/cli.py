# -*- coding: utf-8 -*-
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
@click.option('-i', default='yacho.sketchbook.toml')
def build(i):
    cfg = load_sketchbook_config(i)
    build_site(cfg)


if __name__ == '__main__':
    cli()
