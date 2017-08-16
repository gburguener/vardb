from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import sys
import VARDB


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)  # @UndefinedVariable
        sys.exit(errcode)

setup(
    name='sandman',
    version=VARDB.__version__,
    url='https://github.com/gburguener/vardb',
    license='MIT License',
    author='German Burguener, Ezequiel Sosa',
    tests_require=['pytest'],
    install_requires=['peewee>=2.8.5',
                    ],
    cmdclass={'test': PyTest},
    author_email='germanburguener@gmail.com,ezequieljsosa@gmail.com',
    description='Variant analysis toolkit',
    long_description=long_description,
    packages=['VARDB'],
    include_package_data=True,
    platforms='any',
    test_suite='test.test_queries',
    classifiers = [
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',

        ],
    extras_require={
        'testing': ['pytest'],
    }
)