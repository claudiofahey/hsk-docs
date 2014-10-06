
********************************
Hadoop Starter Kit Documentation
********************************

Introduction
------------

This documentation is an update to our previous EMC Isilon Hadoop Starter Kits (HSK).
Besides lots of new content and updates, the structure of the documentation is
now completely different.
The documentation source files are composed of multiple 
plain-text files that are marked up using ReStructuredText (RST). 
This has some similarities with Markdown but it is a lot more flexible and standardized.
These files are processed into a complete documetation set using Sphinx (http://sphinx-doc.org/).
Although Sphinx has its origin as a Python documentation generator, it's also
a very flexibile, general-purpose, open-source, and freely available documentation tool.
Sphinx can convert your RST documents to HTML, PDF, and many other formats.
Another benefit of using Sphinx is that your documentation can be hosted for free
on http://readthedocs.org/.

There are currently several different variations of the Hadoop Starter Kit.

-  `EMC Isilon Hadoop Starter Kit for Cloudera <http://hsk-cdh.readthedocs.org/>`_
   
-  `EMC Isilon Hadoop Starter Kit for Pivotal <http://hsk-phd.readthedocs.org/>`_

-  `EMC Isilon Hadoop Starter Kit for Hortonworks <http://hsk-hwx.readthedocs.org/>`_

How the Sources Files are Organized
-----------------------------------

The source files are maintained in the Github project https://github.com/claudiofahey/hsk-docs.
When updates are committed to this project by a contributor, the documentation on Read the Docs is automatically
updated.

Each variation (e.g. *EMC Isilon Hadoop Starter Kit for Cloudera*) has its own *index.rst* (Table of Contents) 
and main *hsk.rst* file within a subdirectory (e.g. *cdh*).
There are many sections that are common among these variations. These common sections are in the *common* subdirectory
and they are referenced by *hsk.rst* using the RST include directive.

For example::

  .. include:: ../common/prepare-isilon.rst

When any changes are committed to *prepare-isilon.rst*, all HSK variations that include this file will be updated.

To allow for each HSK variation to become its own PDF, each one has its own Sphinx conf.py file (e.g. *cdh/conf.py*). 

Contributing Changes
--------------------

This documentation is built using open-source tools and the process to contribute updates is the same as in a typical
open-source project. 
In short, create your own branch of this project, commit changes to your branch, and then send a pull request
to us. We will then review and hopefully approve your changes. If you haven't used Github before, you may want
to start with https://guides.github.com/.

If desired, you may want to make your own branch available on Read the Docs while you are drafting it so that you
can easily see the final results. **If you do this, be sure to mark your Read the Docs project as protected or private
so that others don't confuse it with the official documentation.**

For an introduction to RST and Sphinx, see the following:

-  http://write-the-docs.readthedocs.org/

-  http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/sphinx.html

-  http://sphinx-doc.org/rest.html

Read the Docs Configuration
---------------------------

Read the Docs projects are configured as follows:

-  Repo: https://github.com/claudiofahey/hsk-docs.git
   
-  Documentation type: Sphinx Html
   
-  Python configuration file: ``cdh/conf.py``, ``phd/conf.py``, etc.
   
-  Privacy Level: Protected

Building Locally
----------------

It is a good idea to prepare your local workstation to build your documentation locally. This
will allow you to see your changes quickly without having to commit changes to Github and waiting
for Read the Docs to build them.

#.  To edit the RST files, any plain text editor can be used. I recommend 
    `Sublime Text 2 <http://www.sublimetext.com/2>`_ 
    with the RST add-on 
    https://sublime.wbond.net/packages/Restructured%20Text%20(RST)%20Snippets.

#.  You'll also need to install Python and Sphinx. See http://sphinx-doc.org/install.html.

#.  To make your local documentation use the same theme used on ReadTheDocs.org, you'll need
    to install the RTD theme locally.

    ::

      pip install sphinx_rtd_theme

#.  The above is all that is needed to produce HTML documentation locally.
    If you want to produce PDF documentation also, you will need to install 
    `Pandoc <http://johnmacfarlane.net/pandoc/installing.html>`_ and
    `MiKTeX <http://miktex.org/>`_.

#.  To build on Windows, run ``make.cmd``.
  
    To build on Linux, run ``make html`` or ``make latexpdf``.


To Update the RTD Theme
-----------------------

::

  pip install sphinx_rtd_theme

  git clone https://github.com/snide/sphinx_rtd_theme.git

  cp -rv sphinx_rtd_theme/sphinx_rtd_theme ../hsk-docs/_themes/

See also http://read-the-docs.readthedocs.org/en/latest/theme.html.
