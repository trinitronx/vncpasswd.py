REPO_NAME              := vncpasswd.py
SHELL                   = /bin/bash
VERSION_FILE            = VERSION
VERSION                 =`cat $(VERSION_FILE)`
PACKAGE_FILE            = $(REPO_NAME)-$(VERSION).tar.gz

include ./build/main.mk

setup: ## Run python setup.py sdist
	python setup.py sdist

install: ## Runs python setup.py install
	python setup.py install

test: ## Runs tests
	python vncpasswd.py -t

.PHONY: clean
clean:: ## Removes all temporary files - Executes make clean
	rm -rf ./dist
	rm -f MANIFEST
	rm -f README.rst README.txt
	find ./ -iname '*.pyc' -exec rm -f '{}' \;
