# -*- coding: utf-8 -*-
import os
import glob
from jinja2 import Environment, PackageLoader

from .config import Config


class Sketch:
    def __init__(self, path: str):
        self.path = path

    @property
    def name(self):
        return os.path.split(self.path)[1]

    def get_pdes(self):
        p = os.path.join(self.path, '*.pde')
        return sorted(glob.glob(p))


def render_sketch_page(template, sketch):

    codes = []
    for pde in sketch.get_pdes():
        with open(pde, 'r') as f:
            code = f.read()
        codes.append(code)

    return template.render(
        page_title=sketch.name,
        imgs=[],
        codes=codes
    )


def build(cfg: Config):

    sketch_dirs = sorted(glob.glob(os.path.join(cfg.sketchbook_root, 'sketch_*')))
    sketches = [Sketch(sketch_dir) for sketch_dir in sketch_dirs]
    sketch = sketches[0]

    env = Environment(
        loader=PackageLoader('yacho'),
        trim_blocks=True
    )

    template_index = env.get_template('index.html')
    template_sketch_page = env.get_template('sketch_page.html')
    result_index = template_index.render(sketches=sketches)

    result_sketch_page = render_sketch_page(template_sketch_page, sketch)

    if not os.path.exists('dist'):
        os.mkdir('dist')

    with open('dist/index.html', 'w') as f:
        f.write(result_sketch_page)
