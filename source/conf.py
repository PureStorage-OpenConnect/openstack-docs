# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import re
import string

import sphinx_rtd_theme
#import purestoragedocstheme

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# TODO(ajaeger): enable PDF building, for example add 'rst2pdf.pdfbuilder'
extensions = [
#    'sphinxmark',
    'sphinxcontrib.spelling',
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# -- Release watermark -----------------------------------------------

releases = [
    'austin', 'bexar', 'cactus', 'diablo', 'essex', 'folsom', 'grizzly',
    'havana', 'icehouse', 'juno', 'kilo', 'liberty', 'mitaka', 'newton',
    'ocata', 'pike', 'queens', 'rocky', 'stein', 'train', 'ussuri', 'victoria',
    'wallaby', 'xena', 'yoga', 'zed', '2023.1', '2023.2', '2024.1', '2024.2',
    '2025.1'
]
unnamed = list(string.ascii_lowercase[len(releases) % 26:])
releases += unnamed


# If CI, Can we determine if we're on a stable branch via ZUUL_BRANCH?
zuul_branch = os.getenv('ZUUL_BRANCH') or ''
zuul_branch = zuul_branch if zuul_branch.startswith('stable') else ''

watermark = None

# On a local env, look at the base branch perhaps?
local_base_branch = os.popen(
    "git show-branch -a | grep '\\*' | "
    "grep -v $(git rev-parse --abbrev-ref HEAD) | head -n1").read()

local_base_branch_search = re.search(
    r"\[([A-Za-z0-9_/]+)\]", local_base_branch)
if local_base_branch_search:
    watermark = local_base_branch_search.group(1).split('stable/')[-1].upper()

watermark = watermark or zuul_branch.split("stable/")[-1].upper()

# No luck Jose, let's construct the release from what's merged.
if watermark == '':
    stable_branches = sorted(os.popen(
        "git ls-remote --heads origin | grep stable | sed 's?.*refs/heads/??'"
    ).read().strip(' \n\t').lower().split('\n'))
    if len(stable_branches) == 0 or '' in stable_branches:
        # Can be removed as soon as we have stable branches
        watermark = "2025.2 DRAFT"
    else:
        last_stable_release = stable_branches[-1].split('stable/')[-1]
        try:
            rel_index = releases.index(last_stable_release)
        except ValueError:
            rel_index = -1

        if rel_index == (len(releases) - 1) or rel_index == -1:
            watermark = "DRAFT"
        else:
            watermark = "%s DRAFT" % releases[rel_index + 1].upper()

# -- Options for sphinxmark -----------------------------------------------
sphinxmark_enable = True
sphinxmark_div = 'docs-body'
sphinxmark_image = 'text'
sphinxmark_text = watermark
sphinxmark_text_rotation = 0
sphinxmark_text_spacing = 300
sphinxmark_text_color = (255, 0, 0)
sphinxmark_text_size = 100

# -- Building the html context -----------------------------------------------

# General information about the project.
project = u'Pure Storage OpenStack Docs'
bug_tag = u'docs, dog'
copyright = u'2024, Pure Storage Inc.'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '2025.2 DRAFT'
# The full version, including alpha/beta/rc tags.
release = '2025.2 DRAFT'

# A few variables have to be set for the log-a-bug feature.
#   giturl: The location of conf.py on Git. Must be set manually.
#   gitsha: The SHA checksum of the bug description. Automatically
#           extracted from git log.
#   bug_tag: Tag for categorizing the bug. Must be set manually.
# These variables are passed to the logabug code via html_context.
giturl = u'https://github.com/PureStorage-OpenConnect/openstack-docs'
git_cmd = "/usr/bin/git log | head -n1 | cut -f2 -d' '"
gitsha = os.popen(git_cmd).read().strip('\n')
# source tree
pwd = os.getcwd()
html_context = {
    "pwd": pwd,
    "gitsha": gitsha,
    "bug_tag": bug_tag,
    "giturl": giturl,
    "bug_project": "PureStorage-OpenConnect/openstack-docs",
    "watermark": watermark,
#    'css_files': [
#        '_static/bespoke.css',  # custom CSS styling
#        '_static/sphinxmark.css',  # watermark styling
#    ],
}

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["common/*.rst"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'openstackdocs'
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = [purestoragedocstheme.get_html_theme_path()]
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = []

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# So that we can enable "log-a-bug" links from each output HTML page, this
# variable must be set to a format that includes year, month, day, hours and
# minutes.
html_last_updated_fmt = '%Y-%m-%d %H:%M'


# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
html_use_index = False

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'deploy-ops-guide'

# If true, publish source files
html_copy_source = False

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('index', 'DeployOpsGuide.tex',
     u'OpenStack Deployment and Operations Guide',
     u'Pure Storage Inc.', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'installguide', u'Install Guide',
     [u'OpenStack contributors'], 1)
]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'OpenStack Deployment and Operations Guide',
     u'OpenStack Deployment and Operations Guide',
     u'Pure Storage Inc. ', 'DeployOpsGuide',
     'This guide shows OpenStack end users how to install '
     'and configure Pure Storage FlashArrays for their OpenStack cloud.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

# -- Options for Internationalization output ------------------------------
locale_dirs = ['locale/']

# -- Options for PDF output --------------------------------------------------

pdf_documents = [
    ('index', u'DeployOpsGuide', u'OpenStack Deployment and Operations Guide',
     u'Pure Storage Inc.')
]
# -- Options for sphinxcontrib.spelling -----------------------------------------------
# http://sphinxcontrib-spelling.readthedocs.io/en/latest/customize.htm
spelling_lang='en_US'
spelling_word_list_filename='spelling_wordlist.txt'
spelling_ignore_pypi_package_names=True
