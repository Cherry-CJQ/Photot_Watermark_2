#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photot Watermark Tool 主程序文件
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QListWidget,
                             QFileDialog, QToolBar, QAction, QStatusBar, QListWidgetItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PIL import Image
import numpy as np

class MainWindow(QMainWindow):
    """
    主窗口类
    """
    
    def __init__(self):
        """
        初始化主窗口
        """
        super().__init__()
        self.image_files = []  # 存储导入的图片文件路径
        self.current_image_index = -1  # 当前选中的图片索引
        self.init_ui()
        
    def init_ui(self):
        """
        初始化用户界面
        """
        # 设置窗口属性
        self.setWindowTitle('Photot 水印工具')
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # 创建左侧图片列表区域
        self.create_image_list_panel()
        
        # 创建中间预览区域
        self.create_preview_panel()
        
        # 创建右侧控制面板
        self.create_control_panel()
        
        # 创建菜单栏和工具栏
        self.create_menus_and_toolbar()
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('就绪')
        
    def create_image_list_panel(self):
        """
        创建图片列表面板
        """
        # 创建图片列表区域的部件
        self.image_list_widget = QWidget()
        self.image_list_layout = QVBoxLayout(self.image_list_widget)
        self.image_list_layout.setContentsMargins(5, 5, 5, 5)
        
        # 添加标题
        image_list_label = QLabel('图片列表')
        image_list_label.setAlignment(Qt.AlignCenter)
        self.image_list_layout.addWidget(image_list_label)
        
        # 添加图片列表
        self.image_list = QListWidget()
        self.image_list.itemClicked.connect(self.on_image_selected)
        self.image_list_layout.addWidget(self.image_list)
        
        # 添加导入按钮
        self.import_button = QPushButton('导入图片')
        self.import_button.clicked.connect(self.import_images)
        self.image_list_layout.addWidget(self.import_button)
        
        # 将图片列表区域添加到主布局
        self.main_layout.addWidget(self.image_list_widget, 1)
        
    def create_preview_panel(self):
        """
        创建预览面板
        """
        # 创建预览区域的部件
        self.preview_widget = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_widget)
        self.preview_layout.setContentsMargins(5, 5, 5, 5)
        
        # 添加标题
        preview_label = QLabel('预览')
        preview_label.setAlignment(Qt.AlignCenter)
        self.preview_layout.addWidget(preview_label)
        
        # 添加预览标签
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setText('请选择图片进行预览')
        self.preview_label.setMinimumSize(400, 400)
        self.preview_label.setStyleSheet("border: 1px solid gray;")
        self.preview_layout.addWidget(self.preview_label)
        
        # 将预览区域添加到主布局
        self.main_layout.addWidget(self.preview_widget, 2)
        
    def create_control_panel(self):
        """
        创建控制面板
        """
        # 创建控制区域的部件
        self.control_widget = QWidget()
        self.control_layout = QVBoxLayout(self.control_widget)
        self.control_layout.setContentsMargins(5, 5, 5, 5)
        
        # 添加标题
        control_label = QLabel('水印控制')
        control_label.setAlignment(Qt.AlignCenter)
        self.control_layout.addWidget(control_label)
        
        # 添加控制组件（暂时留空，后续添加）
        control_placeholder = QLabel('水印控制面板')
        control_placeholder.setAlignment(Qt.AlignCenter)
        control_placeholder.setMinimumHeight(400)
        control_placeholder.setStyleSheet("border: 1px solid gray;")
        self.control_layout.addWidget(control_placeholder)
        
        # 添加导出按钮
        self.export_button = QPushButton('导出图片')
        self.export_button.clicked.connect(self.export_images)
        self.control_layout.addWidget(self.export_button)
        
        # 将控制区域添加到主布局
        self.main_layout.addWidget(self.control_widget, 1)
        
    def create_menus_and_toolbar(self):
        """
        创建菜单栏和工具栏
        """
        # 创建菜单栏
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        import_action = QAction('导入图片', self)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.import_images)
        file_menu.addAction(import_action)
        
        export_action = QAction('导出图片', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_images)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 创建工具栏
        toolbar = self.addToolBar('工具栏')
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        
        # 添加工具栏按钮
        toolbar.addAction(import_action)
        toolbar.addAction(export_action)
        
    def import_images(self):
        """
        导入图片
        """
        # 打开文件选择对话框
        file_names, _ = QFileDialog.getOpenFileNames(
            self, 
            '选择图片文件', 
            '', 
            '图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff *.tif)'
        )
        
        if file_names:
            # 添加图片到列表
            for file_name in file_names:
                # 检查是否已导入该图片
                if file_name not in self.image_files:
                    self.image_files.append(file_name)
                    # 创建列表项
                    item = QListWidgetItem(os.path.basename(file_name))
                    # 生成缩略图
                    thumbnail = self.generate_thumbnail(file_name)
                    if thumbnail:
                        item.setIcon(thumbnail)
                    self.image_list.addItem(item)
            
            self.status_bar.showMessage(f'已导入 {len(file_names)} 张图片')
        
    def generate_thumbnail(self, image_path):
        """
        生成图片缩略图
        """
        try:
            # 使用PIL打开图片
            image = Image.open(image_path)
            # 调整图片大小作为缩略图
            image.thumbnail((64, 64), Image.Resampling.LANCZOS)
            
            # 转换为numpy数组
            if image.mode == "RGB":
                r, g, b = image.split()
                image = Image.merge("RGB", (b, g, r))
            elif image.mode == "RGBA":
                r, g, b, a = image.split()
                image = Image.merge("RGBA", (b, g, r, a))
            elif image.mode == "L":
                image = image.convert("RGB")
            
            # 转换为QImage
            image_data = image.tobytes("raw", "RGB")
            qimage = QImage(image_data, image.size[0], image.size[1], QImage.Format_RGB888)
            qpixmap = QPixmap.fromImage(qimage)
            return QIcon(qpixmap)
        except Exception as e:
            print(f"生成缩略图失败: {e}")
            return None
        
    def on_image_selected(self, item):
        """
        当图片被选中时的处理函数
        """
        self.current_image_index = self.image_list.row(item)
        self.display_image(self.current_image_index)
        
    def display_image(self, index):
        """
        显示选中的图片
        """
        if 0 <= index < len(self.image_files):
            try:
                # 使用PIL打开图片
                image = Image.open(self.image_files[index])
                # 调整图片大小以适应预览区域
                image = image.copy()  # 创建副本避免影响原图
                max_width, max_height = 600, 500
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # 转换为numpy数组
                if image.mode == "RGB":
                    r, g, b = image.split()
                    image = Image.merge("RGB", (b, g, r))
                elif image.mode == "RGBA":
                    r, g, b, a = image.split()
                    image = Image.merge("RGBA", (b, g, r, a))
                elif image.mode == "L":
                    image = image.convert("RGB")
                
                # 转换为QImage并显示
                image_data = image.tobytes("raw", "RGB")
                qimage = QImage(image_data, image.size[0], image.size[1], QImage.Format_RGB888)
                qpixmap = QPixmap.fromImage(qimage)
                self.preview_label.setPixmap(qpixmap)
                self.preview_label.setAlignment(Qt.AlignCenter)
                self.status_bar.showMessage(f'正在预览: {os.path.basename(self.image_files[index])}')
            except Exception as e:
                self.preview_label.setText(f'无法加载图片: {str(e)}')
                print(f"显示图片失败: {e}")
        
    def export_images(self):
        """
        导出图片
        """
        if not self.image_files:
            self.status_bar.showMessage('请先导入图片')
            return
            
        # 选择导出目录
        export_dir = QFileDialog.getExistingDirectory(self, '选择导出目录')
        if export_dir:
            self.status_bar.showMessage(f'导出功能待实现，目录: {export_dir}')
        else:
            self.status_bar.showMessage('导出已取消')

def main():
    """
    主函数
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()