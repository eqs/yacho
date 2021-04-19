# -*- coding: utf-8 -*-
import os
import glob
import logging
from jinja2 import Environment, PackageLoader

from .config import (
    load_sketch_config, SketchbookConfig
)


class Sketch:
    def __init__(self, path: str):

        self.path = path

        if self.has_config():
            self.cfg = load_sketch_config(
                os.path.join(self.path, 'yacho.sketch.toml')
            )
        else:
            self.cfg = None

    @property
    def name(self):
        return os.path.split(self.path)[1]

    @property
    def title(self):
        if len(self.cfg.title) > 0:
            return self.cfg.title
        else:
            return self.name

    def is_draft(self):
        return self.cfg is None or self.cfg.draft

    def get_pdes(self):
        p = os.path.join(self.path, '*.pde')
        return sorted(glob.glob(p))

    def has_config(self):
        return os.path.exists(os.path.join(self.path, 'yacho.sketch.toml'))


def render_sketch_page(template, sketch):

    codes = []
    filenames = []
    for pde in sketch.get_pdes():
        with open(pde, 'r', encoding='utf-8') as f:
            code = f.read()
        filename = os.path.split(pde)[1]

        codes.append(code)
        filenames.append(filename)

    return template.render(
        page_title=sketch.name,
        imgs=[],
        code_info=zip(filenames, codes)
    )


def build(cfg: SketchbookConfig):

    sketch_dirs = sorted(glob.glob(
        os.path.join(cfg.sketchbook_root, 'sketch_*')
    ))
    sketches = [Sketch(sketch_dir) for sketch_dir in sketch_dirs]
    sketches = list(filter(lambda x: not x.is_draft(), sketches))

    env = Environment(
        loader=PackageLoader('yacho'),
        trim_blocks=True
    )

    template_index = env.get_template('index.html')
    template_sketch_page = env.get_template('sketch_page.html')
    result_index = template_index.render(
        base_url=cfg.base_url,
        sketches=sketches,
        page_title=cfg.title
    )

    result_sketch_pages = []
    for sketch in sketches:
        result_sketch_page = render_sketch_page(template_sketch_page, sketch)
        result_sketch_pages.append(result_sketch_page)

    # --- Write files ---

    if not os.path.exists('dist'):
        os.mkdir('dist')

    with open(os.path.join('dist', 'index.html'), 'w') as f:
        f.write(result_index)

    for sketch, result_sketch_page in zip(sketches, result_sketch_pages):

        output_dir = os.path.join('dist', sketch.name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logging.info(f'`{output_dir}` is created.')

        with open(os.path.join(output_dir, 'index.html'), 'w') as f:
            f.write(result_sketch_page)
