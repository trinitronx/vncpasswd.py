vncpasswd.py
============

[![Build Status](https://travis-ci.org/trinitronx/vncpasswd.py.png?branch=master)](https://travis-ci.org/trinitronx/vncpasswd.py)

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
