.. ffmpy documentation master file, created by
   sphinx-quickstart on Tue May 31 08:22:14 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ffmpy
=====
ffmpy is a Python wrapper for `FFmpeg <https://ffmpeg.org>`_. It compiles FFmpeg command line from provided arguments and their respective options and excutes it using Python's `subprocess <https://docs.python.org/3/library/subprocess.html>`_.

ffmpy resembles the command line approach FFmpeg uses. It can read from an arbitrary number of input "files" (regular files, pipes, network streams, grabbing devices, etc.) and write into arbitrary number of output "files". See FFmpeg `documentation <https://ffmpeg.org/ffmpeg.html#Synopsis>`_ for further details about how FFmpeg command line options and arguments work.

ffmpy supports FFmpeg `pipe <https://ffmpeg.org/ffmpeg-protocols.html#pipe>`_ protocol. This means that it is possible to pass input data to ``stdin`` and get output data from ``stdout``.

At this moment ffmpy has wrappers for ``ffmpeg`` and ``ffprobe`` commands, but it should be possible to run other FFmpeg tools with it (e.g. ``ffserver``).

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

This takes ``input.mp4`` file in the current directory as the input, changes the video container from MP4 to AVI without changing any other video parameters and creates a new output file ``output.avi`` in the current directory.

Documentation
-------------
.. toctree::
  :maxdepth: 2

  ffmpy
  examples
