# -*- coding: utf-8 -*-
#
# Hadoop Starter Kit documentation build configuration file, created by
# sphinx-quickstart on Mon Sep 22 20:51:08 2014.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# on_rtd is whether we are on readthedocs.org, this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# -- General configuration ------------------------------------------------

hsk_dst = 'phd'
hsk_distribution = 'Pivotal HD'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
if on_rtd:
	master_doc = 'index'
else:
	master_doc = '%s/index' % hsk_dst

# General information about the project.
project = u'EMC Isilon Hadoop Starter Kit for %s' % hsk_distribution
copyright = u'2014 EMC Corporation. All Rights Reserved'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '3.0'
# The full version, including alpha/beta/rc tags.
release = '3.0'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

if not on_rtd:
	exclude_patterns.extend([
		'index.rst',
		'common'
		])
	if hsk_dst != 'cdh':
		exclude_patterns.append('cdh')
	if hsk_dst != 'phd':
		exclude_patterns.append('phd')
	if hsk_dst != 'hwx':
		exclude_patterns.append('hwx')

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# otherwise, readthedocs.org uses their theme by default, so no need to specify it

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = project + ' ' + version

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['../_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = False

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
# htmlhelp_basename = 'HadoopStarterKit'

def setup(app):
    # overrides for wide tables in RTD theme
    app.add_stylesheet('theme_overrides.css')   # path relative to _static

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'index.tex', project, u'EMC', 'manual')
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = '../common/images/emc-logo.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
latex_use_parts = True

# If true, show page references after internal links.
latex_show_pagerefs = True

# If true, show URL addresses after external links.
latex_show_urls = True

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True
