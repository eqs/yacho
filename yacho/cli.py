# -*- coding: utf-8 -*-
import click
from .config import load_toml
from .build import build


@click.command()
@click.argument('path')
def main(path):
    cfg = load_toml(path)
    build(cfg)


if __name__ == '__main__':
    main()
