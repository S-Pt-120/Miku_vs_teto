import os
import sys


def resource_path(relative_path):
    """统一取资源路径：源码运行时按 .py 所在目录，打包成 exe 后按临时解压目录。"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后，--add-data 的资源会被解压到 sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
