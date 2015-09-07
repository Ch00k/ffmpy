import os
import re
from subprocess import Popen, PIPE, list2cmdline

from ffmpy.exceptions import (
    FFRuntimeError,
    FFExecutableNotFoundError,
    FFUnsupportedVersionError
)


__version__ = '0.0.2'


# TODO: Improve documentation (improve descriptions, add usage examples etc.)
class FF(object):
    """Wrapper for various `ffmpeg <https://www.ffmpeg.org/>`_. related applications (ffmpeg,
    ffprobe)
    """

    def __init__(self, executable='ffmpeg', global_options=None, input_options=None, inputs=None,
                 output_options=None, outputs=None):
        """Initialize wrapper class.

        Creates an instance of base FFmpeg command line. For deatils see
        `here <https://ffmpeg.org/ffmpeg.html#Synopsis>`_
        :param str executable: absolute path to ffmpeg executable
        :param list global_options: global options passed to ffmpeg executable
        :param list input_options: options for input
        :param list inputs: one or more inputs for processing (as passed to ``-i`` command line
            option of ffmpeg)
        :param list output_options: options for output
        :param list outputs: one or more outputs where the ffmpeg results will be piped
        """
        self.executable = executable
        self.global_options = global_options or []
        self.global_options += ['-hide_banner']
        self.input_options = input_options or []
        self.inputs = inputs or []
        self.output_options = output_options or []
        self.outputs = outputs or []

    def compile_ff_cmd(self):
        """Compile FFmpeg command line.

        Creates a list of FFmpeg command line parts ready to be passed to `subprocess.Popen`
        :return: FFmpeg command line
        :rtype list
        """
        ff_cmd = [self.executable]
        ff_cmd += self.global_options
        ff_cmd += self.merge_opts_args(self.input_options, self.inputs, input_option=True)
        ff_cmd += self.merge_opts_args(self.output_options, self.outputs)
        return ff_cmd

    def merge_opts_args(self, options, args, **kwargs):
        """Merge input/output options with corresponding input/output arguments

        Connects a list of options with their corresponding arguments. If the list of options has
        greater length than the list of arguments the leftover options are ignored. If the list of
        arguments has greater length than the list of options the leftover arguments are added
        without any options.
        :param list options: tuple of options
        :param list args: tuple of arguments
        :param dict kwargs: *input_option* - if specified prepends `-i` to input argument
        :return: merged list of arguments with their respective options
        :rtype: list
        """
        merged = []
        for i, arg in enumerate(args):
            try:
                merged += options[i]
            except IndexError:
                pass
            if 'input_option' in kwargs:
                merged.append('-i')
            merged.append(arg)
        return merged

    def run(self, input_data=None):
        """Runs ffmpeg command and get its output.

        :param str input_data: media (audio, video, transport stream) data as a byte string (e.g. the
            result of reading a file in binary mode)
        :return: output of ffmpeg command as a byte string
        :rtype: str
        :raise: :class:`~.utils.ff.exceptions.FFRuntimeError` in case ffmpeg command fails

        """
        ff_cmd = self.compile_ff_cmd()
        ff_command = Popen(ff_cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        out = ff_command.communicate(input=input_data)

        if ff_command.returncode != 0:
            raise FFRuntimeError(
                "ffmpeg call '{0}' exited with status {1}\n{2}".format(
                    list2cmdline(ff_cmd), ff_command.returncode, out[1])
            )
        return out[0]

    def check_ffmpeg_version(self, executable, min_version):
        """Check ffmpeg version installed in the system.

        :param executable: absolute path to ffmpeg executable
        :param min_version: minimum supported version of ffmpeg
        :raise: :class:`~.utils.ff.exceptions.FFExecutableNotFoundError` if ffmpeg executable is not
            found or is not executable, :class:`~.utils.ff.exceptions.FFUnsupportedVersionError` if
            version is not supported
        """
        if not os.path.isfile(executable) or not os.access(executable, os.X_OK):
            raise FFExecutableNotFoundError(
                "{0} not found or is not executable".format(executable)
            )

        version_info = Popen([executable, '-version'], stdout=PIPE).communicate()[0]

        pattern = re.compile('(ffmpeg|ffprobe) version (.*) Copyright.*')
        match = pattern.match(version_info)
        if not match:
            raise RuntimeError("Could not determine ffmpeg version")

        version = match.groups()[1]
        major_version = float('.'.join(version.split('.')[:2]))
        if major_version < min_version:
            raise FFUnsupportedVersionError(
                "ffmpeg version {0} is not supported. "
                "Please upgrade to {1}+".format(min_version)
            )
