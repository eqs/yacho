# -*- coding: utf-8 -*-
import os
import datetime
import shutil
from jinja2 import Environment, PackageLoader


def make_project_dir(path: str):
    cover_path = os.path.join(path, 'cover')
    if not os.path.exists(cover_path):
        os.makedirs(cover_path)
        with open(os.path.join(cover_path, '.gitkeep'), 'w') as f:
            f.write('')

    images_path = os.path.join(path, 'images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)
        with open(os.path.join(images_path, '.gitkeep'), 'w') as f:
            f.write('')

    config_path = os.path.join(path, 'yacho.sketch.toml')
    if not os.path.exists(config_path):
        with open(os.path.join(config_path), 'w') as f:
            f.write('draft = true')


def generate_id(c):
    if c <= ord('z') - ord('a'):
        return chr(c + ord('a'))
    else:
        return 'z' + generate_id(c - (ord('z') - ord('a') + 1))


class OverworkError(RuntimeError):
    pass


def get_sketch_name(working_dir: str):
    now = datetime.datetime.now()
    date = now.strftime('%y%m%d')
    today_sketch_list = list(filter(lambda x : date in x, os.listdir(working_dir)))
    if len(today_sketch_list) <= ord('z') - ord('a'):
        return 'sketch_' + date + generate_id(len(today_sketch_list))
    else:
        raise OverworkError('You\'ve reached the limit for auto naming of '\
                            'new sketches for the day. '\
                            'How about going for a walk instead?')


def generate_p5js():
    env = Environment(loader=PackageLoader(
        'yacho',
        encoding='utf8'
    ))
    tpl_index = env.get_template('sketch/p5js/index.html')
    tpl_js = env.get_template('sketch/p5js/sketch.js')

    param = {'id' : get_sketch_name('.')}
    output_html = tpl_index.render(param).encode('utf-8')
    output_js = tpl_js.render(param).encode('utf-8')

    # Write files
    make_project_dir(param['id'])

    with open(os.path.join(param['id'], 'index.html'), 'wb') as f:
        f.write(output_html)

    with open(os.path.join(param['id'], 'sketch.js'), 'wb') as f:
        f.write(output_js)


def generate_pde():
    env = Environment(loader=PackageLoader('yacho', encoding='utf8'))
    tpl = env.get_template('sketch/pde/template.pde')

    param = {'id' : get_sketch_name('.')}
    output = tpl.render(param).encode('utf-8')

    # Write files
    make_project_dir(param['id'])

    with open(os.path.join(param['id'], f'{param["id"]}.pde'), 'wb') as f:
        f.write(output)


def generate_sketch(type='pde'):
    if type == 'pde':
        generate_pde()
    elif type == 'p5js':
        generate_p5js()
    else:
        raise RuntimeError(f'Unknown sketch type: {type}')
