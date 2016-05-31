.. ffmpy documentation master file, created by
   sphinx-quickstart on Tue May 31 08:22:14 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ffmpy
=====
ffmpy is a Python wrapper for ffmpeg. It compiles ffmpeg command line from provided arguments and options and runs it using Python's `subprocess <https://docs.python.org/3/library/subprocess.html>`_.

ffmpy resembles the command line approach ffmpeg uses. It can read from an arbitrary number of input "files" (regular files, pipes, network streams, grabbing devices, etc.) and write into arbitrary number of output "files". See `ffmpeg documentation <https://ffmpeg.org/ffmpeg.html#Synopsis>`_ for further details about how ffmpeg command line options and arguments work.

ffmpy supports ffmpeg's `pipe <https://ffmpeg.org/ffmpeg-protocols.html#pipe>`_ protocol. This means that it is possible to pass input data to ``STDIN`` and get output data from ``STDOUT``.

At this moment ffmpy has wrappers for both ``ffmpeg`` and ``ffprobe``.

Installation
------------
::

  pip install ffmpy

Quickstart
----------
::

  import ffmpy
  ff = ffmpy.FFmpeg(
      inputs={'input.mp4': None},
      outputs={'output.avi': None}
  )
  ff.run()

This will change the video format from MP4 to AVI without changing any other video parameters.


Documentation
-------------
.. toctree::
  :maxdepth: 2

  ffmpy
  examples
