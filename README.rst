.. image:: https://img.shields.io/pypi/v/ffmpy.svg
    :target: https://pypi.python.org/pypi/ffmpy
    :alt: Latest version

.. image:: https://img.shields.io/travis/Ch00k/ffmpy.svg
    :target: https://travis-ci.org/Ch00k/ffmpy
    :alt: Travis-CI


ffmpy
=====
ffmpy is the simplest `ffmpeg <http://ffmpeg.org/>`_ wrapper one can imagine. Under the hood it uses Python's `subprocess <https://docs.python.org/2/library/subprocess.html>`_ module to run ffmpeg exeutable. In other words it's a (bit) more user-friendly interface to compiling a command line to be passed to subprocess. Input can be specified as a file path as well as sent to ``STDIN`` via ffmpeg's `pipe <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_ protocol. Same for output - it can be written to a file or sent to ``STDOUT``.

Installation
------------
You guessed it::

    ~$ pip install ffmpy

Usage
-----
ffmpy resembles the command line approach ffmpeg uses. It can read from an arbitrary number of input "files" (regular files, pipes, network streams, grabbing devices, etc.) and write into arbitrary number of output "files". See `ffmpeg documentation <https://ffmpeg.org/ffmpeg.html#Synopsis>`_ for further details about how ffmpeg command line options and arguments work.

The simplest example of usage is converting media from one format to another (in this case from MPEG transport stream to MP4) preserving all other attributes:

.. code:: python

    In [1]: ff = FFmpeg(inputs={'/tmp/input.ts': None}, outputs={'/tmp/output.mp4': None})
    In [2]: ff.cmd_str
    Out[2]: 'ffmpeg -i /tmp/input.ts /tmp/output.mp4'
    In [3] ff.run()

If at the same time we wanted to re-encode video and audio using different codecs we'd have to specify additional output options:

.. code:: python

    In [1]: ff = FFmpeg(inputs={'/tmp/input.ts': None}, outputs={'/tmp/output.mp4': '-c:a mp2 -c:v mpeg2video'})
    In [2]: ff.cmd_str
    Out[2]: 'ffmpeg -i /tmp/input.ts -c:a mp2 -c:v mpeg2video /tmp/output.mp4'
    In [3] ff.run()

A more complex usage example would be demultiplexing an MPEG transport stream into separate elementary (audio and video) streams and save them in MP4 containers preserving the codecs:

.. code:: python

    In [1]: ff = FFmpeg(inputs={'/tmp/input.ts': None}, outputs={'/tmp/video.mp4': '-map 0:0 -c:a copy -f mp4', '/tmp/audio.mp4': '-map 0:1 -c:a copy -f mp4'})
    In [2]: ff.cmd_str
    Out[2]: 'ffmpeg -i /tmp/input.ts -map 0:1 -c:a copy -f mp4 /tmp/audio.mp4 -map 0:0 -c:a copy -f mp4 /tmp/video.mp4'
    In [3] ff.run()

To multiplex video and audio back into an MPEG transport stream with re-encoding:

.. code:: python

    In [1]: ff = FFmpeg(inputs={'/tmp/video.mp4': None, '/tmp/audio.mp4': None}, outputs={'/tmp/output.ts': '-c:v h264 -c:a ac3'})
    In [2]: ff.cmd_str
    Out[2]: 'ffmpeg -i /tmp/audio.mp4 -i /tmp/video.mp4 -c:v h264 -c:a ac3 /tmp/output.ts'
    In [3] ff.run()

There are cases where the order of inputs and outputs must be preserved (e.g. when using ffmpeg's `-map <https://trac.ffmpeg.org/wiki/How%20to%20use%20-map%20option>`_ option). In these cases the use of regular Python dictionary will not work because it does not preserve order. Instead, use `OrderedDict <https://docs.python.org/3/library/collections.html#collections.OrderedDict>`_. For example we want to multiplex one video and two audio streams into an MPEG transport streams re-encoding both audio streams using different codecs. Here we use an OrderedDict to preserve the order of inputs so they match the order of streams in output options:

.. code:: python

    In [1]: from collections import OrderedDict
    In [2]: inputs = OrderedDict([('/tmp/video', None), ('/tmp/audio_1', None), ('/tmp/audio_2', None)])
    In [3]: outputs = {'/tmp/output.ts', '-map 0 -c:v h264 -map 1 -c:a:0 ac3 -map 2 -c:a:1 mp2'}
    In [4]: ff = FFmpeg(inputs=inputs, outputs=outputs)
    In [5]: ff.cmd_str
    Out[5]: 'ffmpeg -i /tmp/video -i /tmp/audio_1 -i /tmp/audio_2 -map 0 -c:v h264 -map 1 -c:a:0 ac3 -map 2 -c:a:1 mp2 /tmp/output.ts'
    In [6]: ff.run()

ffmpy can read input from ``STDIN`` and write output to ``STDOUT``. This can be achieved by using ffmpeg's `pipe <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_ protocol. The following example reads data from a file containing raw video frames in RGB format and passes it to ffmpy on ``STDIN``; ffmpy in its turn will encode raw frame data with H.264 and pack it in an MP4 container passing the output to ``STDOUT``:

.. code:: python

    In [1]: ff = FFmpeg(inputs={'pipe:0': '-f rawvideo -pix_fmt rgb24 -s:v 640x480'}, outputs={'pipe:1': '-v:c h264 -f mp4'})
    In [2]: ff.cmd_str
    Out[2]: 'ffmpeg -f rawvideo -pix_fmt rgb24 -s:v 640x480 -i pipe:0 -v:c h264 -f mp4 pipe:1'
    In [3]: ff.run(input_data=open('/tmp/rawvideo', 'rb').read())
