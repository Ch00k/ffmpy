import sys

from ffmpy import FFmpeg

PY2 = int(sys.version[0]) == 2
PY26 = PY2 and int(sys.version_info[1]) < 7

if PY26:
    from .ordereddict import OrderedDict
else:
    from collections import OrderedDict


def test_default():
    ff = FFmpeg()
    assert ff.cmd == ['ffmpeg']


def test_ff():
    executable = '/opt/ff/ff'
    global_options = ['-hide_banner', '-y']
    inputs = {'/tmp/raw_video': ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s:v', '640x480']}
    outputs = {'/tmp/video.mp4': ['-vcodec', 'h264', '-f', 'mp4']}
    ff = FFmpeg(executable=executable, global_options=global_options, inputs=inputs, outputs=outputs)
    assert ff.cmd == [
        '/opt/ff/ff', '-hide_banner', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s:v', '640x480', '-i', '/tmp/raw_video',
        '-vcodec', 'h264', '-f', 'mp4', '/tmp/video.mp4'
    ]
    assert ff.cmd_str == (
        '/opt/ff/ff -hide_banner -y '
        '-f rawvideo -pix_fmt rgb24 -s:v 640x480 -i /tmp/raw_video '
        '-vcodec h264 -f mp4 /tmp/video.mp4'
    )


def test_global_options_str():
    ff = FFmpeg(global_options='-hide_banner -y')
    assert ff.cmd == ['ffmpeg', '-hide_banner', '-y']


def test_global_options_list():
    ff = FFmpeg(global_options=['-hide_banner', '-y'])
    assert ff.cmd == ['ffmpeg', '-hide_banner', '-y']


def test_input_options_str():
    ff = FFmpeg(inputs={'/tmp/rawvideo': '-f rawvideo'})
    assert ff.cmd == ['ffmpeg', '-f', 'rawvideo', '-i', '/tmp/rawvideo']


def test_input_options_list():
    ff = FFmpeg(inputs={'/tmp/rawvideo': ['-f', 'rawvideo']})
    assert ff.cmd == ['ffmpeg', '-f', 'rawvideo', '-i', '/tmp/rawvideo']


def test_output_options_str():
    ff = FFmpeg(outputs={'/tmp/video.mp4': '-f mp4'})
    assert ff.cmd == ['ffmpeg', '-f', 'mp4', '/tmp/video.mp4']


def test_output_options_list():
    ff = FFmpeg(outputs={'/tmp/video.mp4': ['-f', 'mp4']})
    assert ff.cmd == ['ffmpeg', '-f', 'mp4', '/tmp/video.mp4']


def test_input_none():
    ff = FFmpeg(inputs={None: ['-f', 'rawvideo']})
    assert ff.cmd == ['ffmpeg', '-f', 'rawvideo']


def test_first_input_none():
    inputs = OrderedDict(((None, ['-f', 'rawvideo']), ('/tmp/video.mp4', ['-f', 'mp4'])))
    ff = FFmpeg(inputs=inputs)
    assert ff.cmd == ['ffmpeg', '-f', 'rawvideo', '-f', 'mp4', '-i', '/tmp/video.mp4']


def test_second_input_none():
    inputs = OrderedDict((('/tmp/rawvideo', ['-f', 'rawvideo']), (None, ['-f', 'mp4'])))
    ff = FFmpeg(inputs=inputs)
    assert ff.cmd == ['ffmpeg', '-f', 'rawvideo', '-i', '/tmp/rawvideo', '-f', 'mp4']


def test_first_output_none():
    outputs = OrderedDict(((None, ['-f', 'rawvideo']), ('/tmp/video.mp4', ['-f', 'mp4'])))
    ff = FFmpeg(outputs=outputs)
    assert ff.cmd == ['ffmpeg', '-f', 'rawvideo', '-f', 'mp4', '/tmp/video.mp4']


def test_second_output_none():
    outputs = OrderedDict((('/tmp/rawvideo', ['-f', 'rawvideo']), (None, ['-f', 'mp4'])))
    ff = FFmpeg(outputs=outputs)
    assert ff.cmd == ['ffmpeg', '-f', 'rawvideo', '/tmp/rawvideo', '-f', 'mp4']
