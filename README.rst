ffmpy
=====
ffmpy is the simplest `ffmpeg <http://ffmpeg.org/>`_ wrapper one can imagine. Under the hood it uses Python's `subprocess <https://docs.python.org/2/library/subprocess.html>`_ module to run ffmpeg exeutable. Input can be specified as a file path as well as sent to ``STDIN`` via ffmpeg's `pipe <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_ protocol. Same for output - it can be written to a file or sent to ``STDOUT``.

Installation
------------
Installation is as simple as running::

    ~$ pip install ffmpy
