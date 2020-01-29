vncpasswd.py
============
[![Build Status](http://img.shields.io/travis/trinitronx/vncpasswd.py.svg)](https://travis-ci.org/trinitronx/vncpasswd.py)
<noscript><a href="https://liberapay.com/trinitronx/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a></noscript>
[![Downloads](https://img.shields.io/github/downloads/trinitronx/vncpasswd.py/latest/total.svg)](https://github.com/trinitronx/vncpasswd.py/releases/)

Python implementation of vncpasswd, w/decryption abilities & extra features ;-)
Tested on Python 2.7.3.  (Does not currently work with Python 3)

List of Extra Features:
-----------------------

 - File input and output
 - Decryption / Password recovery!
 - Supports RealVNC long passwords!
 - Hex input and output
 - Read/Write to windows RealVNC registry key

Long password decryption tested against RealVNC Enterprise Edition, 
version: _E4.5.3 (r39012)_ 64-bit (x64) unicode

Windows Registry I/O tested on Windows 7 x64 Professional

Python Installation:
-------------------

This python script was built with and only supports Python 2! If you are from the future, or accessing this via the [GitHub Arctic Code Vault 02/02/2020][5], First of all... congratulations on surviving!  If this code is useful to you, you may need to obtain a version of Python 2.7.  Alternatively, you may use the Python `2to3` utility to convert this source code for use with Python 3 (may take some testing & development to get working on all platforms).

To install Python 2.7.17 (Latest version as of 01/28/2020. Python 2 End of Life was 01/01/2020):

### macOS / Linux:
If your system does not have an available `python2` in `PATH` linked:

    # Make sure you have build dependencies installed on your platform:
    # For example: GNU make, gcc / g++ compiler, build-essential package, etc...
    # Find and/or download Python 2.7
    curl -L -o /tmp/python-v2.7.17.tar.gz https://github.com/python/cpython/archive/v2.7.17.tar.gz
    tar -xvf /tmp/python-v2.7.17.tar.gz
    cd cpython-2.7.17/
    ./configure
    make
    sudo make install
    # OR: sudo make altinstall
    
    # Symlink `python2` to the resulting python2.7 binary
    # For example:
    ln -sf /usr/local/bin/python2.7 /usr/local/bin/python2


### Windows:

Please refer to the [`python/cpython/PCbuild/readme.txt`][6] for Windows-specific build instructions (Microsoft Visual Studio 2017).  The basic idea is to make sure you have build & compilation dependencies installed for Windows platform, and run the `build.bat` script.

Excerpt:

> Building Python using the build.bat script
> ----------------------------------------------
> 
> In this directory you can find build.bat, a script designed to make
> building Python on Windows simpler.  This script will use the env.bat
> script to detect either Visual Studio 2017 or 2015, either of
> which may be used to build Python. Currently Visual Studio 2017 is
> officially supported.
> 
> By default, build.bat will build Python in Release configuration for
> the 32-bit Win32 platform.  It accepts several arguments to change
> this behavior, try `build.bat -h` to learn more.

Installation:
-------------

This project installs from source via:

    git clone https://github.com/trinitronx/vncpasswd.py.git vncpasswd.py
    cd vncpasswd.py
    python2 ./vncpasswd.py --help

Note: The "shebang" line at the top of the python script is: `#!/usr/bin/env python2`

If you have `python2`, and `/usr/bin/env` binaries available in your system's `PATH`, you should be all set up to just run the executable script file as-is: `./vncpasswd.py`

To build a Docker image, or Python Source Distribution, see below or run `make help` to see all available `Makefile` targets.

Usage:
------

The `help` output explains the command line flags:

> usage: vncpasswd.py [-h] [-d] [-e] [-H] [-R] [-f FILENAME] [-t] [passwd]
> 
> Encrypt or Decrypt a VNC password
> 
> positional arguments:
>   passwd                A password to encrypt
> 
> optional arguments:
>   -h, --help            show this help message and exit
>   -d, --decrypt         Decrypt an obfuscated password.
>   -e, --encrypt         Encrypt a plaintext password. (default mode)
>   -H, --hex             Assume input is in hex.
>   -R, --registry        Input or Output to the windows registry.
>   -f FILENAME, --file FILENAME
>                         Input or Output to a specified file.
>   -t, --test            Run the unit tests for this program.

### Docker:

The docker container is ready-built with all dependencies needed.  Just mount in your file (e.g.: `-v $HOME/.vnc/:$HOME/.vnc`, or just `-v $HOME:$HOME`), and run:

    # Decrypt ~/.vnc/passwd
    docker run -ti -v $HOME:$HOME -w $HOME  trinitronx/vncpasswd.py -d -f ~/.vnc/passwd
    
    # More Examples:
    # Encrypt string 'foo'
    docker run  -v $HOME:$HOME -w $HOME -ti trinitronx/vncpasswd.py -e 'foo'
    # Encrypt string 'bar' and output to ~/.vnc/passwd
    mkdir -p $HOME/.vnc/
    docker run  -v $HOME:$HOME -w $HOME -ti trinitronx/vncpasswd.py -e 'foo' -f ~/.vnc/passwd
    # Encrypt string 'bar' as HEX input
    docker run  -v $HOME:$HOME -w $HOME -ti trinitronx/vncpasswd.py -e -H '6261720000000000'
    # Decrypt the encrypted password 'bar' as HEX input
    docker run  -v $HOME:$HOME -w $HOME -ti trinitronx/vncpasswd.py -d -H '9ca3f3686574f277'

Testing:
--------

This project used TravisCI for Continuous Integration & Continuous Deployment to Docker Hub.  The `.travis.yml` contains the build steps.  To test this project, install build dependencies & run the tests:

    pip install --user -r ./build/build-requirements.txt
    make test

Python Source Distribution:
---------------------------

To create a python source distribution via `setuptools`:

    make setup

Docker Image Build:
-------------------

Make sure you have Docker installed on your system, and run:

    make package

DockerHub / Repository Image Ship:
----------------------------------

To ship this image to either DockerHub, or your Docker Image repository of choice, just export the following variables:

    DOCKER_USERNAME=your-username
    DOCKER_PASSWORD=your-password

Then run:

    # DockerHub by default
    make ship
    
    # Alternate Repository
    #  Override & export these variables set in `./build/main.mk`:
    #    REGISTRY    ?= docker.io
    #    REPO_NAME   ?= $(BIN)
    #    REPO        ?= $(REGISTRY)/trinitronx/$(REPO_NAME)
    export REGISTRY=quay.io
    export REPO_NAME=your-reponame
    export USERNAME=your-username
    export REPO=$REGISTRY/$USERNAME/$REPO_NAME
    make ship


Thanks / Props
--------------

Many thanks to the original authors of the d3des libary
(Richard Outerbridge, Dan Hoey, Jim Gillogly, Phil Karn, et. al.), 
and it's python rewrite (Yusuke Shinyama)!
Thanks to Mike Miller for his great [blog post][1] on how he used the d3des.py library.
Thanks to Darren McCall for his wonderful collection of [RealVNC Registry Hacks][2]
And finally...
Thanks to God for the inspiration to reverse engineer RealVNC's multi-block 
method for encrypting long passwords ;-D
(Long story... recovering my *long* RealVNC password saved a bunch of my data!)


Disclaimer:
-----------

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Please only use this software for Good, and don't harm directly or indirectly living beings


References:
-----------

 - [Creating a Hashed Password for VNC][1]
 - [RealVNC Password Hacking][2]
 - [Email Thread: Registry Edit to define server password][3]
 - [Email Thread on User vs. System passwords: Password Shift][4]

[1]: http://www.geekademy.com/2010/10/creating-hashed-password-for-vnc.html
    "Creating a Hashed Password for VNC"
[2]: http://darrenmccall.com/blog/2010/04/30/realvnc-password-hacking/
    "RealVNC Password Hacking"
[3]: http://www.realvnc.com/pipermail/vnc-list/2002-November/035748.html
    "Email Thread: Registry Edit to define server password"
[4]: http://www.realvnc.com/pipermail/vnc-list/2002-August/033007.html
    "Email Thread on User vs. System passwords: Password Shift"
[5]: https://archiveprogram.github.com/#arctic-code-vault
    "GitHub Archive Program: Preserving open source software for future generations (Get your code into the GitHub Arctic Code Vault 02/02/2020)"
[6]: https://github.com/python/cpython/tree/master/PCbuild
    "Building cPython on Windows: PCBuild/readme.txt"