# Photot Watermark Tool

一款功能强大的图片水印处理工具，支持文本水印和图片水印，提供批量处理、实时预览和模板管理功能。

## 🚀 最新版本

**当前版本**: v1.0.1
**发布日期**: 2025-10-05
**支持平台**: Windows 10/11
**文件大小**: 54.25 MB

### 📥 下载地址

[![下载最新版本](https://img.shields.io/badge/Download-v1.0.1-blue)](https://github.com/Cherry-CJQ/Photot_Watermark_2/releases/latest)


直接从 [GitHub Releases](https://github.com/Cherry-CJQ/Photot_Watermark_2/releases/latest) 页面下载 `Photot_Watermark.exe` 文件，双击即可运行，无需安装任何依赖。

## ✨ 功能特点

### 🖼️ 图片处理
- **多格式支持**: JPEG, PNG, BMP, TIFF
- **批量处理**: 支持文件夹批量导入和导出
- **拖拽导入**: 直接将图片拖拽到预览区域
- **图片删除**: 支持删除选中图片或清空列表

### 💧 水印功能
- **文本水印**: 自定义文本内容、字体、大小、颜色
- **图片水印**: 支持PNG透明水印图片
- **智能字体**: 0-100相对字体大小，自动适应图片尺寸
- **多种效果**: 粗体、斜体、描边、阴影效果
- **透明度控制**: 精确控制水印透明度
- **旋转角度**: 支持任意角度旋转

### 🎯 位置控制
- **预设位置**: 9种预设位置（左上、中上、右上等）
- **拖拽定位**: 鼠标拖拽精确定位水印位置
- **实时预览**: 实时查看水印效果

### 📋 模板管理
- **模板保存**: 保存常用水印设置为模板
- **模板加载**: 一键加载预设模板
- **自动加载**: 程序启动时自动加载上一次设置
- **模板删除**: 管理自定义模板

### ⚙️ 导出设置
- **格式选择**: 原图格式、JPEG、PNG
- **质量调整**: JPEG压缩质量控制
- **文件命名**: 多种命名规则（前缀、后缀、自定义、时间戳）
- **尺寸调整**: 导出时自动调整图片尺寸

## 🛠️ 技术栈

- **Python 3.8+** - 编程语言
- **PyQt5** - 图形用户界面框架
- **Pillow** - 图像处理库
- **PyInstaller** - 打包工具

## 🚀 快速开始

### 方式一：直接运行（推荐）
1. 从 [GitHub Releases](https://github.com/Cherry-CJQ/Photot_Watermark_2/releases/latest) 下载 `Photot_Watermark.exe`
2. 双击运行程序
3. 无需安装任何依赖，开箱即用

### 方式二：从源代码运行
如果您想从源代码运行，需要先配置环境：

#### 安装Python
确保系统已安装Python 3.8或更高版本。

#### 安装依赖
```bash
pip install -r requirements.txt
```

如果直接安装出现问题，可以分别安装依赖：
```bash
pip install PyQt5
pip install Pillow
pip install PyInstaller
```

#### 运行程序
```bash
python src/main.py
```

## 📁 项目结构
```
Photot_Watermark_2/
├── src/                    # 源代码目录
│   ├── main.py             # 主程序入口
│   └── modules/            # 功能模块
│       ├── config_manager.py    # 配置管理模块
│       ├── image_processor.py   # 图像处理模块
│       └── gui.py               # GUI界面模块
├── tests/                  # 测试代码目录
├── build_windows.py        # Windows打包脚本
├── requirements.txt        # 项目依赖文件
├── README.md               # 项目说明文件
├── PRDoc.md                # 项目需求文档
└── TaskPlan.md             # 任务计划书
```

## 📦 打包程序

### 自动打包
使用提供的打包脚本：
```bash
python build_windows.py
```

### 手动打包
使用PyInstaller打包为Windows可执行文件：
```bash
pyinstaller --name=Photot_Watermark --onefile --windowed --add-data=src/modules;modules src/main.py
```

## 📖 使用指南

### 基本操作流程
1. **导入图片**: 点击"导入图片"或"导入文件夹"，或直接拖拽图片到预览区域
2. **设置水印**:
   - 文本水印：输入文本、选择字体、设置大小和颜色
   - 图片水印：选择水印图片、设置缩放和透明度
3. **调整位置**: 使用预设位置或拖拽精确定位
4. **应用水印**: 点击"应用水印"查看效果
5. **导出图片**: 点击"导出图片"选择导出设置

### 高级功能
- **模板管理**: 保存常用设置，下次快速加载
- **批量处理**: 一次性处理多张图片
- **智能字体**: 字体大小自动适应图片尺寸
- **效果增强**: 使用描边和阴影提高水印可见性

## 🐛 问题反馈

如果您在使用过程中遇到任何问题，请通过以下方式反馈：
1. 在 [GitHub Issues](https://github.com/Cherry-CJQ/Photot_Watermark_2/issues) 提交问题
2. 描述具体问题和复现步骤
3. 提供相关的截图或错误信息

## 📄 许可证

本项目仅供学习使用。

## 👥 贡献者

- Cherry-CJQ - 项目开发者

---

**注意**: 最新版本请始终以 [GitHub Releases](https://github.com/Cherry-CJQ/Photot_Watermark_2/releases) 页面为准。
