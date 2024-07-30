Examples
========

.. contents:: :local:

Format conversion
-----------------
The simplest example of usage is converting media from one format to another (in this case from MPEG transport stream to MP4) preserving all other attributes:

.. code:: python

    >>> from ffmpy import FFmpeg
    ... ff = FFmpeg(
    ...     inputs={'input.ts': None},
    ...     outputs={'output.mp4': None}
    ... )
    >>> ff.cmd
    'ffmpeg -i input.ts output.mp4'
    >>> ff.run()

Transcoding
-----------
If at the same time we wanted to re-encode video and audio using different codecs we'd have to specify additional output options:

.. code:: python

    >>> ff = FFmpeg(
    ...     inputs={'input.ts': None},
    ...     outputs={'output.mp4': '-c:a mp2 -c:v mpeg2video'}
    ... )
    >>> ff.cmd
    'ffmpeg -i input.ts -c:a mp2 -c:v mpeg2video output.mp4'
    >>> ff.run()

Demultiplexing
--------------
A more complex usage example would be demultiplexing an MPEG transport stream into separate elementary (audio and video) streams and save them in MP4 containers preserving the codecs (note how a list is used for options here):

.. code:: python

    >>> ff = FFmpeg(
    ...     inputs={'input.ts': None},
    ...     outputs={
    ...         'video.mp4': ['-map', '0:0', '-c:a', 'copy', '-f', 'mp4'],
    ...         'audio.mp4': ['-map', '0:1', '-c:a', 'copy', '-f', 'mp4']
    ...     }
    ... )
    >>> ff.cmd
    'ffmpeg -i input.ts -map 0:1 -c:a copy -f mp4 audio.mp4 -map 0:0 -c:a copy -f mp4 video.mp4'
    >>> ff.run()

.. warning::

    Note that it is not possible to mix the expression formats for options, i.e. it is not possible to have a list that contains strings with spaces (an exception to this is :ref:`complex_cmds`). For example, this command line will not work with ``FFmpeg``:


    .. code:: python

        >>> from subprocess import PIPE
        >>> ff = FFmpeg(
        ...     inputs={'input.ts': None},
        ...     outputs={
        ...         'video.mp4': ['-map 0:0', '-c:a copy', '-f mp4'],
        ...         'audio.mp4': ['-map 0:1', '-c:a copy', '-f mp4']
        ...     }
        ... )
        >>> ff.cmd
        'ffmpeg -hide_banner -i input.ts "-map 0:1" "-c:a copy" "-f mp4" audio.mp4 "-map 0:0" "-c:a copy" "-f mp4" video.mp4'
        >>>
        >>> ff.run(stderr=PIPE)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "/Users/ay/projects/personal/ffmpy/ffmpy.py", line 104, in run
            raise FFRuntimeError(self.cmd, ff_command.returncode, out[0], out[1])
        ffmpy.FFRuntimeError: `ffmpeg -hide_banner -i input.ts "-map 0:1" "-c:a copy" "-f mp4" audio.mp4 "-map 0:0" "-c:a copy" "-f mp4" video.mp4` exited with status 1

        STDOUT:


        STDERR:
        Unrecognized option 'map 0:1'.
        Error splitting the argument list: Option not found

        >>>

Notice how the actual ``FFmpeg`` command line contains unnecessary quotes.

Multiplexing
------------
To multiplex video and audio back into an MPEG transport stream with re-encoding:

.. code:: python

    >>> ff = FFmpeg(
    ...     inputs={'video.mp4': None, 'audio.mp3': None},
    ...     outputs={'output.ts': '-c:v h264 -c:a ac3'}
    ... )
    >>> ff.cmd
    'ffmpeg -i audio.mp4 -i video.mp4 -c:v h264 -c:a ac3 output.ts'
    >>> ff.run()

.. note::

    Since Python 3.7 dictionaries preserve order. Using `OrderedDict
   <https://docs.python.org/3/library/collections.html#collections.OrderedDict>`_ is no longer necessary.

There are cases where the order of inputs and outputs must be preserved (e.g. when using FFmpeg `-map <https://trac.ffmpeg.org/wiki/How%20to%20use%20-map%20option>`_ option). In these cases the use of regular Python dictionary will not work because it does not preserve order. Instead, use `OrderedDict <https://docs.python.org/3/library/collections.html#collections.OrderedDict>`_. For example we want to multiplex one video and two audio streams into an MPEG transport streams re-encoding both audio streams using different codecs. Here we use an OrderedDict to preserve the order of inputs so they match the order of streams in output options:

