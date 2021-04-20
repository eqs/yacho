import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'),
                      text_type(r'``\1``'),
                      fd.read())


setup(
    name="yacho",
    version="0.0.0",
    url="https://github.com/eqs/yacho",
    license='MIT',

    author="eqs",
    author_email="murashige.satoshi.mi1 [at] gmail.com",

    description="yacho",
    long_description=read("README.md"),

    packages=find_packages(exclude=('tests',)),

    install_requires=['click', 'toml', 'jinja2'],

    entry_points={'console_scripts': ['yacho = yacho.__main__:main']},
    include_package_data=True,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
