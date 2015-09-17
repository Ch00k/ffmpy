from setuptools import setup
from setuptools.command.test import test as TestCommand  # noqa
from ffmpy import __version__


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--verbose']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        raise SystemExit(errcode)


setup(
    name='ffmpy',
    version=__version__,
    description='A simple Python wrapper around ffmpeg',
    long_description=open('README.rst').read(),
    author='Andriy Yurchuk',
    author_email='ay@mntw.re',
    url='https://github.com/Ch00k/ffmpy',
    packages=['ffmpy'],
    platforms='any',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
