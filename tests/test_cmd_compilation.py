import pytest

from collections import OrderedDict

from ffmpy import FFmpeg


@pytest.mark.parametrize(
    'global_options',
    [
        '-hide_banner -y -v debug',
        ['-hide_banner', '-y', '-v', 'debug'],
        ('-hide_banner', '-y', '-v', 'debug'),
        ['-hide_banner -y', '-v debug']
    ]
)
def test_global_options(global_options):
    ff = FFmpeg(global_options=global_options)
    assert ff._cmd == ['ffmpeg', '-hide_banner', '-y', '-v', 'debug']
    assert ff.cmd == 'ffmpeg -hide_banner -y -v debug'


@pytest.mark.parametrize(
    'input_options',
    [
        '-f rawvideo -pix_fmt rgb24 -s:v 640x480',
        ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s:v', '640x480'],
        ('-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s:v', '640x480')
    ]
)
def test_input_options(input_options):
    ff = FFmpeg(inputs={'/tmp/rawvideo': input_options})
    assert ff._cmd == [
        'ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s:v', '640x480', '-i', '/tmp/rawvideo'
    ]
    assert ff.cmd == 'ffmpeg -f rawvideo -pix_fmt rgb24 -s:v 640x480 -i /tmp/rawvideo'


@pytest.mark.parametrize(
    'output_options',
    [
        '-f rawvideo -pix_fmt rgb24 -s:v 640x480',
        ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s:v', '640x480'],
        ('-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s:v', '640x480')
    ]
)
def test_output_options(output_options):
    ff = FFmpeg(outputs={'/tmp/rawvideo': output_options})
    assert ff._cmd == [
        'ffmpeg', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s:v', '640x480', '/tmp/rawvideo'
    ]
    assert ff.cmd == 'ffmpeg -f rawvideo -pix_fmt rgb24 -s:v 640x480 /tmp/rawvideo'


def test_input_output_none():
    inputs = OrderedDict(((None, ['-f', 'rawvideo']), ('/tmp/video.mp4', ['-f', 'mp4'])))
    outputs = OrderedDict((('/tmp/rawvideo', ['-f', 'rawvideo']), (None, ['-f', 'mp4'])))
    ff = FFmpeg(inputs=inputs, outputs=outputs)
    assert ff._cmd == [
        'ffmpeg', '-f', 'rawvideo', '-f', 'mp4', '-i', '/tmp/video.mp4',
        '-f', 'rawvideo', '/tmp/rawvideo', '-f', 'mp4'
    ]
    assert ff.cmd == 'ffmpeg -f rawvideo -f mp4 -i /tmp/video.mp4 -f rawvideo /tmp/rawvideo -f mp4'


def test_input_options_output_options_none():
    inputs = OrderedDict((('/tmp/rawvideo', None), ('/tmp/video.mp4', ['-f', 'mp4'])))
    outputs = OrderedDict((('/tmp/rawvideo', ['-f', 'rawvideo']), ('/tmp/video.mp4', None)))
    ff = FFmpeg(inputs=inputs, outputs=outputs)
    assert ff._cmd == [
        'ffmpeg', '-i', '/tmp/rawvideo', '-f', 'mp4', '-i', '/tmp/video.mp4',
        '-f', 'rawvideo', '/tmp/rawvideo', '/tmp/video.mp4'
    ]
    assert ff.cmd == (
        'ffmpeg -i /tmp/rawvideo -f mp4 -i /tmp/video.mp4 -f rawvideo /tmp/rawvideo /tmp/video.mp4'
    )


def test_quoted_option():
    inputs = {'input.ts': None}
    quoted_option = (
        "drawtext="
        "fontfile=/Library/Fonts/Verdana.ttf: "
        "timecode='09:57:00:00': "
        "r=25: x=(w-tw)/2: y=h-(2*lh): "
        "fontcolor=white: box=1: "
        "boxcolor=0x00000000@1"
    )

    outputs = {'output.ts': ['-vf', quoted_option, '-an']}
    ff = FFmpeg(inputs=inputs, outputs=outputs)
    assert ff._cmd == ['ffmpeg', '-i', 'input.ts', '-vf', quoted_option, '-an', 'output.ts']
    assert ff.cmd == 'ffmpeg -i input.ts -vf "{0}" -an output.ts'.format(quoted_option)


def test_path_with_spaces():
    inputs = {'/home/ay/file with spaces': None}
    outputs = {'output.ts': None}

    ff = FFmpeg(inputs=inputs, outputs=outputs)
    assert ff._cmd == ['ffmpeg', '-i', '/home/ay/file with spaces', 'output.ts']
    assert ff.cmd == 'ffmpeg -i "/home/ay/file with spaces" output.ts'
