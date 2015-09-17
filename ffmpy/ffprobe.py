import json

from ffmpy import FF


class FFprobe(FF):
    """
    Wrapper for `ffprobe <https://www.ffmpeg.org/ffprobe.html>`_.

    Utilizes ffmpeg `pipe protocol <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_. Input data
    (as a byte string) is passed to ffprobe on standard input. Result is presented in JSON format.
    """

    def __init__(self, executable='ffprobe', global_options='', inputs=None):
        """Create an instance of FFprobe.

        :param str executable: absolute path to ffprobe executable
        :param list, str global_options: global options passed to ffmpeg executable
        :param dict inputs: a dictionary specifying one or more inputs as keys with their
            corresponding options as values
        """
        super(FFprobe, self).__init__(
            executable=executable, global_options=global_options, inputs=inputs
        )

    def run(self, input_data=None):
        """Run ffprobe command and return its output.

        If the command line contains `-print_format json` also parses the JSON output and
        deserializes it into a dictionary.
        :param str input_data: media (audio, video, transport stream) data as a byte string (e.g. the
            result of reading a file in binary mode)
        :return: dictionary describing the input media
        :rtype: dict
        """
        output = super(FFprobe, self).run(input_data)
        if '-print_format json' in self.cmd_str:
            output = json.loads(output)

        # TODO: Convert all "numeric" strings to int/float
        return output
