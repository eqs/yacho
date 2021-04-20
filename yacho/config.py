# -*- coding: utf-8 -*-
from typing import List
from dataclasses import dataclass, field
import toml


@dataclass
class SketchbookConfig:
    sketchbook_root: str = '.'
    base_url: str = '/'
    title: str = 'My Sketchbook'
    author: str = ''


@dataclass
class SketchConfig:
    title: str = ''
    draft: bool = True
    cover: str = ''
    images: List = field(default_factory=list)


def load_sketchbook_config(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)
    return SketchbookConfig(**data)


def load_sketch_config(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)
    return SketchConfig(**data)
