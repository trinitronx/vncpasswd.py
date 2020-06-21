REPO_NAME              := vncpasswd.py
SHELL                   = /bin/bash
VERSION_FILE            = VERSION
VERSION                 = $(shell cat $(VERSION_FILE))
PACKAGE_FILE            = $(REPO_NAME)-$(VERSION).tar.gz

git_current := $(shell cut -c6- .git/HEAD)

# GNU Automake style vars (overridable)
PACKAGE        ?= $(REPO_NAME)
top_srcdir     ?= .
distdir        ?= $(PACKAGE)-$(VERSION)
top_distdir    ?= $(distdir)
top_builddir   ?= ./build
CLEANFILES     ?= $(top_builddir)/lib $(top_builddir)/scripts-* $(top_builddir)/bdist.*
DISTCLEANFILES ?= $(top_srcdir)/dist/ $(top_srcdir)/MANIFEST \
                    $(top_srcdir)/vncpasswd.py.egg-info/ \
                    $(top_srcdir)/README.rst $(top_srcdir)/README.txt \
                    $(top_builddir)/

include $(top_srcdir)/build-aux/main.mk

build-depends: ## Install python pip build dependencies
	pip install --user -r ./build-aux/build-requirements.txt

setup: ## Run python setup.py sdist
	python setup.py sdist
sdist: setup

bdist: ## Run python setup.py bdist
	python setup.py bdist

bdist_rpm: build-depends ## Run python setup.py bdist_rpm
	python setup.py bdist_rpm

bdist_wininst: ## Run python setup.py bdist_wininst
	python setup.py bdist_wininst

bdist_msi: ## Run python setup.py bdist_msi
	python setup.py bdist_msi

install: ## Runs python setup.py install
	python setup.py install

test: ## Runs tests
	python vncpasswd.py -t

.PHONY: CHANGELOG
CHANGELOG: CHANGELOG.md ## Generate CHANGELOG.md from git-chglog
git-version.stamp: .git/$(git_current) ## no-help
	git describe --abbrev=4 2>/dev/null | cut -d'^' -f1 > git-version.stamp
CHANGELOG.md: git-version.stamp ## no-help
	git-chglog --config "$(top_srcdir)/.chglog/config.yml" --output $@

.PHONY: clean
clean:: ## Removes all temporary files - Executes make clean
	rm -rf $(CLEANFILES)
	rm -f $(top_srcdir)/git-version.stamp
	find $(top_srcdir)/ -iname '*.pyc' -exec rm -f '{}' \;

distclean:: clean ## Removes all files created by make setup / sdist, bdist* targets
	rm -rf $(DISTCLEANFILES)
