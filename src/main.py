#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photot Watermark Tool 主程序文件
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QListWidget,
                             QFileDialog, QToolBar, QAction, QStatusBar, QListWidgetItem,
                             QGroupBox, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox,
                             QComboBox, QColorDialog, QMessageBox, QSlider, QInputDialog,
                             QDialog, QDialogButtonBox, QCheckBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor
from PIL import Image
import numpy as np

# 添加项目模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.image_processor import ImageProcessor
from modules.config_manager import ConfigManager

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
        self.image_processor = ImageProcessor()  # 图像处理器
        self.config_manager = ConfigManager()  # 配置管理器
        self.current_watermark_image = None  # 当前水印图片
        self.watermark_color = QColor(255, 255, 255, 128)  # 默认水印颜色
        self.processed_image = None  # 处理后的图像
        self.init_ui()
        self.load_initial_settings()
        
    def init_ui(self):
        """
        初始化用户界面
        """
        # 设置窗口属性
        self.setWindowTitle('Photot 水印工具')
        self.setGeometry(100, 100, 1200, 700)
        
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
        
        # 创建水印控制面板
        self.create_watermark_controls()
        
        # 添加导出按钮
        self.export_button = QPushButton('导出图片')
        self.export_button.clicked.connect(self.export_images)
        self.control_layout.addWidget(self.export_button)
        
        # 将控制区域添加到主布局
        self.main_layout.addWidget(self.control_widget, 1)
        
    def create_watermark_controls(self):
        """
        创建水印控制组件
        """
        # 文本水印组
        text_group = QGroupBox("文本水印")
        text_layout = QFormLayout()
        
        self.text_input = QLineEdit("水印文本")
        text_layout.addRow("文本:", self.text_input)
        
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(8, 100)
        self.font_size_spinbox.setValue(24)
        text_layout.addRow("字体大小:", self.font_size_spinbox)
        
        color_layout = QHBoxLayout()
        self.color_button = QPushButton("选择颜色")
        self.color_button.clicked.connect(self.select_color)
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(30, 30)
        self.color_preview.setStyleSheet("background-color: rgba(255, 255, 255, 128); border: 1px solid black;")
        color_layout.addWidget(self.color_button)
        color_layout.addWidget(self.color_preview)
        color_layout.addStretch()
        text_layout.addRow("颜色:", color_layout)
        
        self.text_opacity_spinbox = QSpinBox()
        self.text_opacity_spinbox.setRange(0, 100)
        self.text_opacity_spinbox.setValue(50)
        self.text_opacity_spinbox.setSuffix(" %")
        text_layout.addRow("透明度:", self.text_opacity_spinbox)
        
        # 文本水印旋转
        text_rotation_layout = QHBoxLayout()
        self.text_rotation_slider = QSlider(Qt.Horizontal)
        self.text_rotation_slider.setRange(0, 360)
        self.text_rotation_slider.setValue(0)
        self.text_rotation_label = QLabel("0°")
        self.text_rotation_slider.valueChanged.connect(
            lambda v: self.text_rotation_label.setText(f"{v}°"))
        text_rotation_layout.addWidget(self.text_rotation_slider)
        text_rotation_layout.addWidget(self.text_rotation_label)
        text_layout.addRow("旋转:", text_rotation_layout)
        
        text_group.setLayout(text_layout)
        self.control_layout.addWidget(text_group)
        
        # 图片水印组
        image_group = QGroupBox("图片水印")
        image_layout = QFormLayout()
        
        image_select_layout = QHBoxLayout()
        self.image_path_label = QLabel("未选择图片")
        self.select_image_button = QPushButton("选择图片")
        self.select_image_button.clicked.connect(self.select_watermark_image)
        image_select_layout.addWidget(self.image_path_label)
        image_select_layout.addWidget(self.select_image_button)
        image_layout.addRow("水印图片:", image_select_layout)
        
        self.scale_spinbox = QDoubleSpinBox()
        self.scale_spinbox.setRange(0.1, 5.0)
        self.scale_spinbox.setSingleStep(0.1)
        self.scale_spinbox.setValue(1.0)
        self.scale_spinbox.setSuffix(" x")
        image_layout.addRow("缩放比例:", self.scale_spinbox)
        
        self.image_opacity_spinbox = QSpinBox()
        self.image_opacity_spinbox.setRange(0, 100)
        self.image_opacity_spinbox.setValue(50)
        self.image_opacity_spinbox.setSuffix(" %")
        image_layout.addRow("透明度:", self.image_opacity_spinbox)
        
        # 图片水印旋转
        image_rotation_layout = QHBoxLayout()
        self.image_rotation_slider = QSlider(Qt.Horizontal)
        self.image_rotation_slider.setRange(0, 360)
        self.image_rotation_slider.setValue(0)
        self.image_rotation_label = QLabel("0°")
        self.image_rotation_slider.valueChanged.connect(
            lambda v: self.image_rotation_label.setText(f"{v}°"))
        image_rotation_layout.addWidget(self.image_rotation_slider)
        image_rotation_layout.addWidget(self.image_rotation_label)
        image_layout.addRow("旋转:", image_rotation_layout)
        
        image_group.setLayout(image_layout)
        self.control_layout.addWidget(image_group)
        
        # 位置控制组
        position_group = QGroupBox("位置控制")
        position_layout = QVBoxLayout()
        
        position_select_layout = QHBoxLayout()
        self.position_combo = QComboBox()
        self.position_combo.addItems([
            "top-left", "top-center", "top-right",
            "middle-left", "center", "middle-right",
            "bottom-left", "bottom-center", "bottom-right"
        ])
        position_select_layout.addWidget(QLabel("预设位置:"))
        position_select_layout.addWidget(self.position_combo)
        position_select_layout.addStretch()
        position_layout.addLayout(position_select_layout)
        
        self.apply_button = QPushButton("应用水印")
        self.apply_button.clicked.connect(self.apply_watermark)
        position_layout.addWidget(self.apply_button)
        
        position_group.setLayout(position_layout)
        self.control_layout.addWidget(position_group)
        
        # 添加模板管理组
        self.create_template_controls()
        
    def create_template_controls(self):
        """
        创建模板管理组件
        """
        template_group = QGroupBox("模板管理")
        template_layout = QVBoxLayout()
        
        # 模板选择
        template_select_layout = QHBoxLayout()
        self.template_combo = QComboBox()
        self.template_combo.addItem("-- 选择模板 --")
        self.refresh_template_list()
        template_select_layout.addWidget(QLabel("模板:"))
        template_select_layout.addWidget(self.template_combo)
        template_select_layout.addStretch()
        template_layout.addLayout(template_select_layout)
        
        # 模板操作按钮
        template_buttons_layout = QHBoxLayout()
        
        self.save_template_button = QPushButton("保存模板")
        self.save_template_button.clicked.connect(self.save_template)
        template_buttons_layout.addWidget(self.save_template_button)
        
        self.load_template_button = QPushButton("加载模板")
        self.load_template_button.clicked.connect(self.load_template)
        template_buttons_layout.addWidget(self.load_template_button)
        
        self.delete_template_button = QPushButton("删除模板")
        self.delete_template_button.clicked.connect(self.delete_template)
        template_buttons_layout.addWidget(self.delete_template_button)
        
        template_layout.addLayout(template_buttons_layout)
        
        template_group.setLayout(template_layout)
        self.control_layout.addWidget(template_group)
        
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
        exit_action.triggered.connect(self.close_application)
        file_menu.addAction(exit_action)
        
        # 模板菜单
        template_menu = menubar.addMenu('模板')
        
        save_template_action = QAction('保存模板', self)
        save_template_action.setShortcut('Ctrl+S')
        save_template_action.triggered.connect(self.save_template)
        template_menu.addAction(save_template_action)
        
        load_template_action = QAction('加载模板', self)
        load_template_action.setShortcut('Ctrl+L')
        load_template_action.triggered.connect(self.load_template)
        template_menu.addAction(load_template_action)
        
        template_menu.addSeparator()
        
        manage_templates_action = QAction('管理模板', self)
        manage_templates_action.triggered.connect(self.manage_templates)
        template_menu.addAction(manage_templates_action)
        
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
                # 重置处理后的图像
                self.processed_image = None
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
            
        # 显示导出设置对话框
        export_dialog = ExportSettingsDialog(self)
        if export_dialog.exec_() != QDialog.Accepted:
            self.status_bar.showMessage('导出已取消')
            return
            
        # 获取导出设置
        export_settings = export_dialog.get_export_settings()
        export_dialog.save_settings()
        
        # 获取上次导出目录
        last_export_dir = self.config_manager.get_setting("export.last_export_dir", "")
        
        # 选择导出目录
        export_dir = QFileDialog.getExistingDirectory(
            self,
            '选择导出目录',
            last_export_dir
        )
        
        if not export_dir:
            self.status_bar.showMessage('导出已取消')
            return
            
        # 检查是否导出到源文件夹
        source_dirs = set(os.path.dirname(path) for path in self.image_files)
        if export_dir in source_dirs:
            # 默认创建 "_watermark" 子文件夹
            watermark_dir = os.path.join(export_dir, "_watermark")
            if not os.path.exists(watermark_dir):
                os.makedirs(watermark_dir)
            
            reply = QMessageBox.information(
                self, "导出目录调整",
                f"为防止覆盖原图，已自动创建子文件夹 '_watermark'。\n导出目录已调整为:\n{watermark_dir}\n\n是否继续导出？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                export_dir = watermark_dir
            else:
                self.status_bar.showMessage('导出已取消')
                return
        
        try:
            # 保存导出目录
            self.config_manager.set_setting("export.last_export_dir", export_dir)
            self.config_manager.save_config()
            
            # 导出所有图片
            success_count = 0
            total_count = len(self.image_files)
            
            for i, image_path in enumerate(self.image_files):
                try:
                    # 生成输出文件名
                    original_name = os.path.basename(image_path)
                    name, ext = os.path.splitext(original_name)
                    
                    naming_rule = export_settings["naming_rule"]
                    if naming_rule == "添加前缀":
                        output_name = f"{export_settings['prefix']}{original_name}"
                    elif naming_rule == "添加后缀":
                        output_name = f"{name}{export_settings['suffix']}{ext}"
                    else:  # 保留原文件名
                        output_name = original_name
                    
                    # 确定文件格式和扩展名
                    export_format = export_settings["format"]
                    if export_format == "JPEG":
                        output_ext = ".jpg"
                        file_format = "JPEG"
                    else:  # PNG
                        output_ext = ".png"
                        file_format = "PNG"
                    
                    # 如果扩展名不匹配，则替换
                    if not output_name.lower().endswith(output_ext.lower()):
                        output_name = os.path.splitext(output_name)[0] + output_ext
                    
                    output_path = os.path.join(export_dir, output_name)
                    
                    # 检查文件是否已存在
                    if os.path.exists(output_path):
                        reply = QMessageBox.question(
                            self, "文件已存在",
                            f"文件 {output_name} 已存在，是否覆盖？",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No
                        )
                        if reply == QMessageBox.No:
                            continue
                    
                    # 加载并处理图片
                    image = self.image_processor.load_image(image_path)
                    
                    # 应用当前水印设置
                    use_text = bool(self.text_input.text().strip())
                    use_image = self.current_watermark_image is not None
                    
                    if use_text or use_image:
                        position = self.position_combo.currentText()
                        
                        # 应用文本水印
                        if use_text:
                            text = self.text_input.text()
                            font_size = self.font_size_spinbox.value()
                            opacity = self.text_opacity_spinbox.value()
                            color = (self.watermark_color.red(),
                                    self.watermark_color.green(),
                                    self.watermark_color.blue(),
                                    self.watermark_color.alpha())
                            rotation = self.text_rotation_slider.value()
                            
                            image = self.image_processor.add_text_watermark(
                                image, text, position,
                                font_size=font_size,
                                color=color,
                                opacity=opacity,
                                rotation=rotation
                            )
                        
                        # 应用图片水印
                        if use_image:
                            scale = self.scale_spinbox.value()
                            opacity = self.image_opacity_spinbox.value()
                            rotation = self.image_rotation_slider.value()
                            
                            image = self.image_processor.add_image_watermark(
                                image, self.current_watermark_image, position,
                                scale=scale,
                                opacity=opacity,
                                rotation=rotation
                            )
                    
                    # 调整图片尺寸
                    if export_settings["resize_enabled"]:
                        img_width, img_height = image.size
                        max_width = export_settings["max_width"]
                        max_height = export_settings["max_height"]
                        if img_width > max_width or img_height > max_height:
                            # 计算新的尺寸，保持宽高比
                            ratio = min(max_width / img_width, max_height / img_height)
                            new_width = int(img_width * ratio)
                            new_height = int(img_height * ratio)
                            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # 保存图片
                    quality = export_settings["quality"]
                    self.image_processor.save_image(image, output_path, quality=quality, file_format=file_format)
                    success_count += 1
                    
                    # 更新状态
                    self.status_bar.showMessage(f'正在导出: {i+1}/{total_count} - {output_name}')
                    
                except Exception as e:
                    print(f"导出图片 {image_path} 失败: {e}")
                    QMessageBox.warning(self, "导出错误", f"导出图片 {os.path.basename(image_path)} 失败: {str(e)}")
            
            # 显示导出结果
            if success_count > 0:
                self.status_bar.showMessage(f'导出完成: {success_count}/{total_count} 张图片已导出到 {export_dir}')
                QMessageBox.information(self, "导出完成",
                                      f"成功导出 {success_count}/{total_count} 张图片到:\n{export_dir}")
            else:
                self.status_bar.showMessage('导出失败: 没有图片被导出')
                QMessageBox.warning(self, "导出失败", "没有图片被导出")
                
        except Exception as e:
            self.status_bar.showMessage(f'导出失败: {str(e)}')
            QMessageBox.warning(self, "导出错误", f"导出失败: {str(e)}")
            
    def select_color(self):
        """
        选择水印颜色
        """
        color = QColorDialog.getColor(self.watermark_color)
        if color.isValid():
            self.watermark_color = color
            self.color_preview.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid black;"
            )
            
    def select_watermark_image(self):
        """
        选择水印图片
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            '选择水印图片', 
            '', 
            '图片文件 (*.png *.jpg *.jpeg *.bmp *.tiff)'
        )
        
        if file_path:
            self.image_path_label.setText(file_path)
            try:
                self.current_watermark_image = Image.open(file_path)
                # 确保图片是RGBA模式
                if self.current_watermark_image.mode != "RGBA":
                    self.current_watermark_image = self.current_watermark_image.convert("RGBA")
                self.status_bar.showMessage(f'已选择水印图片: {os.path.basename(file_path)}')
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法加载水印图片: {str(e)}")
                self.current_watermark_image = None
                
    def apply_watermark(self):
        """
        应用水印
        """
        if self.current_image_index < 0 or self.current_image_index >= len(self.image_files):
            self.status_bar.showMessage('请先选择一张图片')
            return
            
        try:
            # 加载当前图片
            image_path = self.image_files[self.current_image_index]
            image = self.image_processor.load_image(image_path)
            
            # 检查是否同时使用文本和图片水印
            use_text = bool(self.text_input.text().strip())
            use_image = self.current_watermark_image is not None
            
            if not use_text and not use_image:
                self.status_bar.showMessage('请输入水印文本或选择水印图片')
                return
                
            # 获取位置
            position = self.position_combo.currentText()
            
            # 应用文本水印
            if use_text:
                text = self.text_input.text()
                font_size = self.font_size_spinbox.value()
                opacity = self.text_opacity_spinbox.value()
                color = (self.watermark_color.red(), 
                        self.watermark_color.green(), 
                        self.watermark_color.blue(), 
                        self.watermark_color.alpha())
                rotation = self.text_rotation_slider.value()
                
                image = self.image_processor.add_text_watermark(
                    image, text, position,
                    font_size=font_size,
                    color=color,
                    opacity=opacity,
                    rotation=rotation
                )
                
            # 应用图片水印
            if use_image:
                scale = self.scale_spinbox.value()
                opacity = self.image_opacity_spinbox.value()
                rotation = self.image_rotation_slider.value()
                
                image = self.image_processor.add_image_watermark(
                    image, self.current_watermark_image, position,
                    scale=scale,
                    opacity=opacity,
                    rotation=rotation
                )
                
            # 保存处理后的图像
            self.processed_image = image
            
            # 显示添加水印后的图片
            self.display_processed_image(image)
            self.status_bar.showMessage('水印已应用')
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"应用水印失败: {str(e)}")
            
    def display_processed_image(self, image):
        """
        显示处理后的图片
        """
        try:
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
        except Exception as e:
            self.preview_label.setText(f'无法显示处理后的图片: {str(e)}')
            print(f"显示处理后的图片失败: {e}")
            
    def load_initial_settings(self):
        """
        加载初始设置
        """
        try:
            # 加载窗口设置
            width = self.config_manager.get_setting("app.window_geometry.width", 1200)
            height = self.config_manager.get_setting("app.window_geometry.height", 700)
            x = self.config_manager.get_setting("app.window_geometry.x", 100)
            y = self.config_manager.get_setting("app.window_geometry.y", 100)
            self.setGeometry(x, y, width, height)
            
            # 加载水印设置
            text_content = self.config_manager.get_setting("watermark.text.content", "水印文本")
            self.text_input.setText(text_content)
            
            font_size = self.config_manager.get_setting("watermark.text.font_size", 24)
            self.font_size_spinbox.setValue(font_size)
            
            color_data = self.config_manager.get_setting("watermark.text.color", [255, 255, 255, 128])
            self.watermark_color = QColor(color_data[0], color_data[1], color_data[2], color_data[3])
            self.color_preview.setStyleSheet(
                f"background-color: rgba({color_data[0]}, {color_data[1]}, {color_data[2]}, {color_data[3]}); border: 1px solid black;"
            )
            
            text_opacity = self.config_manager.get_setting("watermark.text.opacity", 50)
            self.text_opacity_spinbox.setValue(text_opacity)
            
            text_rotation = self.config_manager.get_setting("watermark.text.rotation", 0)
            self.text_rotation_slider.setValue(text_rotation)
            
            image_scale = self.config_manager.get_setting("watermark.image.scale", 1.0)
            self.scale_spinbox.setValue(image_scale)
            
            image_opacity = self.config_manager.get_setting("watermark.image.opacity", 50)
            self.image_opacity_spinbox.setValue(image_opacity)
            
            image_rotation = self.config_manager.get_setting("watermark.image.rotation", 0)
            self.image_rotation_slider.setValue(image_rotation)
            
            position = self.config_manager.get_setting("watermark.position", "top-left")
            index = self.position_combo.findText(position)
            if index >= 0:
                self.position_combo.setCurrentIndex(index)
                
        except Exception as e:
            print(f"加载初始设置失败: {e}")
            
    def save_current_settings(self):
        """
        保存当前设置
        """
        try:
            # 保存窗口设置
            geometry = self.geometry()
            self.config_manager.set_setting("app.window_geometry.width", geometry.width())
            self.config_manager.set_setting("app.window_geometry.height", geometry.height())
            self.config_manager.set_setting("app.window_geometry.x", geometry.x())
            self.config_manager.set_setting("app.window_geometry.y", geometry.y())
            
            # 保存水印设置
            self.config_manager.set_setting("watermark.text.content", self.text_input.text())
            self.config_manager.set_setting("watermark.text.font_size", self.font_size_spinbox.value())
            self.config_manager.set_setting("watermark.text.color", [
                self.watermark_color.red(),
                self.watermark_color.green(),
                self.watermark_color.blue(),
                self.watermark_color.alpha()
            ])
            self.config_manager.set_setting("watermark.text.opacity", self.text_opacity_spinbox.value())
            self.config_manager.set_setting("watermark.text.rotation", self.text_rotation_slider.value())
            
            self.config_manager.set_setting("watermark.image.scale", self.scale_spinbox.value())
            self.config_manager.set_setting("watermark.image.opacity", self.image_opacity_spinbox.value())
            self.config_manager.set_setting("watermark.image.rotation", self.image_rotation_slider.value())
            
            self.config_manager.set_setting("watermark.position", self.position_combo.currentText())
            
            # 保存配置
            self.config_manager.save_config()
            
        except Exception as e:
            print(f"保存设置失败: {e}")
            
    def refresh_template_list(self):
        """
        刷新模板列表
        """
        self.template_combo.clear()
        self.template_combo.addItem("-- 选择模板 --")
        
        template_names = self.config_manager.get_template_names()
        for name in template_names:
            self.template_combo.addItem(name)
            
    def save_template(self):
        """
        保存当前设置为模板
        """
        template_name, ok = QInputDialog.getText(self, '保存模板', '请输入模板名称:')
        if ok and template_name:
            try:
                # 收集当前设置
                text_settings = {
                    "content": self.text_input.text(),
                    "font_size": self.font_size_spinbox.value(),
                    "color": [
                        self.watermark_color.red(),
                        self.watermark_color.green(),
                        self.watermark_color.blue(),
                        self.watermark_color.alpha()
                    ],
                    "opacity": self.text_opacity_spinbox.value(),
                    "rotation": self.text_rotation_slider.value()
                }
                
                image_settings = {
                    "scale": self.scale_spinbox.value(),
                    "opacity": self.image_opacity_spinbox.value(),
                    "rotation": self.image_rotation_slider.value()
                }
                
                position_settings = self.position_combo.currentText()
                
                # 创建模板数据
                template_data = self.config_manager.create_watermark_template(
                    text_settings, image_settings, position_settings
                )
                
                # 保存模板
                self.config_manager.save_template(template_name, template_data)
                self.refresh_template_list()
                
                QMessageBox.information(self, "成功", f"模板 '{template_name}' 已保存")
                
            except Exception as e:
                QMessageBox.warning(self, "错误", f"保存模板失败: {str(e)}")
                
    def load_template(self):
        """
        加载选中的模板
        """
        template_name = self.template_combo.currentText()
        if template_name == "-- 选择模板 --":
            QMessageBox.warning(self, "警告", "请先选择一个模板")
            return
            
        try:
            template_data = self.config_manager.load_template(template_name)
            
            # 应用文本设置
            if "text" in template_data:
                text_settings = template_data["text"]
                self.text_input.setText(text_settings.get("content", "水印文本"))
                self.font_size_spinbox.setValue(text_settings.get("font_size", 24))
                
                color_data = text_settings.get("color", [255, 255, 255, 128])
                self.watermark_color = QColor(color_data[0], color_data[1], color_data[2], color_data[3])
                self.color_preview.setStyleSheet(
                    f"background-color: rgba({color_data[0]}, {color_data[1]}, {color_data[2]}, {color_data[3]}); border: 1px solid black;"
                )
                
                self.text_opacity_spinbox.setValue(text_settings.get("opacity", 50))
                self.text_rotation_slider.setValue(text_settings.get("rotation", 0))
            
            # 应用图片设置
            if "image" in template_data:
                image_settings = template_data["image"]
                self.scale_spinbox.setValue(image_settings.get("scale", 1.0))
                self.image_opacity_spinbox.setValue(image_settings.get("opacity", 50))
                self.image_rotation_slider.setValue(image_settings.get("rotation", 0))
            
            # 应用位置设置
            if "position" in template_data:
                position = template_data["position"]
                index = self.position_combo.findText(position)
                if index >= 0:
                    self.position_combo.setCurrentIndex(index)
                    
            QMessageBox.information(self, "成功", f"模板 '{template_name}' 已加载")
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载模板失败: {str(e)}")
            
    def delete_template(self):
        """
        删除选中的模板
        """
        template_name = self.template_combo.currentText()
        if template_name == "-- 选择模板 --":
            QMessageBox.warning(self, "警告", "请先选择一个模板")
            return
            
        reply = QMessageBox.question(self, "确认删除",
                                   f"确定要删除模板 '{template_name}' 吗？",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.config_manager.delete_template(template_name)
                self.refresh_template_list()
                QMessageBox.information(self, "成功", f"模板 '{template_name}' 已删除")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"删除模板失败: {str(e)}")
                
    def manage_templates(self):
        """
        管理模板对话框
        """
        # TODO: 实现模板管理对话框
        QMessageBox.information(self, "模板管理", "模板管理功能正在开发中...")
        
    def close_application(self):
        """
        关闭应用程序
        """
        self.save_current_settings()
        self.close()

class ExportSettingsDialog(QDialog):
    """
    导出设置对话框
    """
    
    def __init__(self, parent=None):
        """
        初始化导出设置对话框
        """
        super().__init__(parent)
        self.config_manager = parent.config_manager if parent else ConfigManager()
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """
        初始化用户界面
        """
        self.setWindowTitle("导出设置")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # 导出格式设置
        format_group = QGroupBox("导出格式")
        format_layout = QFormLayout()
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPEG", "PNG"])
        format_layout.addRow("格式:", self.format_combo)
        
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(0, 100)
        self.quality_slider.setValue(95)
        self.quality_label = QLabel("95%")
        self.quality_slider.valueChanged.connect(
            lambda v: self.quality_label.setText(f"{v}%"))
        
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_label)
        format_layout.addRow("JPEG质量:", quality_layout)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # 文件命名规则
        naming_group = QGroupBox("文件命名")
        naming_layout = QFormLayout()
        
        self.naming_combo = QComboBox()
        self.naming_combo.addItems([
            "保留原文件名",
            "添加前缀",
            "添加后缀"
        ])
        self.naming_combo.currentTextChanged.connect(self.on_naming_rule_changed)
        naming_layout.addRow("命名规则:", self.naming_combo)
        
        self.prefix_input = QLineEdit("wm_")
        naming_layout.addRow("前缀:", self.prefix_input)
        
        self.suffix_input = QLineEdit("_watermarked")
        naming_layout.addRow("后缀:", self.suffix_input)
        
        naming_group.setLayout(naming_layout)
        layout.addWidget(naming_group)
        
        # 图片尺寸调整
        resize_group = QGroupBox("图片尺寸调整")
        resize_layout = QFormLayout()
        
        self.resize_checkbox = QCheckBox("启用尺寸调整")
        self.resize_checkbox.toggled.connect(self.on_resize_toggled)
        resize_layout.addRow(self.resize_checkbox)
        
        self.max_width_spinbox = QSpinBox()
        self.max_width_spinbox.setRange(100, 10000)
        self.max_width_spinbox.setValue(1920)
        self.max_width_spinbox.setSuffix(" px")
        resize_layout.addRow("最大宽度:", self.max_width_spinbox)
        
        self.max_height_spinbox = QSpinBox()
        self.max_height_spinbox.setRange(100, 10000)
        self.max_height_spinbox.setValue(1080)
        self.max_height_spinbox.setSuffix(" px")
        resize_layout.addRow("最大高度:", self.max_height_spinbox)
        
        resize_group.setLayout(resize_layout)
        layout.addWidget(resize_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # 初始状态
        self.on_naming_rule_changed(self.naming_combo.currentText())
        self.on_resize_toggled(self.resize_checkbox.isChecked())
        
    def on_naming_rule_changed(self, rule):
        """
        命名规则改变时的处理
        """
        is_prefix = rule == "添加前缀"
        is_suffix = rule == "添加后缀"
        
        self.prefix_input.setEnabled(is_prefix)
        self.suffix_input.setEnabled(is_suffix)
        
    def on_resize_toggled(self, enabled):
        """
        尺寸调整开关状态改变时的处理
        """
        self.max_width_spinbox.setEnabled(enabled)
        self.max_height_spinbox.setEnabled(enabled)
        
    def load_settings(self):
        """
        加载导出设置
        """
        try:
            export_format = self.config_manager.get_setting("export.format", "JPEG")
            index = self.format_combo.findText(export_format)
            if index >= 0:
                self.format_combo.setCurrentIndex(index)
                
            quality = self.config_manager.get_setting("export.quality", 95)
            self.quality_slider.setValue(quality)
            
            naming_rule = self.config_manager.get_setting("export.naming_rule", "original")
            if naming_rule == "prefix":
                self.naming_combo.setCurrentText("添加前缀")
            elif naming_rule == "suffix":
                self.naming_combo.setCurrentText("添加后缀")
            else:
                self.naming_combo.setCurrentText("保留原文件名")
                
            prefix = self.config_manager.get_setting("export.prefix", "wm_")
            self.prefix_input.setText(prefix)
            
            suffix = self.config_manager.get_setting("export.suffix", "_watermarked")
            self.suffix_input.setText(suffix)
            
            resize_enabled = self.config_manager.get_setting("export.resize_enabled", False)
            self.resize_checkbox.setChecked(resize_enabled)
            
            max_width = self.config_manager.get_setting("export.max_width", 1920)
            self.max_width_spinbox.setValue(max_width)
            
            max_height = self.config_manager.get_setting("export.max_height", 1080)
            self.max_height_spinbox.setValue(max_height)
            
        except Exception as e:
            print(f"加载导出设置失败: {e}")
            
    def save_settings(self):
        """
        保存导出设置
        """
        try:
            # 保存格式设置
            self.config_manager.set_setting("export.format", self.format_combo.currentText())
            self.config_manager.set_setting("export.quality", self.quality_slider.value())
            
            # 保存命名规则
            naming_rule = self.naming_combo.currentText()
            if naming_rule == "添加前缀":
                self.config_manager.set_setting("export.naming_rule", "prefix")
            elif naming_rule == "添加后缀":
                self.config_manager.set_setting("export.naming_rule", "suffix")
            else:
                self.config_manager.set_setting("export.naming_rule", "original")
                
            self.config_manager.set_setting("export.prefix", self.prefix_input.text())
            self.config_manager.set_setting("export.suffix", self.suffix_input.text())
            
            # 保存尺寸设置
            self.config_manager.set_setting("export.resize_enabled", self.resize_checkbox.isChecked())
            self.config_manager.set_setting("export.max_width", self.max_width_spinbox.value())
            self.config_manager.set_setting("export.max_height", self.max_height_spinbox.value())
            
            # 保存配置
            self.config_manager.save_config()
            
        except Exception as e:
            print(f"保存导出设置失败: {e}")
            
    def get_export_settings(self):
        """
        获取导出设置
        """
        return {
            "format": self.format_combo.currentText(),
            "quality": self.quality_slider.value(),
            "naming_rule": self.naming_combo.currentText(),
            "prefix": self.prefix_input.text(),
            "suffix": self.suffix_input.text(),
            "resize_enabled": self.resize_checkbox.isChecked(),
            "max_width": self.max_width_spinbox.value(),
            "max_height": self.max_height_spinbox.value()
        }
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