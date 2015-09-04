class FFExecutableNotFoundError(Exception):
    """Raise when ffmpeg/ffprobe executable was not found"""


class FFUnsupportedVersionError(Exception):
    """Raise when found an ffmpeg version lower than supported one"""


class FFRuntimeError(Exception):
    """Raise when FFmpeg/FFprobe run fails."""
    pass
