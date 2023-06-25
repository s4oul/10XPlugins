import os
import time
import pyopencl as cl
from datetime import timedelta
from N10X import Editor as editor


"""
python3 -m pip install --target="C:\Program Files\PureDevSoftware\10x\Lib\site-packages" pyopencl --no-user
"""

def __log(msg: str):
    editor.LogToBuildOutput(f'{msg}.\n')


def __log_version():
    opencl_version = cl.get_cl_header_version()
    __log(f'OpenCL: v{opencl_version[0]}.{opencl_version[1]}')


def __plugin_build_opencl(filename: str):
    try:
        __log_version()
        __log(f'Building: {os.path.basename(filename)}')
        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        start = time.time()
        sources = str()
        with open(filename) as fd:
            for line in fd:
                sources += line
        prg = cl.Program(ctx, sources)
        prg.build()
        end = time.time()
        elapsed = (end - start) / 1000
        __log(f'Success: {timedelta(seconds=end - start)}s')
    except Exception as e:
        __log(f'Failure: {e}.\n')


def BuildOpenCL():
    editor.ShowBuildOutput()
    editor.ClearBuildOutput()
    editor.LogToBuildOutput('=== OPENCL ===\n')
    __plugin_build_opencl(editor.GetCurrentFilename())
    editor.LogToBuildOutput('==============\n')
