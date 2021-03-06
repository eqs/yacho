# yacho

[![Latest PyPI version](https://img.shields.io/pypi/v/yacho.svg)](https://pypi.python.org/pypi/yacho)
[![Latest Travis CI build status](https://travis-ci.com/eqs/yacho.png)](https://travis-ci.com/eqs/yacho)

The static site generator for creative coders.

## Demo page

* Demo page: https://yacho-demo.netlify.app/
* Repository: https://github.com/eqs/yacho-example

## Requirements

* Python 3.7+

## Installation

```
pip install yacho
```

## Usage

### Directory Structure

```
.
│  avatar.png
│  custom.css
│  yacho.sketchbook.toml    <----------- Put PROJECT config file
│
├─sketch_210401a
│  │  sketch_210401a.pde
│  │  yacho.sketch.toml    <----------- Put sketch config file
│  │
│  ├─cover
│  │      cover_image.png
│  │
│  └─images
│          img1.png
│          img2.png
│          img3.png
│          ...
│
└─sketch_210402a
    │  sketch_210402a.pde
    │  yacho.sketch.toml    <----------- Put sketch config file
    │
    ├─cover
    │      cover_image.png
    │
    └─images
            img1.png
            img2.png
            img3.png
            ...
```

### Build site

```
# v0.0.2+
yacho build

# v0.0.1
# yacho yacho.sketchbook.toml
```

Push `dist` to your gh-pages.

### Sketch generator

Processing sketch

```
yacho create
```

p5.js sketch

```
yacho create -t p5js
```

### Example `yacho.sketchbook.toml`

```toml
sketchbook_root = '.'

base_url = 'https://yacho-demo.netlify.app/'

# Page title
title = 'My Sketchbook'

# Profile information
author = 'eqs'
avatar = 'chi.png' # relative path from sketchbook_root
bio = """
Creative Coder
"""

# Your custom css (relative path from sketchbook_root)
custom_css = 'custom.css'

[social]
home = "https://www.eqseqs.work"
twitter = "eqs_work"
github = "eqs"
instagram = ""
youtube = ""
facebook = ""
```

### Example `yacho.sketch.toml`

```toml
# If title is empty, sketch dir name will be used as title.
title = "Flowers"

# Default to false
draft = false

comment = "An example comment."

# Files listed in this value will be public.
# Default to:
public = ['*.pde', 'sketch.js', '*.py']

# video embedding will be available v0.0.2
[video]
# Please set 'none', 'youtube', 'vimeo', 'neort' or 'gif'
type = 'none'

# If you use 'gif', id will be interpreted as file path of gif animation.
id = ''
```
