# Photot_Watermark_2

水印工具：作业2

## 项目简介

这是一款基于Python开发的Windows桌面应用程序，用于给图片添加文本水印和图片水印。支持批量处理、实时预览和模板管理功能。

## 功能特点

- 支持多种图片格式导入（JPEG, PNG, BMP, TIFF）
- 支持文本水印和图片水印
- 提供实时预览功能
- 支持批量处理图片
- 可保存和管理水印模板

## 技术栈

- Python 3.8+
- PyQt5/PyQt6 或 Tkinter（GUI框架）
- Pillow（图像处理库）
- PyInstaller（打包工具）

## 环境配置

### 安装Python
确保系统已安装Python 3.8或更高版本。

### 安装依赖
```bash
pip install -r requirements.txt
```

## 项目结构
```
Photot_Watermark_2/
├── src/                 # 源代码目录
│   ├── main.py          # 主程序入口
│   └── modules/         # 功能模块
│       ├── config_manager.py   # 配置管理模块
│       ├── image_processor.py  # 图像处理模块
│       └── gui.py              # GUI界面模块
├── tests/               # 测试代码目录
├── requirements.txt     # 项目依赖文件
├── README.md            # 项目说明文件
├── PRDoc.md             # 项目需求文档
└── TaskPlan.md          # 任务计划书
```

## 运行程序

```bash
python src/main.py
```

## 打包程序

使用PyInstaller打包为Windows可执行文件：
```bash
pyinstaller --onefile src/main.py
```

## 使用说明

待完善...