.. code:: python

    >>> from collections import OrderedDict
    >>> inputs = OrderedDict([('video.mp4', None), ('audio_1.mp3', None), ('audio_2.mp3', None)])
    >>> outputs = {'output.ts', '-map 0 -c:v h264 -map 1 -c:a:0 ac3 -map 2 -c:a:1 mp2'}
    >>> ff = FFmpeg(inputs=inputs, outputs=outputs)
    >>> ff.cmd
    'ffmpeg -i video.mp4 -i audio_1.mp3 -i audio_2.mp3 -map 0 -c:v h264 -map 1 -c:a:0 ac3 -map 2 -c:a:1 mp2 output.ts'
    >>> ff.run()

Using ``pipe`` protocol
-----------------------
*ffmpy* can read input from ``STDIN`` and write output to ``STDOUT``. This can be achieved by using FFmpeg `pipe <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_ protocol. The following example reads data from a file containing raw video frames in RGB format and passes it to *ffmpy* on ``STDIN``; *ffmpy* in its turn will encode raw frame data with H.264 and pack it in an MP4 container passing the output to ``STDOUT`` (note that you must redirect ``STDOUT`` of the process to a pipe by using ``subprocess.PIPE`` as ``stdout`` value, otherwise the output will get lost):

.. code:: python

    >>> import subprocess
    >>> ff = FFmpeg(
    ...     inputs={'pipe:0': '-f rawvideo -pix_fmt rgb24 -s:v 640x480'},
    ...     outputs={'pipe:1': '-c:v h264 -f mp4'}
    ... )
    >>> ff.cmd
    'ffmpeg -f rawvideo -pix_fmt rgb24 -s:v 640x480 -i pipe:0 -c:v h264 -f mp4 pipe:1'
    >>> stdout, stderr = ff.run(input_data=open('rawvideo', 'rb').read(), stdout=subprocess.PIPE)

.. _complex_cmds:

Complex command lines
---------------------
``FFmpeg`` command line can get pretty complex, for example, when using `filtering <https://trac.ffmpeg.org/wiki/FilteringGuide>`_. Therefore it is important to understand some of the rules for building command lines building with *ffmpy*. If an option contains quotes, it must be specified as a separate item in the options list **without** the quotes. However, if a single string is used for options, the quotes of the quoted option must be preserved in the string:

.. code:: python

    >>> ff = FFmpeg(
    ...     inputs={'input.ts': None},
    ...     outputs={'output.ts': ['-vf', 'adif=0:-1:0, scale=iw/2:-1']}
    ... )
    >>> ff.cmd
    'ffmpeg -i input.ts -vf "adif=0:-1:0, scale=iw/2:-1" output.ts'
    >>>
    >>> ff = FFmpeg(
    ...     inputs={'input.ts': None},
    ...     outputs={'output.ts': '-vf "adif=0:-1:0, scale=iw/2:-1"'}
    ... )
    >>> ff.cmd
    'ffmpeg -i input.ts -vf "adif=0:-1:0, scale=iw/2:-1" output.ts'

An even more complex example is a command line that burns the timecode into video:

.. code:: shell

    ffmpeg -i input.ts -vf "drawtext=fontfile=/Library/Fonts/Verdana.ttf: timecode='09\:57\:00\:00': r=25: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000000@1" -an output.ts

In *ffmpy* it can be expressed in the following way:

.. code:: python

    >>> ff = FFmpeg(
    ...     inputs={'input.ts': None},
    ...     outputs={'output.ts': ['-vf', "drawtext=fontfile=/Library/Fonts/Verdana.ttf: timecode='09\:57\:00\:00': r=25: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000000@1", '-an']}
    ... )
    >>> ff.cmd
    'ffmpeg -i input.ts -vf "drawtext=fontfile=/Library/Fonts/Verdana.ttf: timecode=\'09\:57\:00\:00\': r=25: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000000@1" -an output.ts'

The same command line can be compiled by passing output option as a single string, while keeping the quotes:

.. code:: python

    >>> ff = FFmpeg(
    ...     inputs={'input.ts': None},
    ...     outputs={'output.ts': ["-vf \"drawtext=fontfile=/Library/Fonts/Verdana.ttf: timecode='09\:57\:00\:00': r=25: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000000@1\" -an"}
    ... )
    >>> ff.cmd
    'ffmpeg -i input.ts -vf "drawtext=fontfile=/Library/Fonts/Verdana.ttf: timecode=\'09\:57\:00\:00\': r=25: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000000@1" -an output.ts'
