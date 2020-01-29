REPO_NAME              := vncpasswd.py
SHELL                   = /bin/bash
VERSION_FILE            = VERSION
VERSION                 =`cat $(VERSION_FILE)`
PACKAGE_FILE            = $(REPO_NAME)-$(VERSION).tar.gz

include ./build/main.mk

setup: ## Run python setup.py sdist
	python setup.py sdist
sdist: setup

bdist: ## Run python setup.py bdist
	python setup.py bdist

bdist_rpm: ## Run python setup.py bdist_rpm
	python setup.py bdist_rpm

bdist_wininst: ## Run python setup.py bdist_wininst
	python setup.py bdist_wininst

install: ## Runs python setup.py install
	python setup.py install

test: ## Runs tests
	python vncpasswd.py -t

.PHONY: clean
clean:: ## Removes all temporary files - Executes make clean
	rm -rf ./build/lib ./build/scripts-* ./build/bdist.*
	rm -rf ./dist ./vncpasswd.py.egg-info/
	rm -f MANIFEST
	rm -f README.rst README.txt
	find ./ -iname '*.pyc' -exec rm -f '{}' \;
