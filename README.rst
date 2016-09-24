.. image:: https://img.shields.io/pypi/v/ffmpy.svg
    :target: https://pypi.python.org/pypi/ffmpy
    :alt: Latest version

.. image:: https://travis-ci.org/Ch00k/ffmpy.svg?branch=master
    :target: https://travis-ci.org/Ch00k/ffmpy
    :alt: Travis-CI

.. image:: https://readthedocs.org/projects/ffmpy/badge/?version=latest
    :target: http://ffmpy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


ffmpy
=====
ffmpy is a simplystic `FFmpeg <http://ffmpeg.org/>`_ command line wrapper. It implements a Pythonic interface for FFmpeg command line compilation and uses Python `subprocess <https://docs.python.org/2/library/subprocess.html>`_ module to execute compiled command line.

Installation
------------
You guessed it::

  pip install ffmpy

Quick example
-------------
.. code:: python

  >>> import ffmpy
  >>> ff = ffmpy.FFmpeg(
  ...     inputs={'input.mp4': None},
  ...     outputs={'output.avi': None}
  ... )
  >>> ff.run()

This will take ``input.mp4`` file in the current directory as the input, change the video container from MP4 to AVI without changing any other video parameters and create a new output file ``output.avi`` in the current directory.

Documentation
-------------
http://ffmpy.readthedocs.io/en/latest

See `Examples <http://ffmpy.readthedocs.io/en/latest/examples.html>`_ section for usage examples.
