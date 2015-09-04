import json

from ffmpy import FF


class FFprobe(FF):
    """
    Wrapper for `ffprobe <https://www.ffmpeg.org/ffprobe.html>`_.

    Utilizes ffmpeg `pipe protocol <https://www.ffmpeg.org/ffmpeg-protocols.html#pipe>`_. Input data
    (as a byte string) is passed to ffprobe on standard input. Result is presented in JSON format.
    """

    def __init__(self, executable='ffprobe', global_options=None, input_options=None, inputs=None,
                 output_options=None, outputs=None):
        """Create an instance of FFprobe.

        :param str executable: absolute path to ffmpeg executable
        :param list global_options: global options passed to ffmpeg executable
        :param list input_options: options for input
        :param list inputs: one or more inputs for processing (as passed to ``-i`` command line
            option of ffmpeg)
        :param list output_options: options for output
        :param list outputs: one or more outputs where the ffmpeg results will be piped
        """
        output_options = output_options or []
        output_options += ['-print_format', 'json']
        super(FFprobe, self).__init__(
            executable=executable, global_options=global_options, input_options=input_options,
            inputs=inputs, output_options=output_options, outputs=outputs
        )

    def compile_ff_cmd(self):
        """Compile FFmpeg command line.

        Creates a list of FFmpeg command line parts ready to be passed to `subprocess.Popen`
        :return: FFmpeg command line
        :rtype list
        """
        ff_cmd = [self.executable]
        ff_cmd += self.global_options
        ff_cmd += self.merge_opts_args(self.input_options, self.inputs, input_option=True)
        ff_cmd += self.output_options
        return ff_cmd

    def run(self, input_data=None):
        """Run ffprobe command and convert JSON output to a Python object.

        :param str input_data: media (audio, video, transport stream) data as a byte string (e.g. the
            result of reading a file in binary mode)
        :return: dictionary describing the input media
        :rtype: dict
        """
        output = super(FFprobe, self).run(input_data)
        data = json.loads(output)

        # TODO: Convert all "numeric" strings to int/float
        return data
