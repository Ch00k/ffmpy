import os
import re
import shlex
from subprocess import Popen, PIPE, list2cmdline

from ffmpy.exceptions import (
    FFRuntimeError,
    FFExecutableNotFoundError,
    FFUnsupportedVersionError
)


__version__ = '0.0.4'


class FF(object):
    """Wrapper for various `ffmpeg <https://www.ffmpeg.org/>`_. related applications (ffmpeg,
    ffprobe)
    """

    def __init__(self, executable='ffmpeg', global_options='', inputs=None, outputs=None):
        """Initialize wrapper class.

        Creates an instance of base FFmpeg command line. For details see
        `here <https://ffmpeg.org/ffmpeg.html#Synopsis>`_
        :param str executable: absolute path to ffmpeg executable
        :param list, str global_options: global options passed to ffmpeg executable
        :param dict inputs: a dictionary specifying one or more inputs as keys with their
            corresponding options as values
        :param dict outputs: a dictionary specifying one or more outputs as keys with their
            corresponding options as values
        """

        self.cmd = [executable]
        if not self.isiterable(global_options):
            global_options = shlex.split(global_options)
        self.cmd += global_options
        self.cmd += self.merge_args_opts(inputs, input_option=True)
        self.cmd += self.merge_args_opts(outputs)
        self.cmd_str = list2cmdline(self.cmd)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.cmd_str)

    def isiterable(self, obj):
        """Check if the object is an iterable type.

        :param object obj: an object to be checked
        :return: True if the object is iterable but is not a string, False otherwise
        :rtype: bool
        """
        return hasattr(obj, '__iter__') and not isinstance(obj, str)

    def merge_args_opts(self, args_opts_dict, **kwargs):
        """Merge input/output options with corresponding input/output arguments

        Iterates over the dictionary holding arguments (keys) and options (values). Merges each
        options string with its corresponding argument.
        :param dict args_opts_dict: a dictionary of arguments and options
        :param dict kwargs: *input_option* - if specified prepends `-i` to input argument
        :return: merged list of arguments with their respective options
        :rtype: list
        """
        merged = []
        if not args_opts_dict:
            return merged
        for arg, opt in args_opts_dict.items():
            if not self.isiterable(opt):
                opt = shlex.split(opt or '')
            merged += opt
            if not arg:
                continue
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
        ff_command = Popen(self.cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        out = ff_command.communicate(input=input_data)

        if ff_command.returncode != 0:
            raise FFRuntimeError(
                "ffmpeg call '{0}' exited with status {1}\n{2}".format(
                    self.cmd_str, ff_command.returncode, out[1])
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
