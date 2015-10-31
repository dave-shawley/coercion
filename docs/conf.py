#!/usr/bin/env python
# -*- coding: utf-8 -*-

import alabaster

import coercion


project = 'coercion'
copyright = '2015, Dave Shawley'
version = coercion.__version__
release = '.'.join(str(x) for x in coercion.version_info[:2])

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]
templates_path = []
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_theme_path = [alabaster.get_path()]
html_static_path = []
html_sidebars = {
    '**': ['about.html', 'navigation.html'],
}
html_theme_options = {
    'description': 'Coerces datastructures',
    'github_user': 'dave-shawley',
    'github_repo': 'coercion',
    'github_banner': True,
}

intersphinx_mapping = {
    'python': ('http://docs.python.org/3/', None),
}
