import subprocess
import threading
import xml.etree.ElementTree as ET
from N10X import Editor as editor

"""
PVS-Studio: https://pvs-studio.com/en/docs/manual/0035/
"""

def __print(msg: str):
    editor.LogToBuildOutput(msg)
    editor.LogToBuildOutput('\n')

def __read_plog():
    plog = f'{editor.GetWorkspaceFilename()}.plog'
    tree = ET.parse(plog)
    root = tree.getroot()

    sln_path = root.find('Solution_Path')
    if sln_path:
        sln_ver = sln_path.find('SolutionVersion')
        plog_ver = sln_path.find('PlogVersion')
        __print(f'Visual Studio: {sln_ver.text}')
        __print(f'Plog Version: {sln_ver.text}')

    for it in root.findall('PVS-Studio_Analysis_Log'):
        project_name = it.find('Project').text
        error_code = it.find('ErrorCode').text
        short_file = it.find('ShortFile').text
        line = it.find('Line').text
        false_alarm = it.find('FalseAlarm').text
        message = it.find('Message').text

        __print(f'Project[{project_name}] - Error[{error_code}] - Alarm[{false_alarm}]')
        __print(f'\t{short_file} - {line}')
        __print(f'\t{message}')


def __pvs_studio_run(cmd: str):
    editor.LogToBuildOutput(f'{cmd}\n')
    process = subprocess.Popen(cmd)
    __read_plog()

def PVSStudioCmd():
    editor.Clear10xOutput()
    editor.ShowBuildOutput()
    editor.ClearBuildOutput()

    editor.LogToBuildOutput('=== PVS-STUDIO ===\n')

    workspace = editor.GetWorkspaceFilename()
    exe = 'C:\Program Files (x86)\PVS-Studio\PVS-Studio_Cmd.exe'
    arg_sln = f'-t "{workspace}"'
    arg_log = f'-o "{workspace}.plog"'
    cmd = f'{exe} {arg_sln} {arg_log}'

    t = threading.Thread(target=__pvs_studio_run, args=(cmd,))
    t.start()

