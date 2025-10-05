#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Windows 打包脚本
使用 PyInstaller 打包为可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_windows():
    """构建 Windows 版本"""
    print("开始构建 Windows 版本...")
    
    # 清理之前的构建
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller 配置
    pyinstaller_cmd = [
        "pyinstaller",
        "--name=Photot_Watermark",
        "--onefile",
        "--windowed",
        "--add-data=src/modules;modules",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=PIL._imagingtk",
        "--hidden-import=PIL._webp",
        "--collect-all=PIL",
        "src/main.py"
    ]
    
    try:
        # 执行打包命令
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True)
        print("打包成功！")
        print(result.stdout)
        
        # 检查生成的可执行文件
        exe_path = Path("dist/Photot_Watermark.exe")
        if exe_path.exists():
            print(f"可执行文件已生成: {exe_path}")
            print(f"文件大小: {exe_path.stat().st_size / (1024*1024):.2f} MB")
        else:
            print("警告: 可执行文件未找到")
            
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("错误: 未找到 PyInstaller，请先安装: pip install pyinstaller")
        sys.exit(1)

def create_installer():
    """创建安装包（可选）"""
    print("创建安装包...")
    
    # 这里可以添加 NSIS 或 Inno Setup 脚本
    # 暂时只打包为单个可执行文件
    pass

if __name__ == "__main__":
    build_windows()