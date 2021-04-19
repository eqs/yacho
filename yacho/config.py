# -*- coding: utf-8 -*-
from dataclasses import dataclass
import toml


@dataclass
class Config:
    sketchbook_root: str
    base_url: str


def load_toml(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)
    return Config(
        sketchbook_root=data['sketchbook_root'],
        base_url=data['base_url']
    )
