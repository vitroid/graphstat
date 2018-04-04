all:
	echo Hello.
install:
	./setup.py install
uninstall:
	-pip3 uninstall -y genice
distclean:
	-rm *.scad *.yap @*
	-rm -rf build dist
	-rm -rf graphstat.egg-info
	-rm README.rst
	-rm .DS_Store
	find . -name __pycache__ | xargs rm -rf 
	find . -name \*.pyc      | xargs rm -rf
	find . -name \*~         | xargs rm -rf
