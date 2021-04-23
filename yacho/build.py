# -*- coding: utf-8 -*-
import os
import shutil
import glob
import functools
import logging
from jinja2 import Environment, PackageLoader

from .config import (
    load_sketch_config, SketchbookConfig, VideoType, CodeInfo
)


class Sketch:
    def __init__(self, path: str, sketchbook_cfg: SketchbookConfig):

        self.path = path
        self.sketchbook_cfg = sketchbook_cfg

        if self.has_config():
            self.cfg = load_sketch_config(
                os.path.join(self.path, 'yacho.sketch.toml')
            )
        else:
            self.cfg = None

        # 設定ファイルに画像の記載が無い
        # & カバー画像，画像リストのフォルダが存在するならフォルダからの
        # デプロイにする
        if (os.path.exists(os.path.join(self.path, 'cover'))
                and os.path.exists(os.path.join(self.path, 'images'))
                and (len(self.cfg.cover) == 0 and len(self.cfg.images) == 0)):

            cover = glob.glob(
                os.path.join(self.path, 'cover', '*')
            )[0]
            self.cfg.cover = os.path.join('cover', os.path.split(cover)[1])

            images = glob.glob(
                os.path.join(self.path, 'images', '*')
            )
            self.cfg.images = [os.path.join('images', os.path.split(image)[1])
                               for image in images]

    @property
    def name(self):
        return os.path.split(self.path)[1]

    @property
    def title(self):
        if len(self.cfg.title) > 0:
            return self.cfg.title
        else:
            return self.name

    @property
    def cover_name(self):
        return os.path.split(self.cfg.cover)[1]

    @property
    def url(self):
        return self.name

    @property
    def cover_url(self):
        return self.url + '/imgs/' + self.cover_name

    def is_draft(self):
        return self.cfg is None or self.cfg.draft

    def get_codes(self):
        paths = self.get_code_paths()
        codes = []
        for path in paths:
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
            codes.append(CodeInfo(path, code))
        return codes

    def get_code_paths(self):
        if self.cfg is None:
            return []
        else:
            paths = []
            for name in self.cfg.public:
                paths.append(glob.glob(os.path.join(self.path, name)))
            paths = list(functools.reduce(lambda x, y: x + y, paths))
            return sorted(paths)

    def get_cover(self):
        if len(self.cfg.cover) > 0:
            return os.path.join(self.path, self.cfg.cover)
        else:
            return None

    def get_images(self):
        images = [os.path.join(self.path, image) for image in self.cfg.images]
        return images

    def has_config(self):
        return os.path.exists(os.path.join(self.path, 'yacho.sketch.toml'))


def render_sketch_page(cfg, template, sketch):

    code_infos = sketch.get_codes()

    if sketch.get_cover() is not None:
        cover_filename = os.path.split(sketch.get_cover())[1]
    else:
        cover_filename = None
    image_filenames = [os.path.split(image)[1]
                       for image in sketch.get_images()]

    video_type = sketch.cfg.video.type
    video_id = sketch.cfg.video.id
    video_embed_code = VideoType.get_embed_code(video_type, video_id)

    return template.render(
        cfg=cfg,
        base_url=cfg.base_url,
        site_title=cfg.title,
        page_title=sketch.title,
        sketch=sketch,
        comment=sketch.cfg.comment,
        video_embed_code=video_embed_code,
        cover=cover_filename,
        images=image_filenames,
        code_infos=code_infos,
        custom_css=os.path.split(cfg.custom_css)[1]
    )


def build_site(cfg: SketchbookConfig):

    sketch_dirs = sorted(glob.glob(
        os.path.join(cfg.sketchbook_root, 'sketch_*')
    ))
    sketches = [Sketch(sketch_dir, cfg) for sketch_dir in sketch_dirs]
    sketches = list(filter(lambda x: not x.is_draft(), sketches))

    env = Environment(
        loader=PackageLoader('yacho'),
        trim_blocks=True
    )

    template_index = env.get_template('index.html')
    template_sketch_page = env.get_template('sketch_page.html')
    result_index = template_index.render(
        cfg=cfg,
        base_url=cfg.base_url,
        sketches=sketches,
        site_title=cfg.title,
        page_title=cfg.title,
        author=cfg.author,
        bio=cfg.bio,
        avatar=cfg.avatar,
        custom_css=os.path.split(cfg.custom_css)[1]
    )

    result_sketch_pages = []
    for sketch in sketches:
        result_sketch_page = render_sketch_page(
            cfg, template_sketch_page, sketch
        )
        result_sketch_pages.append(result_sketch_page)

    # --- Write files ---

    if not os.path.exists('dist'):
        os.mkdir('dist')

    with open(os.path.join('dist', 'index.html'), 'w') as f:
        f.write(result_index)

    for sketch, result_sketch_page in zip(sketches, result_sketch_pages):

        # Create output directory

        output_dir = os.path.join('dist', sketch.name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logging.info(f'`{output_dir}` is created.')

        img_dir = os.path.join('dist', sketch.name, 'imgs')
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
            logging.info(f'`{img_dir}` is created.')

        # Write HTMLs

        with open(os.path.join(output_dir, 'index.html'), 'w') as f:
            f.write(result_sketch_page)

        # Copy images

        cover_path = sketch.get_cover()
        if cover_path is not None and os.path.exists(cover_path):
            cover_name = os.path.split(cover_path)[1]
            shutil.copy(cover_path, os.path.join(img_dir, cover_name))
        else:
            logging.warning(f'Cover image: `{cover_path}` is not found.')

        image_paths = sketch.get_images()
        for image_path in image_paths:
            if os.path.exists(image_path):
                _, img_name = os.path.split(image_path)
                shutil.copy(image_path, os.path.join(img_dir, img_name))
            else:
                logging.warning(f'Image: `{image_path}` is not found.')

        # Copy gif
        if sketch.cfg.video.type == VideoType.gif:
            # 出力先のディレクトリが無いなら作る
            gif_dir = os.path.join('dist', sketch.name, 'gifs')
            if not os.path.exists(gif_dir):
                os.makedirs(gif_dir)
                logging.info(f'`{gif_dir}` is created.')

            # GIF画像のときはIDがファイルパス
            gif_path = os.path.join(sketch.name, sketch.cfg.video.id)
            _, gif_name = os.path.split(gif_path)
            shutil.copy(gif_path, os.path.join(gif_dir, gif_name))

        # Static files
        static_images_dir = os.path.join('dist', 'images')
        if not os.path.exists(static_images_dir):
            os.makedirs(static_images_dir)
            logging.info(f'`{static_images_dir}` is created.')

        if len(cfg.avatar) > 0:
            _, img_name = os.path.split(cfg.avatar)
            shutil.copy(cfg.avatar, os.path.join(static_images_dir, img_name))

        static_css_dir = os.path.join('dist', 'css')
        if not os.path.exists(static_css_dir):
            os.makedirs(static_css_dir)
            logging.info(f'`{static_css_dir}` is created.')

        if len(cfg.custom_css) > 0:
            _, css_name = os.path.split(cfg.custom_css)
            shutil.copy(cfg.custom_css, os.path.join(static_css_dir, css_name))
