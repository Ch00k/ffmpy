.. image:: https://img.shields.io/pypi/v/ffmpy.svg
    :target: https://pypi.python.org/pypi/ffmpy
    :alt: Latest version

.. image:: https://travis-ci.org/Ch00k/ffmpy.svg?branch=master
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

    from ffmpy import FFmpeg
    ff = FFmpeg(
        inputs={'input.ts': None},
        outputs={'output.mp4': None}
    )
    ff.cmd_str
    >>> ffmpeg -i input.ts output.mp4
    ff.run()

If at the same time we wanted to re-encode video and audio using different codecs we'd have to specify additional output options:

.. code:: python

    ff = FFmpeg(
        inputs={'input.ts': None},
        outputs={'output.mp4': '-c:a mp2 -c:v mpeg2video'}
    )
    ff.cmd_str
    >>> ffmpeg -i input.ts -c:a mp2 -c:v mpeg2video output.mp4
    ff.run()

A more complex usage example would be demultiplexing an MPEG transport stream into separate elementary (audio and video) streams and save them in MP4 containers preserving the codecs:

.. code:: python

    ff = FFmpeg(
        inputs={'input.ts': None},
        outputs={
            'video.mp4': '-map 0:0 -c:a copy -f mp4',
            'audio.mp4': '-map 0:1 -c:a copy -f mp4'
        }
    )
    ff.cmd_str
    >>> ffmpeg -i input.ts -map 0:1 -c:a copy -f mp4 audio.mp4 -map 0:0 -c:a copy -f mp4 video.mp4
    ff.run()

To multiplex video and audio back into an MPEG transport stream with re-encoding:

.. code:: python

    ff = FFmpeg(
        inputs={'video.mp4': None, 'audio.mp4': None},
        outputs={'output.ts': '-c:v h264 -c:a ac3'}
    )
    ff.cmd_str
    >>> ffmpeg -i audio.mp4 -i video.mp4 -c:v h264 -c:a ac3 output.ts
    ff.run()

There are cases where the order of inputs and outputs must be preserved (e.g. when using ffmpeg's `-map <https://trac.ffmpeg.org/wiki/How%20to%20use%20-map%20option>`_ option). In these cases the use of regular Python dictionary will not work because it does not preserve order. Instead, use `OrderedDict <https://docs.python.org/3/library/collections.html#collections.OrderedDict>`_. For example we want to multiplex one video and two audio streams into an MPEG transport streams re-encoding both audio streams using different codecs. Here we use an OrderedDict to preserve the order of inputs so they match the order of streams in output options:

.. code:: python

    from collections import OrderedDict
    inputs = OrderedDict([('video.mp4', None), ('audio_1.mp3', None), ('audio_2.mp3', None)])
    outputs = {'output.ts', '-map 0 -c:v h264 -map 1 -c:a:0 ac3 -map 2 -c:a:1 mp2'}
    ff = FFmpeg(inputs=inputs, outputs=outputs)
    ff.cmd_str
    >>> ffmpeg -i video.mp4 -i audio_1.mp3 -i audio_2.mp3 -map 0 -c:v h264 -map 1 -c:a:0 ac3 -map 2 -c:a:1 mp2 output.ts
    ff.run()

ffmpy can read input from ``STDIN`` and write output to ``STDOUT``. This can be achieved by using ffmpeg's `pipe <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_ protocol. The following example reads data from a file containing raw video frames in RGB format and passes it to ffmpy on ``STDIN``; ffmpy in its turn will encode raw frame data with H.264 and pack it in an MP4 container passing the output to ``STDOUT``:

.. code:: python

    ff = FFmpeg(
        inputs={'pipe:0': '-f rawvideo -pix_fmt rgb24 -s:v 640x480'},
        outputs={'pipe:1': '-c:v h264 -f mp4'}
    )
    ff.cmd_str
    >>> ffmpeg -f rawvideo -pix_fmt rgb24 -s:v 640x480 -i pipe:0 -c:v h264 -f mp4 pipe:1'
    ff.run(input_data=open('rawvideo', 'rb').read())
