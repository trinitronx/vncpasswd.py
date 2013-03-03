#!/usr/bin/env python

#import sys
import d3des as d
import WindowsRegistry as wreg
import argparse
#from struct import pack, unpack

def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

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
        data = data.strip()
        data = unhex(data)
    return data

def do_file_out(filename, data, inhex):
    f = open(filename, 'w')
    if ( inhex ):
	    data = data.encode('hex')
    f.write(data)
    f.close()

def unhex(s):
    try:
        s = s.decode('hex')
    except TypeError as e:
        if e.message == 'Odd-length string':
            print 'WARN: %s . Chopping last char off... "%s"' % ( e.message, s[:-1] )
            s = s[:-1].decode('hex')
        else:
            raise
    return s


def main():
    parser = argparse.ArgumentParser(description='Encrypt or Decrypt a VNC password')
    parser.add_argument("-d", "--decrypt", dest="decrypt", action="store_true", default=False, \
            help="Decrypt an obfuscated password.")
    parser.add_argument("-e", "--encrypt", dest="decrypt", action="store_false", default=False, \
            help="Encrypt a plaintext password. (default mode)")
    parser.add_argument("-H", "--hex", dest="hex", action="store_true", default=False, \
            help="Assume input is in hex.")
    parser.add_argument("-R", "--registry", dest="registry", action="store_true", default=False, \
            help="Input or Output to the windows registry.")
    parser.add_argument("-f", "--file", dest="filename", \
            help="Input or Output to a specified file.")
    parser.add_argument("passwd", nargs='?', \
            help="A password to encrypt")

    args = parser.parse_args()
    if ( args.filename == None and args.passwd == None and args.registry == False ):
        parser.error('Error: No password file or password passed\n')
    if ( args.registry and args.decrypt ):
        reg = wreg.WindowsRegistry("RealVNC", "WinVNC4")
        ( args.passwd, key_type) = reg.getval("Password")
    if ( args.passwd != None and args.hex ):
        args.passwd = unhex(args.passwd)
    if ( args.filename != None and args.decrypt ):
        args.passwd = do_file_in(args.filename, args.hex)

    # If the hex encoded passwd length is longer than 16 hex chars and divisible
    # by 16, then we chop the passwd into blocks of 64 bits (16 hex chars)
    # (1 hex char = 4 binary bits = 1 nibble)
    hexpasswd = args.passwd.encode('hex')
    if ( len(hexpasswd) > 16 and (len(hexpasswd) % 16) == 0 ):
        print 'INFO: Detected ciphertext > 64 bits... breaking into blocks to decrypt...'
        splitstr = split_len(args.passwd.encode('hex'), 16)
        print 'INFO: Split blocks = %s' % splitstr
        cryptedblocks = []
        for sblock in splitstr:
            cryptedblocks.append( do_crypt(sblock.decode('hex'), args.decrypt) )
            #print '%016s\t%s' % ( sblock, cryptedblocks )
            crypted = ''.join(cryptedblocks)
    elif ( len(hexpasswd) <= 16):
        crypted = do_crypt(args.passwd, args.decrypt)
    else:
        if ( args.decrypt ):
            print 'WARN: Ciphertext length was not divisible by 8 (hex/16).'
            print 'Length: %d' % len(args.passwd)
            print 'Hex Length: %d' % len(hexpasswd)
        crypted = do_crypt(args.passwd, args.decrypt)

    if ( args.filename != None and not args.decrypt ):
        do_file_out(args.filename, crypted, args.hex)
    if ( args.registry and not args.decrypt ):
        reg = wreg.WindowsRegistry("RealVNC", "WinVNC4")
        reg.setval('Password', crypted, wreg.WindowsRegistry.REG_BINARY)

    prefix = ('En','De')[args.decrypt == True]
    print "%scrypted Bin Pass= '%s'" % ( prefix, crypted )
    print "%scrypted Hex Pass= '%s'" % ( prefix, crypted.encode('hex') )

if __name__ == '__main__':
	main()
