REPO_NAME              := vncpasswd.py
SHELL                   = /bin/bash
VERSION_FILE            = VERSION
VERSION                 = $(shell cat $(VERSION_FILE))
PACKAGE_FILE            = $(REPO_NAME)-$(VERSION).tar.gz

# GNU Automake style vars (overridable)
PACKAGE     ?= $(REPO_NAME)
top_srcdir  ?= .
distdir     ?= $(PACKAGE)-$(VERSION)
top_distdir ?= $(distdir)
DISTFILES   ?= $(top_srcdir)/dist/ MANIFEST

include $(top_srcdir)/build/main.mk

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

.PHONY: CHANGELOG
CHANGELOG: CHANGELOG.md ## Generate CHANGELOG.md from git-chglog
git-version.stamp: ## no-help
	git describe --abbrev=4 2>/dev/null | cut -d'^' -f1 > git-version.stamp
CHANGELOG.md: git-version.stamp ## no-help
	git-chglog --config "$(top_srcdir)/.chglog/config.yml" --output $@

.PHONY: clean
clean:: ## Removes all temporary files - Executes make clean
	rm -rf ./build/lib ./build/scripts-* ./build/bdist.*
	rm -rf $(distdir)
	rm -rf $(top_srcdir)/vncpasswd.py.egg-info/
	rm -f $(top_srcdir)/git-version.stamp
	rm -f $(top_srcdir)/MANIFEST
	rm -f $(top_srcdir)/README.rst $(top_srcdir)/README.txt
	find $(top_srcdir)/ -iname '*.pyc' -exec rm -f '{}' \;

distclean:: ## Removes all files created by make setup
	rm -rf $(DISTFILES)
