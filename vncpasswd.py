#!/usr/bin/env python2

"""vncpasswd.py: Python implementation of vncpasswd, w/decryption abilities & extra features ;-)"""

__author__      = "James Cuzella"
__copyright__   = "Copyright 2012,2013, James Cuzella"
__credits__ = [ 'Yusuke Shinyama', 'Richard Outerbridge', 'Dan Hoey', 'Jim Gillogly', 'Phil Karn' ]
__license__ = "MIT"
__version__ = "1.2.1"
__maintainer__ = "James Cuzella"

import sys
import argparse
import platform
#from struct import pack, unpack

from d3des import d3des as d
if platform.system().startswith('Windows'): from WindowsRegistry import WindowsRegistry as wreg

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
    """
    Decodes a string of hex characters

    Return: This method returns an decoded version of the string.
    If a hexidecimal string with odd length is passed, the last character is chopped off and the decoded version of this is returned.

    Example:
        >>> unhex("48656c6c6f20576f726c64")
        'Hello World'
        >>> unhex("48656c6c6f20576f726c6")
        WARN: Odd-length string . Chopping last char off... "48656c6c6f20576f726c"
        'Hello Worl'
        >>> unhex('303132333435363738396162636465666768696a6b6c6d6e6f707172737475767778797a4142434445464748494a4b4c4d4e4f505152535455565758595a2122232425262728292a2b2c2d2e2f3a3b3c3d3e3f405b5c5d5e5f607b7c7d7e20090a0d0b0c')
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\\'()*+,-./:;<=>?@[\\\\]^_`{|}~ \\t\\n\\r\\x0b\\x0c'
        >>> unhex('000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F')
        '\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b\\x0c\\r\\x0e\\x0f\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x18\\x19\\x1a\\x1b\\x1c\\x1d\\x1e\\x1f'
        >>> unhex('abcdefghijklmnop')
        Traceback (most recent call last):
          File "/usr/lib/python2.7/doctest.py", line 1289, in __run
            compileflags, 1) in test.globs
          File "<doctest __main__.unhex[2]>", line 1, in <module>
            unhex('abcdefghijklmnop')
          File "./vncpasswd.py", line 51, in unhex
            s = s.decode('hex')
          File "/usr/lib/python2.7/encodings/hex_codec.py", line 42, in hex_decode
            output = binascii.a2b_hex(input)
        TypeError: Non-hexadecimal digit found
    """
    try:
        s = s.decode('hex')
    except TypeError as e:
        if e.message == 'Odd-length string':
            print 'WARN: %s . Chopping last char off... "%s"' % ( e.message, s[:-1] )
            s = s[:-1].decode('hex')
        else:
            raise
    return s

def run_tests(verbose=False):
    print "Running Unit Tests..."
    import doctest
    import __main__
    (failure_count, test_count) = doctest.testmod(None, None, None, verbose, True)
    pass_count = test_count - failure_count

    methods = dir(__main__)
    ignore_methods = ['__builtins__', '__doc__', '__file__', '__name__', '__package__', '__warningregistry__', 'argparse', 'sys' ]
    methods = [i for i in methods if not i in ignore_methods or ignore_methods.remove(i)]

    print '%d tests in %s items.' % ( test_count, len(methods) )
    if failure_count > 0:
        print '%d out of %d tests failed' % (failure_count, test_count)
    else:
        print '%d passed and %d failed.' % ( pass_count, failure_count )
        print 'Test passed.'
    sys.exit(failure_count)

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
    parser.add_argument("-t", "--test", dest="test", action="store_true", default=False, \
            help="Run the unit tests for this program.")

    args = parser.parse_args()
    if (args.test):
        run_tests()

    if ( args.filename == None and args.passwd == None and (args.registry == False or not platform.system().startswith('Windows')) ):
        parser.error('Error: No password file or password passed\n')
    if ( args.registry and args.decrypt and platform.system().startswith('Windows')):
        reg = get_realvnc_key()
        ( args.passwd, key_type) = reg.getval("Password")
    elif not platform.system().startswith('Windows'):
        print 'Cannot read from Windows Registry on a %s system' % platform.system()
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
    if ( args.registry and not args.decrypt and platform.system().startswith('Windows')):
        reg = get_realvnc_key()
        reg.setval('Password', crypted, wreg.WindowsRegistry.REG_BINARY)
    elif not platform.system().startswith('Windows'):
        print 'Cannot write to Windows Registry on a %s system' % platform.system()

    prefix = ('En','De')[args.decrypt == True]
    print "%scrypted Bin Pass= '%s'" % ( prefix, crypted )
    print "%scrypted Hex Pass= '%s'" % ( prefix, crypted.encode('hex') )


def get_realvnc_key():
    reg = None

    for k in ['vncserver', 'WinVNC4',]:
        try:
            reg = wreg.WindowsRegistry('RealVNC', k)
            break
        except WindowsError as e:
            if 'The system cannot find the file specified' in str(e):
                pass
            else:
                raise e

    return reg


if __name__ == '__main__':
	main()
