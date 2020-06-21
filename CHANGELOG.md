
<a name="v1.2.3"></a>
## [v1.2.3](https://github.com/trinitronx/range2cidr/compare/v1.2.2...v1.2.3)

> 2020-06-21

### Bug Fixes

* **non-windows:** Fixes [#23](https://github.com/trinitronx/range2cidr/issues/23) - Handle `_key_type` check properly on non-windows platforms


<a name="v1.2.2"></a>
## [v1.2.2](https://github.com/trinitronx/range2cidr/compare/v1.2.1...v1.2.2)

> 2020-06-21

### Bug Fixes

* **CHANGELOG:** Use git-version.stamp to determine when to re-generate CHANGELOG.md
* **README:** Document Windows Python & VS Code install further
* **Windows:** Only add pass2reg.cmd to distribution scripts on Windows platform
* **Windows:** Update usage help output for pass2reg.cmd script
* **Windows:** Fix pass2reg.cmd script for WinVNC3 registry write
* **Windows:** Fixes [#20](https://github.com/trinitronx/range2cidr/issues/20) - Fix unhandled cases when Registry I/O failed or `args.passwd` is `None`
* **Windows:** Fixes [#21](https://github.com/trinitronx/range2cidr/issues/21) - Properly decode Hexidecimal Registry values when type is REG_SZ
* **non-windows:** Only print registry warning on non-Windows platforms when -R flag is requested (fixes [#18](https://github.com/trinitronx/range2cidr/issues/18))

### Code Refactoring

* **CHANGELOG:** Use full config.yml for `git-chglog`
* **CHANGELOG:** Detect changes from .git/refs/* (When file commit ids change)
* **Makefile:** Better handling for clean / distclean targets
* **Makefile:** Use GNU Make shell instead of backtick
* **Makefile:** Add distclean, debug targets; Use Automake style variables; Help text cleanup
* **travis-ci:** Use new build-depends Makefile target

### Features

* **CHANGELOG:** Adding git-chglog configs for auto-generated CHANGELOG.md
* **CHANGELOG:** Adding create-release GitHub Action workflow w/CHANGELOG generation
* **CHANGELOG:** Update CHANGELOG for v1.2.2
* **CHANGELOG:** Add generated CHANGELOG.md
* **Makefile:** Document `make build-depends` target in README.md
* **Makefile:** Add `make build-depends` target to install build dependencies via pip
* **STDOUT:** Add `-o` / `--stdout` flags for quieter and scriptable ASCII (decrypted plaintext) or HEX (ciphertext) output
* **Windows:** Add bdist_msi Makefile & VSCode targets
* **Windows:** Add debug functionality to WindowsRegistry class & make warnings quieter by default
* **Windows:** Add debug functionality to doctests
* **Windows:** Document pass2reg.cmd that is installed on Windows %PATH%
* **bdist_rpm:** Fix settings for building bdist_rpm target
* **eprint:** Implement STDERR print function eprint() & convert all print() calls for Python 3
* **vscode:** Adding VSCode tasks.json for common project Makefile tasks
* **vscode:** Adding VSCode launch.json for common project Debug tasks


<a name="v1.2.1"></a>
## [v1.2.1](https://github.com/trinitronx/range2cidr/compare/v1.2.0...v1.2.1)

> 2019-08-09

* Bump version to 1.2.1
* Fix indents for some print statements
* Fix imports for python package.module syntax
* Merge pull request [#12](https://github.com/trinitronx/range2cidr/issues/12) from trinitronx/project-packaging-travis-ci-docker
* Refactor docker push to use Makefile target: ship
* Merge pull request [#11](https://github.com/trinitronx/range2cidr/issues/11) from trinitronx/project-packaging-travis-ci-docker
* Trying to fix push: Switch to use REPO for Docker Image (REPO_NAME cannot have slashes)
* Switch to REGISTRY short name?
* Refactor TravisCI build & Docker Image tag debug output into GNU Make function
* Removing AWS / ECR specific ship tasks in Makefile
* Merge pull request [#10](https://github.com/trinitronx/range2cidr/issues/10) from trinitronx/project-packaging-travis-ci-docker
* Switch docker image repo slug tagging to be compatible with Docker Hub
* Adding actual Docker push command now that we know state of TravisCI merged vars
* Merge pull request [#9](https://github.com/trinitronx/range2cidr/issues/9) from trinitronx/project-packaging-travis-ci-docker
* Output TRAVIS_EVENT_TYPE, TRAVIS_PULL_REQUEST for eval as better "push to master" image push trigger
* Output better TravisCI ENV var via info for debugging
* Try to fix TravisCI tagging logic to avoid latest & VERSION on PR builds (assumption is: TRAVIS_PULL_REQUEST_BRANCH is set only on PRs, not on merge to master)
* Add TRAVIS_BRANCH detection to trigger Docker image tag via VERSION file & "latest" on master
* Add make package to TravisCI build to test docker packaging
* Merge pull request [#8](https://github.com/trinitronx/range2cidr/issues/8) from trinitronx/project-packaging-docker
* setup.py changes to use VERSION file
* Adding initial Dockerfile & VERSION file
* Merge pull request [#7](https://github.com/trinitronx/range2cidr/issues/7) from trinitronx/project-packaging
* Try to fix "IOError: [Errno 13] Permission denied" on TravisCI
* Remove deprecated Gratipay & replace with Liberapay
* Fix ImportError exception on TravisCI
* Fix ImportError exception handler to read correct file... next fix TravisCI build
* Add initial Makefile python / docker framework
* Add missing metadata to setup.py, and auto-generate README.rst, README.txt from README.md
* Add setup.py for distutils packaging
* Move libraries to own directories for packaging

<a name="v1.2.0"></a>
## [v1.2.0](https://github.com/trinitronx/range2cidr/compare/v1.0.0...v1.2.0)

> 2017-06-02

* Merge branch 'master' of github.com:trinitronx/vncpasswd.py
* Merge pull request [#5](https://github.com/trinitronx/range2cidr/issues/5) from sikyu/master
* Handle both vncserver and WinVNC keys
* Handle 32-bit Python on 64-bit Windows
* Only py2 compatible
* Adding downloads badge

<a name="v1.0.0"></a>
## v1.0.0

> 2014-10-28

* Update badge due to name change: Gittip -> Gratipay
* Use shields.io for SVG build status badge
* Adding gittip badge to repo
* Adding build status badge to README
* Adding travis.yml for CI tests
* Fix Windows checks
* Fix script on Linux (make _winreg conditional import for Windows)
* Updated README; Add misc. metadata
* Merge branch 'add-windows-registry-io'
* Fail much more gracefully without write access rights
* Get Windows Registry Input/Output working!
* Fix WindowsRegistry to fail gracefully if no write access
* Fix WindowsRegistry class tests & access rights
* Add python bytecode files to .gitignore
* Some improvements to WindowsRegistry class
* Update References in README
* Add 2013 (c) year
* Added License and Credits information
* Added unit tests to unhex function
* Added python version compatibility note to README. closes [#1](https://github.com/trinitronx/range2cidr/issues/1)
* Update README with new references for win reg keys.
* Add initial registry read flag; Attempt to use WindowsRegistry class...
* Added WindowsRegistry class
* Some quick readme updates
* Added README markdown file for github
* Cleanup some debug info
* Strip whitespace and use new unhex function on hex file input
* Fixes for supporting longer hex ciphertext strings. (split into blocks and encrypt each)
* Fix some whitespace issues and remove unnecessary imports
* Add hex input and output functionality
* Fix do_crypt function so it only does the (De/En)cryption and passes the binary data back
* Add initial argument parsing ability
* Added Ruby version of the VNC d3des from: http://pentester.jogger.pl/files/des.rb
* Adding VNC password encoding scripts from: http://www.geekademy.com/2010/10/creating-hashed-password-for-vnc.html
