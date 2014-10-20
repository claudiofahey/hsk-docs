
rmdir /s /q _build

call sphinx-build -a -c hwx -b html  -d _build/hwx/doctrees . _build/hwx/html
call sphinx-build -a -c hwx -b latex -d _build/hwx/doctrees . _build/hwx/latex

call sphinx-build -a -c phd -b html  -d _build/phd/doctrees . _build/phd/html
call sphinx-build -a -c phd -b latex -d _build/phd/doctrees . _build/phd/latex

call sphinx-build -a -c cdh -b html  -d _build/cdh/doctrees . _build/cdh/html
call sphinx-build -a -c cdh -b latex -d _build/cdh/doctrees . _build/cdh/latex

rem pandoc -f rst -t latex -o out.pdf --latex-engine=xelatex deploying-cloudera-cdh-5-with-isilon.rst

pause
