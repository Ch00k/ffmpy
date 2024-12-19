from __future__ import annotations

import os
import subprocess
import threading
import time
from unittest import mock

import pytest

from ffmpy import FFExecutableNotFoundError, FFmpeg, FFRuntimeError

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), "ffmpeg")
os.environ["PATH"] = FFMPEG_PATH + os.pathsep + os.environ["PATH"]


def test_invalid_executable_path() -> None:
    ff = FFmpeg(executable="/tmp/foo/bar/ffmpeg")
    with pytest.raises(FFExecutableNotFoundError) as exc_info:
        ff.run()
    assert str(exc_info.value) == "Executable '/tmp/foo/bar/ffmpeg' not found"


def test_other_oserror() -> None:
    executable = os.path.join(FFMPEG_PATH, "ffmpeg.go")
    ff = FFmpeg(executable=executable)
    with pytest.raises(PermissionError) as exc_info:
        ff.run()
    assert str(exc_info.value).startswith("[Errno 13] Permission denied")


def test_executable_full_path() -> None:
    executable = os.path.join(FFMPEG_PATH, "ffmpeg")
    ff = FFmpeg(executable=executable)
    ff.run()
    assert ff.cmd == executable


def test_no_redirection() -> None:
    global_options = "--stdin none --stdout oneline --stderr multiline --exit-code 0"
    ff = FFmpeg(global_options=global_options)
    stdout, stderr = ff.run()
    assert stdout is None
    assert stderr is None


def test_redirect_to_devnull() -> None:
    global_options = "--stdin none --stdout oneline --stderr multiline --exit-code 0"
    ff = FFmpeg(global_options=global_options)
    devnull = open(os.devnull, "wb")
    stdout, stderr = ff.run(stdout=devnull, stderr=devnull)
    assert stdout is None
    assert stderr is None


def test_redirect_to_pipe() -> None:
    global_options = "--stdin none --stdout oneline --stderr multiline --exit-code 0"
    ff = FFmpeg(global_options=global_options)
    stdout, stderr = ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert stdout == b"This is printed to stdout"
    assert stderr == b"These are\nmultiple lines\nprinted to stderr"


def test_input() -> None:
    global_options = "--stdin pipe --stdout oneline --stderr multiline --exit-code 0"
    ff = FFmpeg(global_options=global_options)
    stdout, stderr = ff.run(
        input_data=b"my input data", stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert stdout == b"my input data\nThis is printed to stdout"
    assert stderr == b"These are\nmultiple lines\nprinted to stderr"


def test_non_zero_exitcode() -> None:
    global_options = "--stdin none --stdout multiline --stderr multiline --exit-code 42"
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert exc_info.value.cmd == (
        "ffmpeg --stdin none --stdout multiline --stderr multiline --exit-code 42"
    )
    assert exc_info.value.exit_code == 42
    assert exc_info.value.stdout == b"These are\nmultiple lines\nprinted to stdout"
    assert exc_info.value.stderr == b"These are\nmultiple lines\nprinted to stderr"
    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout multiline --stderr multiline --exit-code 42` "
        "exited with status 42\n\n"
        "STDOUT:\n"
        "These are\n"
        "multiple lines\n"
        "printed to stdout\n\n"
        "STDERR:\n"
        "These are\n"
        "multiple lines\n"
        "printed to stderr"
    )


def test_non_zero_exitcode_no_stderr() -> None:
    global_options = "--stdin none --stdout multiline --stderr none --exit-code 42"
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert exc_info.value.cmd == (
        "ffmpeg --stdin none --stdout multiline --stderr none --exit-code 42"
    )
    assert exc_info.value.exit_code == 42
    assert exc_info.value.stdout == b"These are\nmultiple lines\nprinted to stdout"
    assert exc_info.value.stderr == b""
    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout multiline --stderr none --exit-code 42` "
        "exited with status 42\n\n"
        "STDOUT:\n"
        "These are\n"
        "multiple lines\n"
        "printed to stdout\n\n"
        "STDERR:\n"
    )


def test_non_zero_exitcode_no_stdout() -> None:
    global_options = "--stdin none --stdout none --stderr multiline --exit-code 42"
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert exc_info.value.cmd == (
        "ffmpeg --stdin none --stdout none --stderr multiline --exit-code 42"
    )
    assert exc_info.value.exit_code == 42
    assert exc_info.value.stdout == b""
    assert exc_info.value.stderr == b"These are\nmultiple lines\nprinted to stderr"
    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout none --stderr multiline --exit-code 42` "
        "exited with status 42\n\n"
        "STDOUT:\n"
        "\n\n"
        "STDERR:\n"
        "These are\n"
        "multiple lines\n"
        "printed to stderr"
    )


def test_non_zero_exitcode_no_stdout_and_stderr() -> None:
    global_options = "--stdin none --stdout none --stderr none --exit-code 42"
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert exc_info.value.cmd == ("ffmpeg --stdin none --stdout none --stderr none --exit-code 42")
    assert exc_info.value.exit_code == 42
    assert exc_info.value.stdout == b""
    assert exc_info.value.stderr == b""
    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout none --stderr none --exit-code 42` "
        "exited with status 42\n\n"
        "STDOUT:\n"
        "\n\n"
        "STDERR:\n"
    )


def test_raise_exception_with_stdout_stderr_none() -> None:
    global_options = "--stdin none --stdout none --stderr none --exit-code 42"
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run()

    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout none --stderr none --exit-code 42` "
        "exited with status 42\n\n"
        "STDOUT:\n"
        "\n\n"
        "STDERR:\n"
    )


def test_terminate_process() -> None:
    global_options = "--long-run"
    ff = FFmpeg(global_options=global_options)

    thread_1 = threading.Thread(target=ff.run)
    thread_1.start()

    timeout = time.time() + 3
    while time.time() < timeout:
        if ff.process is None:
            time.sleep(0.05)
        else:
            break
    else:
        raise AssertionError("FFmpeg process was not started within 3 seconds")

    print(ff.process.returncode)

    ff.process.terminate()
    thread_1.join()

    assert ff.process.returncode == -15


@mock.patch("ffmpy.subprocess.Popen")
def test_custom_env(popen_mock: mock.MagicMock) -> None:
    ff = FFmpeg()
    popen_mock.return_value.communicate.return_value = ("output", "error")
    popen_mock.return_value.returncode = 0
    ff.run(env={"FOO": "BAR"})
    popen_mock.assert_called_with(
        mock.ANY, stdin=mock.ANY, stdout=mock.ANY, stderr=mock.ANY, env={"FOO": "BAR"}
    )


@mock.patch("ffmpy.subprocess.Popen")
def test_arbitraty_popen_kwargs(popen_mock: mock.MagicMock) -> None:
    ff = FFmpeg()
    popen_mock.return_value.communicate.return_value = ("output", "error")
    popen_mock.return_value.returncode = 0
    ff.run(creationflags=42, encoding="foo", text="bar")
    popen_mock.assert_called_with(
        mock.ANY,
        stdin=mock.ANY,
        stdout=mock.ANY,
        stderr=mock.ANY,
        env=None,
        creationflags=42,
        encoding="foo",
        text="bar",
    )
