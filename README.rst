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
ffmpy is the simplest `ffmpeg <http://ffmpeg.org/>`_ wrapper one can imagine. Under the hood it uses Python's `subprocess <https://docs.python.org/2/library/subprocess.html>`_ module to run ffmpeg executable.

Installation
------------
You guessed it::

  pip install ffmpy

Quick example
-------------
::

  import ffmpy
  ff = ffmpy.FFmpeg(
      inputs={'input.mp4': None},
      outputs={'output.avi': None}
  )
  ff.run()

This will take ``input.mp4`` file in the current directory as the input, change the video container from MP4 to AVI without changing any other video parameters and create a new output file ``output.avi`` in the current directory.

Documentation
-------------
http://ffmpy.readthedocs.io/en/latest
