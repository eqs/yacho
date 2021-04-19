# -*- coding: utf-8 -*-
from dataclasses import dataclass
import toml


@dataclass
class SketchbookConfig:
    sketchbook_root: str = '.'
    base_url: str = '/'
    title: str = 'My Sketchbook'


@dataclass
class SketchConfig:
    title: str = ''
    draft: bool = True


def load_sketchbook_config(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)
    return SketchbookConfig(**data)


def load_sketch_config(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)
    return SketchConfig(**data)
