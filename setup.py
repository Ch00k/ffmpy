from setuptools import setup
from setuptools.command.test import test as TestCommand  # noqa
from ffmpy import __version__


setup(
    name='ffmpy',
    version=__version__,
    description='A simple Python wrapper for ffmpeg',
    long_description=open('README.rst').read(),
    author='Andriy Yurchuk',
    author_email='ay@mntw.re',
    license='MIT',
    url='https://github.com/Ch00k/ffmpy',
    py_modules=['ffmpy'],
    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X'
    ],
    keywords='ffmpeg ffprobe wrapper audio video transcoding'
)
