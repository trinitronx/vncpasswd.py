import sys
import _winreg as wreg
import cPickle as pickle
import platform

class WindowsRegistry:
    """ A class to simplify read/write access to the Windows Registry """
    __author__      = "James Cuzella"
    __copyright__   = "Copyright 2012,2013, James Cuzella"
    __credits__ = [ 'Based on a class by', 'Dirk Holtwick', 'http://code.activestate.com/recipes/146305-windows-registry-for-dummies/' ]
    __license__ = "MIT"

    # Registry Data types
    REG_NONE                = wreg.REG_NONE          # No value type
    REG_SZ                  = wreg.REG_SZ            # Unicode nul terminated string
    REG_EXPAND_SZ           = wreg.REG_EXPAND_SZ     # Unicode nul terminated string
                                                     # (with environment variable references)
    REG_BINARY              = wreg.REG_BINARY        #   // Free form binary
    REG_DWORD               = wreg.REG_DWORD         #   // 32-bit number
    REG_DWORD_LITTLE_ENDIAN = wreg.REG_DWORD_LITTLE_ENDIAN #   // 32-bit number (same as REG_DWORD)
    REG_DWORD_BIG_ENDIAN    = wreg.REG_DWORD_BIG_ENDIAN    #   // 32-bit number
    REG_LINK                = wreg.REG_LINK          #   // Symbolic Link (unicode)
    REG_MULTI_SZ            = wreg.REG_MULTI_SZ      #   // Multiple Unicode strings
    REG_RESOURCE_LIST       = wreg.REG_RESOURCE_LIST #   // Resource list in the resource map
    REG_FULL_RESOURCE_DESCRIPTOR = wreg.REG_FULL_RESOURCE_DESCRIPTOR # Resource list in the hardware description
    REG_RESOURCE_REQUIREMENTS_LIST  = wreg.REG_RESOURCE_REQUIREMENTS_LIST

    RIGHTSDICT = {  wreg.KEY_ALL_ACCESS: 'KEY_ALL_ACCESS', wreg.KEY_WRITE: 'KEY_WRITE', wreg.KEY_READ: 'KEY_READ', wreg.KEY_QUERY_VALUE: 'KEY_QUERY_VALUE', wreg.KEY_SET_VALUE: 'KEY_SET_VALUE', wreg.KEY_CREATE_SUB_KEY: 'KEY_CREATE_SUB_KEY', wreg.KEY_ENUMERATE_SUB_KEYS: 'KEY_ENUMERATE_SUB_KEYS' }
    RIGHTS_WRITABLE = [ wreg.KEY_ALL_ACCESS, wreg.KEY_WRITE, wreg.KEY_CREATE_SUB_KEY, wreg.KEY_SET_VALUE ]
        
    def __init__(self, company="RealVNC", project="WinVNC4", create=0):
        """
            Constructor to open registry key

            Returns: handle for registry access

            Examples:
            >>> r = WindowsRegistry('Microsoft', 'Windows')
            >>> isinstance(r, WindowsRegistry)
            True
            >>> r = WindowsRegistry('Santo Spirito', 'TestKey', create=1)
            >>> isinstance(r, WindowsRegistry)
            True
            >>> r.key.__class__
            <type 'PyHKEY'>
            
        """
        self.create = create
        self.company = company
        self.project = project
        self.keyname = "Software\\%s\\%s" % (self.company, self.project)
        self.key = None
        self.can_write = False
        self.right = None

        rights = [ wreg.KEY_ALL_ACCESS, wreg.KEY_WRITE, wreg.KEY_READ, wreg.KEY_CREATE_SUB_KEY, wreg.KEY_SET_VALUE, wreg.KEY_ENUMERATE_SUB_KEYS, wreg.KEY_QUERY_VALUE ]
        
        not_opened = True
        i=0
        while not_opened and i<len(rights)-1:
            try:
                if platform.machine().endswith('64') and platform.architecture()[0] == '32bit':
                    self.key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, self.keyname, 0, rights[i] | wreg.KEY_WOW64_64KEY)
                else:
                    self.key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, self.keyname,0, rights[i])
                not_opened = False
                self.right = rights[i]
                #print "rights = %05x" % rights[i]
                #print "Rights were: %s" % WindowsRegistry.RIGHTSDICT[rights[i]]
                #print "self.key = %s" % self.key
            except WindowsError as e:
                if self.create:
                    try:
                        self.key = wreg.CreateKeyEx(wreg.HKEY_LOCAL_MACHINE, self.keyname,0, rights[i])
                        not_opened = False
                        self.right = rights[i]
                    except WindowsError:
                        pass
                #print "Error: ", sys.exc_info()[0]
                #print "%s" % e.strerror
                #print i
                #print "Tried rights = %s (0x%x)" % ( WindowsRegistry.RIGHTSDICT[rights[i]], rights[i] )
                i=i+1
        if self.key == None:
            print e.strerror
            print "Failed to open Registry with rights = %s (0x%x)" % ( WindowsRegistry.RIGHTSDICT[rights[i]], rights[i] )
            print "Try running as Administrator?"
            raise e
        if self.right in WindowsRegistry.RIGHTS_WRITABLE:
            self.can_write = True

    def getval(self, name):
        """ Get value for key in registry """
        return wreg.QueryValueEx(self.key, name)
    
    def get_subkey(self, name):
        " Get subkey (Default) value out of registry "
        return wreg.QueryValue(self.key, name)

    def pget_subkey(self, name):
        " Get subkey (Default) value using pickle "
        return pickle.loads(self.get_subkey(name))
    
    def setval(self, name, value, value_type=wreg.REG_SZ):
        """
            Set value for key in registry

            Examples:
            >>> r.setval('test_stringval', 'string')
            >>> r.getval('test_stringval')
            (u'string', 1)
        """
        if not self.can_write:
            raise WindowsError, "Registry opened with read-only rights %s (0x%x)" % ( WindowsRegistry.RIGHTSDICT[self.right], self.right )
        if value_type == wreg.REG_SZ:
            value = str(value)
        wreg.SetValueEx(self.key, name, 0, value_type, value)
        
    def set_subkey(self, subkey_name, value):
        """
            Set subkey (Default) value in registry

            Example:
            >>> r.set_subkey('test', 'test_str')
            >>> r.get_subkey('test')
            'test_str'
        """
        if not self.can_write:
            raise WindowsError, "Registry opened with read-only rights %s (0x%x)" % ( WindowsRegistry.RIGHTSDICT[self.right], self.right )
        wreg.SetValue(self.key, subkey_name, wreg.REG_SZ, str(value))

    def pset_subkey(self, name, value):
        """
            Store python ojbect into subkey (Default) value using pickle

            Examples:
            >>> r.pset_subkey("testp_int", 123)
            >>> r.pget_subkey("testp_int")
            123
            >>> r.pset_subkey("testp_str", "string")
            >>> r.pget_subkey("testp_str")
            'string'
            >>> r.pset_subkey("testp_bool", True)
            >>> r.pget_subkey("testp_bool")
            True
            >>> r.pset_subkey("testp_float", 1.0)
            >>> r.pget_subkey("testp_float")
            1.0
            >>> r.pset_subkey("testp_complex", 1+1.0j)
            >>> r.pget_subkey("testp_complex")
            (1+1j)
            >>> r.pset_subkey("testp_unicode", u'unicodestr')
            >>> r.pget_subkey("testp_unicode")
            u'unicodestr'
            >>> r.pset_subkey("testp_tuple", (1, 2, 3, 'string'))
            >>> r.pget_subkey("testp_tuple")
            (1, 2, 3, 'string')
        """
        self.set_subkey(name, pickle.dumps(value))

    def del_subkey(self, subkey_name):
        """
            Delete the specified subkey

            Example:
            >>> r.pset_subkey('test_remove_subkey', 'removeme')
            >>> r.del_subkey('test_remove_subkey')
            >>> try:
            ...     r.pget_subkey('test_remove_subkey')
            ... except WindowsError:
            ...     print 'delete success'
            delete success
        """
        if not self.can_write:
            raise WindowsError, "Registry opened with read-only rights %s (0x%x)" % ( WindowsRegistry.RIGHTSDICT[self.right], self.right )
        wreg.DeleteKey(self.key, subkey_name)
    def delval(self, name):
        """
            Delete the specified value

            Example:
            >>> r.setval('test_remove_stringval', 'removeme')
            >>> r.delval('test_remove_stringval')
            >>> try:
            ...     r.getval('test_remove_stringval')
            ... except WindowsError:
            ...     print 'delete success'
            delete success
        """
        if not self.can_write:
            raise WindowsError, "Registry opened with read-only rights %s (0x%x)" % ( WindowsRegistry.RIGHTSDICT[self.right], self.right )
        wreg.DeleteValue(self.key, name)
    def close(self):
        """
            Close the key
        """
        if self.key:
            self.key.Close()

    def __del__(self):
        self.close()


if __name__=="__main__":
    import doctest
    try:
        r = WindowsRegistry('Santo Spirito', 'TestKey', create=1)
        # Run unit tests
        verbose=False
        doctest.testmod(None, None, None, verbose, True)
        if r.key: print "Registry opened with: %s (0x%x)" % ( WindowsRegistry.RIGHTSDICT[r.right], r.right )
        r.del_subkey('test')
        r.del_subkey("testp_int")
        r.del_subkey("testp_str")
        r.del_subkey("testp_bool")
        r.del_subkey("testp_float")
        r.del_subkey("testp_complex")
        r.del_subkey("testp_unicode")
        r.del_subkey("testp_tuple")
        r.delval('test_stringval')
        
        # Cleanup the subkeys that the instance can't access
        wreg.DeleteKey(wreg.HKEY_LOCAL_MACHINE, r.keyname)
        wreg.DeleteKey(wreg.HKEY_LOCAL_MACHINE, 'Software\\Santo Spirito')
        r.close()
    except WindowsError as e:
        pass
