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
            f.write('draft = false')


def generate_id(c):
    if c <= ord('z') - ord('a'):
        return chr(c + ord('a'))
    else:
        return 'z' + f(c - (ord('z') - ord('a') + 1))


def generate_p5js():
    env = Environment(loader=PackageLoader(
        'template/sketch/p5js',
        encoding='utf8'
    ))
    tpl_index = env.get_template('index.html')
    tpl_js = env.get_template('sketch.js')

    now = datetime.datetime.now()
    date = now.strftime('%y%m%d')
    today_sketch_list = list(filter(lambda x : date in x, os.listdir('.')))

    param = {'id' : 'sketch_' + date + generate_id(len(today_sketch_list))}
    output_html = tpl_index.render(param).encode('utf-8')
    output_js = tpl_js.render({}).encode('utf-8')

    # Write files
    make_project_dir(param['id'])

    with open(os.path.join(param['id'], 'index.html'), 'wb') as f:
        f.write(output_html)

    with open(os.path.join(param['id'], f'{param["id"]}.js'), 'wb') as f:
        f.write(output_js)


def generate_pde():
    env = Environment(loader=PackageLoader('template/sketch/pde', encoding='utf8'))
    tpl = env.get_template('template.pde')

    now = datetime.datetime.now()
    date = now.strftime('%y%m%d')

    today_sketch_list = list(filter(lambda x : date in x, os.listdir('.')))
    param = {'id' : 'sketch_' + date + generate_id(len(today_sketch_list))}

    output = tpl.render({}).encode('utf-8')

    # Write files
    make_project_dir(param['id'])

    with open(os.path.join(param['id'], f'{param["id"]}.pde'), 'wb') as f:
        f.write(output)


def generate_sketch(type='pde'):
    generate_pde()
