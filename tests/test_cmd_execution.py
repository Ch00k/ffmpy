import subprocess
import os
import threading
import time

import pytest

from ffmpy import FFmpeg, FFRuntimeError, FFExecutableNotFoundError


def test_invalid_executable_path():
    ff = FFmpeg(executable='/tmp/foo/bar/ffmpeg')
    with pytest.raises(FFExecutableNotFoundError) as exc_info:
        ff.run()
    assert str(exc_info.value) == "Executable '/tmp/foo/bar/ffmpeg' not found"


def test_no_redirection():
    global_options = '--stdin none --stdout oneline --stderr multiline --exit-code 0'
    ff = FFmpeg(global_options=global_options)
    stdout, stderr = ff.run()
    assert stdout is None
    assert stderr is None


def test_redirect_to_devnull():
    global_options = '--stdin none --stdout oneline --stderr multiline --exit-code 0'
    ff = FFmpeg(global_options=global_options)
    devnull = open(os.devnull, 'wb')
    stdout, stderr = ff.run(stdout=devnull, stderr=devnull)
    assert stdout is None
    assert stderr is None


def test_redirect_to_pipe():
    global_options = '--stdin none --stdout oneline --stderr multiline --exit-code 0'
    ff = FFmpeg(global_options=global_options)
    stdout, stderr = ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert stdout == b'This is printed to stdout'
    assert stderr == b'These are\nmultiple lines\nprinted to stderr'


def test_input():
    global_options = '--stdin pipe --stdout oneline --stderr multiline --exit-code 0'
    ff = FFmpeg(global_options=global_options)
    stdout, stderr = ff.run(
        input_data=b'my input data',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert stdout == b'my input data\nThis is printed to stdout'
    assert stderr == b'These are\nmultiple lines\nprinted to stderr'


def test_non_zero_exitcode():
    global_options = '--stdin none --stdout multiline --stderr multiline --exit-code 42'
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert exc_info.value.cmd == (
        "ffmpeg --stdin none --stdout multiline --stderr multiline --exit-code 42"
    )
    assert exc_info.value.exit_code == 42
    assert exc_info.value.stdout == b'These are\nmultiple lines\nprinted to stdout'
    assert exc_info.value.stderr == b'These are\nmultiple lines\nprinted to stderr'
    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout multiline --stderr multiline --exit-code 42` "
        'exited with status 42\n\n'
        'STDOUT:\n'
        'These are\n'
        'multiple lines\n'
        'printed to stdout\n\n'
        'STDERR:\n'
        'These are\n'
        'multiple lines\n'
        'printed to stderr'
    )


def test_non_zero_exitcode_no_stderr():
    global_options = '--stdin none --stdout multiline --stderr none --exit-code 42'
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert exc_info.value.cmd == (
        "ffmpeg --stdin none --stdout multiline --stderr none --exit-code 42"
    )
    assert exc_info.value.exit_code == 42
    assert exc_info.value.stdout == b'These are\nmultiple lines\nprinted to stdout'
    assert exc_info.value.stderr == b''
    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout multiline --stderr none --exit-code 42` "
        'exited with status 42\n\n'
        'STDOUT:\n'
        'These are\n'
        'multiple lines\n'
        'printed to stdout\n\n'
        'STDERR:\n'
    )


def test_non_zero_exitcode_no_stdout():
    global_options = '--stdin none --stdout none --stderr multiline --exit-code 42'
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert exc_info.value.cmd == (
        "ffmpeg --stdin none --stdout none --stderr multiline --exit-code 42"
    )
    assert exc_info.value.exit_code == 42
    assert exc_info.value.stdout == b''
    assert exc_info.value.stderr == b'These are\nmultiple lines\nprinted to stderr'
    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout none --stderr multiline --exit-code 42` "
        'exited with status 42\n\n'
        'STDOUT:\n'
        '\n\n'
        'STDERR:\n'
        'These are\n'
        'multiple lines\n'
        'printed to stderr'
    )


def test_non_zero_exitcode_no_stdout_and_stderr():
    global_options = '--stdin none --stdout none --stderr none --exit-code 42'
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    assert exc_info.value.cmd == (
        "ffmpeg --stdin none --stdout none --stderr none --exit-code 42"
    )
    assert exc_info.value.exit_code == 42
    assert exc_info.value.stdout == b''
    assert exc_info.value.stderr == b''
    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout none --stderr none --exit-code 42` "
        'exited with status 42\n\n'
        'STDOUT:\n'
        '\n\n'
        'STDERR:\n'
    )


def test_raise_exception_with_stdout_stderr_none():
    global_options = '--stdin none --stdout none --stderr none --exit-code 42'
    ff = FFmpeg(global_options=global_options)
    with pytest.raises(FFRuntimeError) as exc_info:
        ff.run()

    assert str(exc_info.value) == (
        "`ffmpeg --stdin none --stdout none --stderr none --exit-code 42` "
        'exited with status 42\n\n'
        'STDOUT:\n'
        '\n\n'
        'STDERR:\n'
    )


def test_terminate_process():
    global_options = '--long-run'
    ff = FFmpeg(global_options=global_options)

    thread_1 = threading.Thread(target=ff.run)
    thread_1.start()

    while not ff.process:
        time.sleep(0.05)

    print(ff.process.returncode)

    ff.process.terminate()
    thread_1.join()

    assert ff.process.returncode == -15
