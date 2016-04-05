import errno
import json
import shlex
from subprocess import Popen, PIPE, list2cmdline


__version__ = '0.1.0'


class FFmpeg(object):
    """Wrapper for various `ffmpeg <https://www.ffmpeg.org/>`_ related applications (ffmpeg,
    ffprobe).
    """

    def __init__(self, executable='ffmpeg', global_options='', inputs=None, outputs=None):
        """Initialize wrapper class.

        Compiles FFmpegg command like from passed arguments (executable path, options, inputs and
        outputs). FFmpeg executable by default is taken from ``PATH`` but can be overridden with an
        absolute path. For more info about FFmpeg command line format see
        `here <https://ffmpeg.org/ffmpeg.html#Synopsis>`_.

        :param str executable: ffmpeg executable; can either be ``ffmpeg`` command that will be found
            in ``PATH`` (the default) or an absolute path to ``ffmpeg`` executable
        :param iterable global_options: global options passed to ``ffmpeg`` executable (e.g.
            ``-y``, ``-v`` etc.)
        :param dict inputs: a dictionary specifying one or more inputs as keys with their
            corresponding options as values
        :param dict outputs: a dictionary specifying one or more outputs as keys with their
            corresponding options as values
        """
        self.executable = executable
        self.cmd = [executable]
        if not self._is_sequence(global_options):
            global_options = shlex.split(global_options)
        self.cmd += global_options
        self.cmd += self._merge_args_opts(inputs, input_option=True)
        self.cmd += self._merge_args_opts(outputs)
        self.cmd_str = list2cmdline(self.cmd)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.cmd_str)

    def _is_sequence(self, obj):
        """Check if the object is an iterable type.

        :param object obj: an object to be checked
        :return: True if the object is iterable but is not a string, False otherwise
        :rtype: bool
        """
        return hasattr(obj, '__iter__') and not isinstance(obj, str)

    def _merge_args_opts(self, args_opts_dict, **kwargs):
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
            if not self._is_sequence(opt):
                opt = shlex.split(opt or '')
            merged += opt
            if not arg:
                continue
            if 'input_option' in kwargs:
                merged.append('-i')
            merged.append(arg)
        return merged

    def run(self, input_data=None, verbose=False):
        """Run ffmpeg command and get its output.

        :param str input_data: media (audio, video, transport stream) data as a byte string (e.g. the
            result of reading a file in binary mode)
        :param bool verbose: show ffmpeg output
        :return: output of ffmpeg command as a byte string
        :rtype: str
        :raise: :class:`~.utils.ff.exceptions.FFRuntimeError` in case ffmpeg command fails
        """
        if verbose:
            stdout = stderr = None
        else:
            stdout = stderr = PIPE

        try:
            ff_command = Popen(self.cmd, stdin=PIPE, stdout=stdout, stderr=stderr)
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise FFExecutableNotFoundError("Executable '{0}' not found".format(self.executable))

        out = ff_command.communicate(input=input_data)
        if ff_command.returncode != 0:
            raise FFRuntimeError(
                "ffmpeg call '{0}' exited with status {1}\n{2}".format(
                    self.cmd_str, ff_command.returncode, out[1])
            )
        return out[0]


class FFprobe(FFmpeg):
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
            output = json.loads(output.decode())

        # TODO: Convert all "numeric" strings to int/float
        return output


class FFExecutableNotFoundError(Exception):
    """Raise when ffmpeg/ffprobe executable was not found"""


class FFRuntimeError(Exception):
    """Raise when FFmpeg/FFprobe run fails."""
