from setuptools import setup, find_packages
from ffmpy import __version__

setup(
    name='ffmpy',
    version=__version__,
    description='A simple Python wrapper around ffmpeg',
    long_description=open('README.rst').read(),
    author='Andriy Yurchuk',
    author_email='ay@mntw.re',
    url='https://github.com/Ch00k/ffmpy',
    packages=find_packages(),
)
