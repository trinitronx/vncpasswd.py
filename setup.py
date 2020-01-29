from distutils.core import setup
import inspect
import os, errno

SETUP_PY_FILENAME = inspect.getframeinfo(inspect.currentframe()).filename
ROOT_DIR          = os.path.dirname(os.path.abspath(SETUP_PY_FILENAME))
README_MD_PATH    = os.path.join(ROOT_DIR, 'README.md')
README_RST_PATH   = os.path.join(ROOT_DIR, 'README.rst')
README_TXT_PATH   = os.path.join(ROOT_DIR, 'README.txt')
VERSION_TXT_PATH  = os.path.join(ROOT_DIR, 'VERSION')

try:
    from m2r import parse_from_file
    readme = parse_from_file(README_MD_PATH)
    f = open(README_RST_PATH,'w')
    f.write(readme)
    f.close()
    os_symlink = getattr(os, "symlink", None)
    if callable(os_symlink):
        try:
            os.symlink(README_RST_PATH, README_TXT_PATH)
        except OSError, e:
            if e.errno == errno.EEXIST:
                os.remove(README_TXT_PATH)
                os.symlink(README_RST_PATH, README_TXT_PATH)
    else:
        f = open(README_TXT_PATH,'w')
        f.write(readme)
        f.close()
except ImportError:
    # m2r may not be installed in user environment
    with open(README_MD_PATH) as f:
        readme = f.read()

with open(VERSION_TXT_PATH, 'r') as f:
        version = f.read().rstrip()

setup(
    name='vncpasswd.py',
    version=version,
    packages=['d3des','WindowsRegistry',],
    license='License :: OSI Approved :: MIT License',
    long_description=readme,
    author='James Cuzella',
    author_email='james.cuzella@lyraphase.com',
    url='https://github.com/trinitronx/vncpasswd.py'
)

