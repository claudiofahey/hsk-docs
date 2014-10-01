
rmdir /s /q _build

call sphinx-build -a -c cdh -b html  -d _build/cdh/doctrees . _build/cdh/html
call sphinx-build -a -c cdh -b latex -d _build/cdh/doctrees . _build/cdh/latex

call sphinx-build -a -c phd -b html  -d _build/phd/doctrees . _build/phd/html
call sphinx-build -a -c phd -b latex -d _build/phd/doctrees . _build/phd/latex

rem pandoc -f rst -t latex -o out.pdf --latex-engine=xelatex deploying-cloudera-cdh-5-with-isilon.rst

pause
