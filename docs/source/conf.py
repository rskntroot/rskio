# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Rskio'
copyright = '2024, rskntroot'
author = 'rskntroot'
release = '1.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Markdown Support - https://www.sphinx-doc.org/en/master/usage/markdown.html
extensions = ['myst_parser']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# PyData Theme - https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html (0.15.3)
html_theme = "furo"
html_static_path = ['_static']
