# -*- coding: utf-8 -*-
import os
from typing import List
from dataclasses import dataclass, field
from enum import Enum
import toml


@dataclass
class SocialConfig:
    home: str = ''
    twitter: str = ''
    github: str = ''
    instagram: str = ''
    youtube: str = ''
    facebook: str = ''


class VideoType(Enum):
    none = 0
    youtube = 1
    vimeo = 2
    neort = 3
    gif = 4

    @staticmethod
    def get_embed_code(video_type, id_):
        if video_type.name == 'none':
            return ''
        elif video_type.name == 'youtube':
            return f'''<div class="youtube-embed"><iframe \
width="560" height="315" \
src="https://www.youtube.com/embed/{id_}" \
title="YouTube video player" frameborder="0" \
allow="accelerometer; autoplay; clipboard-write; encrypted-media; \
gyroscope; picture-in-picture" allowfullscreen></iframe></div>'''

        elif video_type.name == 'vimeo':
            return f'''<div class="vimeo-embed">\
<iframe src="https://player.vimeo.com/video/{id_}?loop=1" \
style="position:absolute;top:0;left:0;width:100%;height:100%;" \
frameborder="0" allow="autoplay; fullscreen; picture-in-picture" \
allowfullscreen></iframe>\
</div>'''
        elif video_type.name == 'neort':
            return f'''<div class="neort-embed">
<iframe src="https://neort.io/embed/{id_}?autoStart=true&\
quality=1&info=true" \
frameborder="0" sandbox="allow-forms allow-modals allow-pointer-lock \
allow-popups allow-same-origin allow-scripts" \
allow="geolocation; microphone; camera; midi; vr" \
allowfullscreen="true" allowtransparency="true"></iframe>\
</div>'''
        elif video_type.name == 'gif':
            filename = os.path.split(id_)[1]
            return f'<div class="gif-embed"><img src="gifs/{filename}"></div>'
        else:
            raise RuntimeError()


@dataclass
class VideoConfig:
    type: VideoType = field(default_factory=lambda: VideoType.none)
    id: str = ''


@dataclass
class CodeInfo:
    filepath: str
    code: str

    @property
    def filename(self):
        return os.path.split(self.filepath)[1]

    @property
    def ext(self):
        return os.path.splitext(self.filepath)[1]

    @property
    def lang(self):
        if self.ext in ['.pde', '.java']:
            return 'java'
        elif self.ext in ['.js']:
            return 'js'
        elif self.ext in ['.html']:
            return 'html'
        elif self.ext in ['.c', '.cpp', '.h', '.hpp']:
            return 'cpp'
        elif self.ext in ['.glsl']:
            return 'glsl'
        elif self.ext in ['.py']:
            return 'python'
        else:
            return 'plaintext'


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

    video: VideoConfig = field(default_factory=lambda: VideoConfig())
    public: List[str] = field(default_factory=lambda: [
        '*.pde', 'sketch.js', '*.py'
    ])


def load_sketchbook_config(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)

    if 'social' in data:
        data.update({'social': SocialConfig(**data['social'])})

    return SketchbookConfig(**data)


def load_sketch_config(path: str):
    with open(path, 'r') as f:
        data = toml.load(f)

    if 'video' in data:
        data.update({'video': VideoConfig(
            type=VideoType[data['video']['type']],
            id=data['video']['id']
        )})

    return SketchConfig(**data)
