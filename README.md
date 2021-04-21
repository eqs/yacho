# yacho

yacho

[![Latest PyPI version](https://img.shields.io/pypi/v/yacho.svg)](https://pypi.python.org/pypi/yacho)
[![Latest Travis CI build status](https://travis-ci.com/eqs/yacho.png)](https://travis-ci.com/eqs/yacho)

## Requirements

* Python 3.7+

## Installation

```
pip install git+https://github.com/eqs/yacho.git@v0.0.1
```

## Usage

### Directory Structure

### Build site

```
yacho yacho.sketchbook.toml
```

## Example

* Demo page: https://yacho-demo.netlify.app/
* Repository: https://github.com/eqs/yacho-example

### Example `yacho.sketchbook.toml`

```toml
sketchbook_root = '.'

base_url = 'https://yacho-demo.netlify.app/'

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
```
