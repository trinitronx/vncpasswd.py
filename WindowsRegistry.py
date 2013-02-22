import _winreg as wreg
import cPickle as pickle

class WindowsRegistry:

    def __init__(self, company="RealVNC", project="WinVNC4", write=1):
        """
            Constructor to open registry key

            Returns: handle for registry access

            Example:
            >>> r = WindowsRegistry('Santo Spirito', 'TestKey', write=1)
            >>> isinstance(r, WindowsRegistry)
            True
            
        """
        self.write = write
        self.company = company
        self.project = project
        self.keyname = "Software\\%s\\%s" % (self.company, self.project)

        try:
            self.key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, self.keyname)
        except:
            if self.write:
                self.key = wreg.CreateKey(wreg.HKEY_LOCAL_MACHINE, self.keyname)

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
            'string'
        """
        # TODO: Fix this
        if not self.write:
            raise Exception, "registry is read only"
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
        if not self.write:
            raise Exception, "registry is read only"
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

    def close(self):
        """
            Close the key
        """
        self.key.Close()

    def __del__(self):
        self.close()


if __name__=="__main__":
    import doctest
    r = WindowsRegistry('Santo Spirito', 'TestKey', write=1)
    # Run unit tests
    verbose=True
    doctest.testmod(None, None, None, verbose, True)
    r.close()
