#!/usr/bin/env python

#import sys
import d3des as d
import argparse
#from struct import pack, unpack

def do_crypt(password, decrypt):
    passpadd = (password + '\x00'*8)[:8]
    strkey = ''.join([ chr(x) for x in d.vnckey ])
    key = d.deskey(strkey, decrypt)
    crypted = d.desfunc(passpadd, key)
    return crypted

def do_file_in(filename, inhex):
    f = open(filename, 'r')
    data = f.read()
    f.close()
    if ( inhex ):
        data = data.decode('hex')
    return data

def do_file_out(filename, data, inhex):
    f = open(filename, 'w')
    if ( inhex ):
	    data = data.encode('hex')
    f.write(data)
    f.close()

def main():
    parser = argparse.ArgumentParser(description='Encrypt or Decrypt a VNC password')
    parser.add_argument("-d", "--decrypt", dest="decrypt", action="store_true", default=False, \
            help="Decrypt an obfuscated password.")
    parser.add_argument("-e", "--encrypt", dest="decrypt", action="store_false", default=False, \
            help="Encrypt a plaintext password. (default mode)")
    parser.add_argument("-H", "--hex", dest="hex", action="store_true", default=False, \
            help="Assume input is in hex.")
    parser.add_argument("-f", "--file", dest="filename", \
            help="Input or Output to a specified file.")
    parser.add_argument("passwd", nargs='?', \
            help="A password to encrypt")

    args = parser.parse_args()
    if ( args.filename == None and args.passwd == None ):
        parser.error('Error: No password file or password passed\n')
    if ( args.passwd != None and args.hex ):
	    args.passwd = args.passwd.decode('hex')
    if ( args.filename != None and args.decrypt ):
        args.passwd = do_file_in(args.filename, args.hex)

    crypted = do_crypt(args.passwd, args.decrypt)

    if ( args.filename != None and not args.decrypt ):
        do_file_out(args.filename, crypted, args.hex)

    prefix = ('En','De')[args.decrypt == True]
    print "%scrypted Bin Pass= '%s'" % ( prefix, crypted )
    print "%scrypted Hex Pass= '%s'" % ( prefix, crypted.encode('hex') )

if __name__ == '__main__':
	main()
