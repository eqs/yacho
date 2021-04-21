# -*- coding: utf-8 -*-
from typing import List
from dataclasses import dataclass, field
import toml


@dataclass
class SocialConfig:
    home: str = ''
    twitter: str = ''
    github: str = ''
    instagram: str = ''
    youtube: str = ''
    facebook: str = ''


@dataclass
class SketchbookConfig:
    sketchbook_root: str = '.'
    base_url: str = '/'
    title: str = 'My Sketchbook'
    author: str = ''
    avatar: str = ''
    bio: str = ''
    custom_css: str = ''

    social: SocialConfig = field(default_factory=lambda: SocialConfig())


@dataclass
class SketchConfig:
    title: str = ''
    draft: bool = True
    cover: str = ''
    images: List = field(default_factory=list)
    comment: str = ''


def load_sketchbook_config(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)
    return SketchbookConfig(**data)


def load_sketch_config(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)
    return SketchConfig(**data)
