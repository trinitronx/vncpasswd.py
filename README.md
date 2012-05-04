vncpasswd.py
============

Python implementation of vncpasswd, w/decryption abilities & extra features ;-)

List of Extra Features:
-----------------------

 - File input and output
 - Decryption / Password recovery!
 - Supports RealVNC long passwords!
 - Hex input and output

Long password decryption tested against RealVNC Enterprise Edition, 
version: _E4.5.3 (r39012)_ 64-bit (x64) unicode

Thanks / Props
--------------

Many thanks to the original authors of the d3des libary
(Richard Outerbridge, Dan Hoey, Jim Gillogly, Phil Karn, et. al.), 
and it's python rewrite (Yusuke Shinyama)!
Thanks to Darren McCall for his wonderful collection of [RealVNC Registry Hacks][1]
And finally...
Thanks to God for the inspiration to reverse engineer RealVNC's multi-block 
method for encrypting long passwords ;-D
(Long story... recovering my *long* RealVNC password saved a bunch of my data!)

References:
[1]: http://darrenmccall.com/blog/2010/04/30/realvnc-password-hacking/
    "RealVNC Password Hacking"
