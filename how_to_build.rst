
************
How to Build
************

On Windows
----------

Sphinx

Pandoc

MikTeX

Sublime Text 2

https://sublime.wbond.net/packages/Restructured%20Text%20(RST)%20Snippets

Install RTD Theme Locally
-------------------------

pip install sphinx_rtd_theme

git clone https://github.com/snide/sphinx_rtd_theme.git

cp -rv sphinx_rtd_theme/sphinx_rtd_theme ../hsk-docs/_themes/


On Ubuntu
----------

aptitude install python-sphinx

aptitude install python-setuptools

easy_install rst2pdf

rst2pdf --output out.pdf --stylesheets sphinx,kerning,letter deploying-cloudera-cdh-5-with-isilon.rst

Github
------

Configure Github to push changes to ReadTheDocs.org.
