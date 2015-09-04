from ffmpy import FF


class FFmpeg(FF):
    """Wrapper for `ffmpeg <https://www.ffmpeg.org/>`_.

    Utilizes ffmpeg `pipe protocol <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_. Input data
    (as a byte string) is passed to ffmpeg on standard input and the result is read from standard
    output (as a byte string).
    """

    def __init__(self, executable='ffmpeg', global_options=None, input_options=None, inputs=None,
                 output_options=None, outputs=None):
        """Create an instance of FFmpeg.

        :param str executable: absolute path to ffmpeg executable
        :param list global_options: global options passed to ffmpeg executable
        :param list input_options: options for input. A tuple of lists that will be merged with
            corresponding inputs
        :param list inputs: one or more inputs for processing (as passed to ``-i`` command line
            option of ffmpeg)
        :param list output_options: options for output. A tuple of lists that will be merged with
            corresponding outputs
        :param list outputs: one or more outputs where the ffmpeg results will be piped
        """
        global_options = global_options or []
        global_options += ['-y']
        super(FFmpeg, self).__init__(
            executable=executable, global_options=global_options, input_options=input_options,
            inputs=inputs, output_options=output_options, outputs=outputs
        )
