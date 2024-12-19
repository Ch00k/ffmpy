from __future__ import annotations

import pytest

from ffmpy import FFmpeg, FFprobe


@pytest.mark.parametrize(
    "global_options",
    [
        "-hide_banner -y -v debug",
        ["-hide_banner", "-y", "-v", "debug"],
        ("-hide_banner", "-y", "-v", "debug"),
        ["-hide_banner -y", "-v debug"],
    ],
)
def test_global_options(global_options: list) -> None:
    ff = FFmpeg(global_options=global_options)
    assert ff._cmd == ["ffmpeg", "-hide_banner", "-y", "-v", "debug"]
    assert ff.cmd == "ffmpeg -hide_banner -y -v debug"


def test_global_options_none() -> None:
    ff = FFmpeg(global_options=None)
    assert ff._cmd == ["ffmpeg"]
    assert ff.cmd == "ffmpeg"


@pytest.mark.parametrize(
    "input_options",
    [
        "-f rawvideo -pix_fmt rgb24 -s:v 640x480",
        ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s:v", "640x480"],
        ("-f", "rawvideo", "-pix_fmt", "rgb24", "-s:v", "640x480"),
    ],
)
def test_input_options(input_options: list) -> None:
    ff = FFmpeg(inputs={"/tmp/rawvideo": input_options})
    assert ff._cmd == [
        "ffmpeg",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s:v",
        "640x480",
        "-i",
        "/tmp/rawvideo",
    ]
    assert ff.cmd == "ffmpeg -f rawvideo -pix_fmt rgb24 -s:v 640x480 -i /tmp/rawvideo"


@pytest.mark.parametrize(
    "output_options",
    [
        "-f rawvideo -pix_fmt rgb24 -s:v 640x480",
        ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s:v", "640x480"],
        ("-f", "rawvideo", "-pix_fmt", "rgb24", "-s:v", "640x480"),
    ],
)
def test_output_options(output_options: list) -> None:
    ff = FFmpeg(outputs={"/tmp/rawvideo": output_options})
    assert ff._cmd == [
        "ffmpeg",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s:v",
        "640x480",
        "/tmp/rawvideo",
    ]
    assert ff.cmd == "ffmpeg -f rawvideo -pix_fmt rgb24 -s:v 640x480 /tmp/rawvideo"


# This kind of usage would be invalid, but it's tested to ensure the correct behavior
def test_input_output_options_split_mixed() -> None:
    ff = FFmpeg(
        inputs={"/tmp/rawvideo": ["-f rawvideo", "-pix_fmt rgb24", "-s:v 640x480"]},
        outputs={"/tmp/rawvideo": ["-f rawvideo", "-pix_fmt rgb24", "-s:v 640x480"]},
    )
    assert ff._cmd == [
        "ffmpeg",
        "-f rawvideo",
        "-pix_fmt rgb24",
        "-s:v 640x480",
        "-i",
        "/tmp/rawvideo",
        "-f rawvideo",
        "-pix_fmt rgb24",
        "-s:v 640x480",
        "/tmp/rawvideo",
    ]
    assert ff.cmd == (
        'ffmpeg "-f rawvideo" "-pix_fmt rgb24" "-s:v 640x480" -i /tmp/rawvideo '
        '"-f rawvideo" "-pix_fmt rgb24" "-s:v 640x480" /tmp/rawvideo'
    )


def test_input_output_none() -> None:
    inputs = {None: ["-f", "rawvideo"], "/tmp/video.mp4": ["-f", "mp4"]}
    outputs = {"/tmp/rawvideo": ["-f", "rawvideo"], None: ["-f", "mp4"]}
    ff = FFmpeg(inputs=inputs, outputs=outputs)  # type: ignore[arg-type]
    assert ff._cmd == [
        "ffmpeg",
        "-f",
        "rawvideo",
        "-f",
        "mp4",
        "-i",
        "/tmp/video.mp4",
        "-f",
        "rawvideo",
        "/tmp/rawvideo",
        "-f",
        "mp4",
    ]
    assert ff.cmd == ("ffmpeg -f rawvideo -f mp4 -i /tmp/video.mp4 -f rawvideo /tmp/rawvideo -f mp4")


def test_input_options_output_options_none() -> None:
    inputs = {"/tmp/rawvideo": None, "/tmp/video.mp4": ["-f", "mp4"]}
    outputs = {"/tmp/rawvideo": ["-f", "rawvideo"], "/tmp/video.mp4": None}
    ff = FFmpeg(inputs=inputs, outputs=outputs)
    assert ff._cmd == [
        "ffmpeg",
        "-i",
        "/tmp/rawvideo",
        "-f",
        "mp4",
        "-i",
        "/tmp/video.mp4",
        "-f",
        "rawvideo",
        "/tmp/rawvideo",
        "/tmp/video.mp4",
    ]
    assert ff.cmd == (
        "ffmpeg -i /tmp/rawvideo -f mp4 -i /tmp/video.mp4 -f rawvideo /tmp/rawvideo /tmp/video.mp4"
    )


def test_quoted_option() -> None:
    inputs = {"input.ts": None}
    quoted_option = (
        "drawtext="
        "fontfile=/Library/Fonts/Verdana.ttf: "
        "timecode='09:57:00:00': "
        "r=25: x=(w-tw)/2: y=h-(2*lh): "
        "fontcolor=white: box=1: "
        "boxcolor=0x00000000@1"
    )

    outputs = {"output.ts": ["-vf", quoted_option, "-an"]}
    ff = FFmpeg(inputs=inputs, outputs=outputs)
    assert ff._cmd == [
        "ffmpeg",
        "-i",
        "input.ts",
        "-vf",
        quoted_option,
        "-an",
        "output.ts",
    ]
    assert ff.cmd == f'ffmpeg -i input.ts -vf "{quoted_option}" -an output.ts'


def test_path_with_spaces() -> None:
    inputs = {"/home/ay/file with spaces": None}
    outputs = {"output.ts": None}

    ff = FFmpeg(inputs=inputs, outputs=outputs)
    assert ff._cmd == ["ffmpeg", "-i", "/home/ay/file with spaces", "output.ts"]
    assert ff.cmd == 'ffmpeg -i "/home/ay/file with spaces" output.ts'


def test_repr() -> None:
    inputs = {"input.ts": "-f rawvideo"}
    outputs = {"output.ts": "-f rawvideo"}
    ff = FFmpeg(inputs=inputs, outputs=outputs)
    assert repr(ff) == "<'FFmpeg' 'ffmpeg -f rawvideo -i input.ts -f rawvideo output.ts'>"


def test_ffprobe() -> None:
    inputs = {"input.ts": "-f rawvideo"}
    ff = FFprobe(global_options="--verbose", inputs=inputs)
    assert repr(ff) == "<'FFprobe' 'ffprobe --verbose -f rawvideo -i input.ts'>"
