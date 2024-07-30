#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import sys
from typing import Dict

sys.path.insert(0, os.path.abspath(".."))  # noqa
import ffmpy  # noqa

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

source_suffix = ".rst"
master_doc = "index"

project = "ffmpy"
copyright = f"2015-{datetime.datetime.now().year}, Andrii Yurchuk"
author = "Andrii Yurchuk"

version = ffmpy.__version__
release = ffmpy.__version__

language = "en"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

primary_domain = "py"
default_role = "py:obj"
pygments_style = "sphinx"
todo_include_todos = False

html_theme = "sphinx_rtd_theme"

htmlhelp_basename = "ffmpydoc"

latex_elements: Dict = {}
latex_documents = [
    (master_doc, "ffmpy.tex", "ffmpy Documentation", "Andrii Yurchuk", "manual"),
]

man_pages = [(master_doc, "ffmpy", "ffmpy Documentation", [author], 1)]

texinfo_documents = [
    (
        master_doc,
        "ffmpy",
        "ffmpy Documentation",
        author,
        "ffmpy",
        "One line description of project.",
        "Miscellaneous",
    ),
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
autoclass_content = "both"
autodoc_member_order = "bysource"
