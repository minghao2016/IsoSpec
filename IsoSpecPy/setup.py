
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Extension
from distutils import spawn
# To use a consistent encoding
from codecs import open
import os
import glob
import shutil


# For debugging, set the below to True. Run with (sth like): LD_PRELOAD='/usr/lib64/gcc/x86_64-pc-linux-gnu/9.2.0/libasan.so.5.0.0' python ...
use_asan = False

if not os.path.exists("IsoSpec++"):
    try:
        os.symlink("../IsoSpec++", "IsoSpec++")
    except: # OS doesn't support symlinks
        shutil.copytree("../IsoSpec++", "IsoSpec++", symlinks=True)



here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
#with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#    long_description = f.read()

if use_asan:
    cmodule = Extension('IsoSpecCppPy',
                    sources = ['IsoSpec++/unity-build.cpp'],
                    extra_compile_args = '-O0 -g -DISOSPEC_DEBUG -std=c++17 -fsanitize=address'.split(),
                    extra_link_args = '-fsanitize=address'.split()
                    )
else:
    cmodule = Extension('IsoSpecCppPy',
                    sources = ['IsoSpec++/unity-build.cpp'],
                    extra_compile_args = '-mtune=native -march=native -O3 -std=c++17'.split(),
                    )


setup_args = {
#setup(
    'name': 'IsoSpecPy',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    'version': '2.1.3',

    'description': 'Python interface to IsoSpec++ isotopic envelope calculator library',
    'long_description': 'Python interface to IsoSpec++ isotopic envelope calculator library',

    # The project's main homepage.
    'url': 'http://matteolacki.github.io/IsoSpec/',

    # Author details
    'author': 'Mateusz Lacki & Michal Startek',
    'author_email': 'matteo.lacki@gmail.com',

    # Choose your license
    'license': '2-clause BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'classifiers' : [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # What does your project relate to?
    'keywords' : 'isotopic envelope mass spectrometry',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    'packages' : ['IsoSpecPy'],#find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    'install_requires' : ['cffi'],

    'zip_safe' : False,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    'extras_require' : {
       'test': ["pytest", "numpy"]
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    'package_data' : {},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    'data_files' : [], #[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
#    entry_points={
#        'console_scripts': [
#            'sample=sample:main',
#        ],
#    },
    'ext_modules' : [cmodule],
}

import platform
import sys


if 'windows' in platform.system().lower():
    # Probably Anaconda distribution.
    # Of course Windows can't even compile stuff. Install prebuilt C++ lib.
    import copy
    win_setup_args = copy.deepcopy(setup_args)
    win_setup_args['ext_modules'] = []
    win_setup_args['include_package_data'] = True
    setup(**win_setup_args)
elif 'cygwin' in platform.system().lower():
    try:
        import cffi
    except ImportError:
        print("You appear to be using CYGWIN, and CFFI was not found. Please use the Cygwin installer to install the cffi-python package for the appropriate Python version.")
        print("Installing CFFI using pip will most likely NOT work. This is *NOT* a bug in IsoSpecPy.")
        sys.exit(1)
    if spawn.find_executable('clang++') == None:
        print("You appear to be using CYGWIN and clang++ executable was not found. Please install the clang++ package using Cygwin installer.")
        sys.exit(1)
    import distutils
    import distutils.sysconfig
    distutils.sysconfig.get_config_vars() # Precalculate the dict so we can...
    distutils.sysconfig._config_vars['CFLAGS'] = "" # Nuke CFLAGS: they contain gcc stuff not supported by clang

    from distutils.command.build_ext import build_ext
    class build_ext_subclass(build_ext):
        def get_libraries(self, ext):
            return ext.libraries # Override default function which wants to link in libpython on Windows. We're using CFFI and don't need that.
    setup_args['cmdclass'] = {'build_ext' : build_ext_subclass}
    setup(**setup_args)

elif 'darwin' in platform.system().lower():
    # Okay, so OSX is apparently horribly broken. On OSX the "g++" command can be nonexistent and stuff will be compiled with clang++,
    # or g++ can be present and behave sanely, or it can be clang pretending to be g++ and behaving somewhat sanely, or it can be broken
    # clang which needs extra commandline arguments to compile anything that imports stdlib headers. Because hey, it's absolutely normal
    # that C++ compiler should require extra commandline args to compile a "Hello World" program, and of course those commandline options
    # are incompatible with g++ it's pretending to be. Someone at Apple should be tarred and feathered for this. For now we will do
    # some convoluted logic to try to find out experimentally whether "g++" really is g++, or is working clang or is broken clang, and 
    # which flags are needed to compile stuff. Setuptools don't make this easy to do as well...
    #
    # See https://github.com/mciach/wassersteinms/issues/1 for the rationale behind this.

    from distutils.command.build_ext import build_ext
    import subprocess

    class build_ext_subclass(build_ext):
        def build_extensions(self):
            compiler_cmd = "g++" # sane default in case the next stuff crashes...
            try:
                compiler_cmd = self.compiler.compiler_cxx[0]
                compiler_cmd = self.compiler.compiler_so_cxx[0]
            except AttributeError:
                pass

            with open(os.devnull, 'w') as devnull:

                def check_flags(flags_l):
                    cpp_hello_world = '''#include <iostream>

                    int main()
                    {
                        std::cout << "Hello World!" << std::endl;
                    };
                    '''
                    try:
                        proc = subprocess.Popen([compiler_cmd] + ["-x", "c++", "-fsyntax-only", "-"] + flags_l, stdin = subprocess.PIPE, stdout = devnull, stderr = devnull, universal_newlines = True)
                        proc.stdin.write(cpp_hello_world)
                        proc.stdin.flush()
                        proc.stdin.close()
                        ret = proc.wait()
                    except (OSError, IOError):
                        return False

                    print("Check flags:", ret == 0, flags_l)
                    return ret == 0

                if check_flags(["-stdlib=libc++"]):
                    cmodule.extra_compile_args.append("-stdlib=libc++")
                elif check_flags(["-stdlib=libstdc++"]):
                    cmodule.extra_compile_args.append("-stdlib=libstdc++")
                # else just hope for the best, that is, that the compiler isn't broken...
            try:
                super(build_ext_subclass, self).build_extensions()
            except TypeError: # which means we're on Python 2 and *of course* build_ext is an old-style class...
                build_ext.build_extensions(self)

    setup_args['cmdclass'] = {'build_ext' : build_ext_subclass}
    setup(**setup_args)

else:
    # Assuming sane UNIX with a working compiler.
    setup(**setup_args)
