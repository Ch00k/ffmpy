ffmpy
=====
ffmpy is the simplest `ffmpeg <http://ffmpeg.org/>`_ wrapper one can imagine. Under the hood it uses Python's `subprocess <https://docs.python.org/2/library/subprocess.html>`_ module to run ffmpeg exeutable. Input can be specified as a file path as well as sent to ``STDIN`` via ffmpeg's `pipe <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_ protocol. Same for output - it can be written to a file or sent to ``STDOUT``.

Installation
------------
Installation is as simple as running::

    ~$ pip install ffmpy

Usage
-----
ffmpy resembles the command line approach ffmpeg uses. It can read from an arbitrary number of input "files" (regular files, pipes, network streams, grabbing devices, etc.) and write into arbitrary number of output "files". See `ffmpeg documentation <https://ffmpeg.org/ffmpeg.html#Synopsis>`_ for further details.
