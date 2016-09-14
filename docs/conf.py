#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(".."))  # noqa
import ffmpy

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = 'ffmpy'
copyright = '2016, Andriy Yurchuk'
author = 'Andriy Yurchuk'

version = ffmpy.__version__
release = ffmpy.__version__

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

primary_domain = 'py'
default_role = 'py:obj'
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

htmlhelp_basename = 'ffmpydoc'

latex_elements = {}
latex_documents = [
    (master_doc, 'ffmpy.tex', 'ffmpy Documentation',
     'Andriy Yurchuk', 'manual'),
]

man_pages = [
    (master_doc, 'ffmpy', 'ffmpy Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'ffmpy', 'ffmpy Documentation',
     author, 'ffmpy', 'One line description of project.',
     'Miscellaneous'),
]

intersphinx_mapping = {'https://docs.python.org/3': None}
autoclass_content = 'both'
autodoc_member_order = 'bysource'
