all:
	echo Hello.
install:
	./setup.py install
uninstall:
	-pip3 uninstall -y genice
test:
	python graphstat/graphstat_sqlite3.py
	python graphstat/graphstat_sqlite3.py
clean:
	-rm *.scad *.yap @*
	-rm -rf build dist
	-rm -rf graphstat.egg-info
	-rm README.rst
	-rm .DS_Store
	find . -name __pycache__ | xargs rm -rf 
	find . -name \*.pyc      | xargs rm -rf
	find . -name \*~         | xargs rm -rf
