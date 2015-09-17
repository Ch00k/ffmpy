from ffmpy import FF


class FFmpeg(FF):
    """Wrapper for `ffmpeg <https://www.ffmpeg.org/>`_.

    Utilizes ffmpeg `pipe protocol <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_. Input data
    (as a byte string) is passed to ffmpeg on standard input and the result is read from standard
    output (as a byte string).
    """

    def __init__(self, executable='ffmpeg', global_options='', inputs=None, outputs=None):
        """Create an instance of FFmpeg.

        :param str executable: absolute path to ffmpeg executable
        :param list, str global_options: global options passed to ffmpeg executable
        :param dict inputs: a dictionary specifying one or more inputs as keys with their
            corresponding options as values
        :param dict outputs: a dictionary specifying one or more outputs as keys with their
            corresponding options as values
        """
        super(FFmpeg, self).__init__(
            executable=executable, global_options=global_options, inputs=inputs, outputs=outputs
        )
