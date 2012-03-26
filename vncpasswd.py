#!/usr/bin/env python

import d3des as d
import argparse
from struct import pack, unpack

def do_crypt(password, decrypt):
    passpadd = (password + '\x00'*8)[:8]
    strkey = ''.join([ chr(x) for x in d.vnckey ])
    key = d.deskey(strkey, decrypt)

    crypted = d.desfunc(passpadd, key)
    print "Encrypted Bin Pass= '%s'" % crypted
    print "Encrypted Hex Pass= '%s'" % crypted.encode('hex')
    return crypted.encode('hex')
    
def main():
    parser = argparse.ArgumentParser(description='Encrypt or Decrypt a VNC password')
    parser.add_argument("-d", "--decrypt", dest="decrypt", action="store_true", default=False, \
            help="Decrypt an obfuscated password.")
    parser.add_argument("-e", "--encrypt", dest="decrypt", action="store_false", default=False, \
            help="Encrypt a plaintext password. (default mode)")
    parser.add_argument("-f", "--file", dest="filename", \
            help="Input or Output to a specified file.")
    parser.add_argument("passwd", nargs='?', \
            help="A password to encrypt")
  
    args = parser.parse_args()
    import sys
    print do_crypt(args.passwd, args.decrypt)

if __name__ == '__main__':
	main()
