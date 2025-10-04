#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图像处理模块
负责图片导入、导出和水印处理
"""

from PIL import Image, ImageDraw, ImageFont
import os

class ImageProcessor:
    """
    图像处理器类
    """
    
    def __init__(self):
        """
        初始化图像处理器
        """
        pass
    
    def load_image(self, file_path):
        """
        加载图片
        """
        try:
            image = Image.open(file_path)
            # 转换为RGBA模式以支持透明度
            if image.mode != "RGBA":
                image = image.convert("RGBA")
            return image
        except Exception as e:
            raise Exception(f"无法加载图片 {file_path}: {str(e)}")
    
    def save_image(self, image, file_path, quality=95, file_format=None):
        """
        保存图片
        """
        try:
            # 如果没有指定格式，根据文件扩展名确定
            if file_format is None:
                file_format = file_path.split('.')[-1].upper()
                if file_format == 'JPG':
                    file_format = 'JPEG'
            
            # 对于JPEG格式，需要转换为RGB模式（不支持透明度）
            if file_format == 'JPEG':
                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                rgb_image.save(file_path, format=file_format, quality=quality)
            else:
                image.save(file_path, format=file_format)
        except Exception as e:
            raise Exception(f"无法保存图片 {file_path}: {str(e)}")
    
    def add_text_watermark(self, image, text, position, **kwargs):
        """
        添加文本水印
        
        Args:
            image: PIL图像对象
            text: 水印文本
            position: 水印位置 (x, y) 或 预设位置字符串
            kwargs: 其他参数
                - font_path: 字体文件路径
                - font_size: 字体大小
                - color: 文本颜色 (R, G, B, A)
                - opacity: 透明度 (0-100)
        
        Returns:
            添加水印后的图像
        """
        try:
            # 创建水印图层
            watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark_layer)
            
            # 获取参数
            font_path = kwargs.get('font_path', None)
            font_size = kwargs.get('font_size', 24)
            color = kwargs.get('color', (255, 255, 255, 128))  # 默认白色半透明
            opacity = kwargs.get('opacity', 100)
            
            # 处理透明度
            if len(color) == 3:
                r, g, b = color
                a = int(255 * opacity / 100)
            elif len(color) == 4:
                r, g, b, a = color
                a = int(a * opacity / 100)
            
            # 加载字体
            try:
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    # 使用默认字体
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # 计算文本大小
            try:
                # 新版本PIL
                left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
                text_width = right - left
                text_height = bottom - top
            except:
                # 兼容旧版本PIL
                text_width, text_height = draw.textsize(text, font=font)
            
            # 解析位置
            x, y = self._parse_position(position, image.size, (text_width, text_height))
            
            # 绘制文本水印
            draw.text((x, y), text, font=font, fill=(r, g, b, a))
            
            # 将水印图层与原图合并
            result = Image.alpha_composite(image, watermark_layer)
            return result
        except Exception as e:
            raise Exception(f"添加文本水印失败: {str(e)}")
    
    def add_image_watermark(self, image, watermark_image, position, **kwargs):
        """
        添加图片水印
        
        Args:
            image: PIL图像对象（背景图）
            watermark_image: PIL图像对象（水印图）
            position: 水印位置 (x, y) 或 预设位置字符串
            kwargs: 其他参数
                - scale: 缩放比例
                - opacity: 透明度 (0-100)
        
        Returns:
            添加水印后的图像
        """
        try:
            # 获取参数
            scale = kwargs.get('scale', 1.0)
            opacity = kwargs.get('opacity', 100)
            
            # 调整水印图片大小
            if scale != 1.0:
                new_width = int(watermark_image.width * scale)
                new_height = int(watermark_image.height * scale)
                watermark_image = watermark_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 处理透明度
            if opacity < 100:
                if watermark_image.mode == "RGBA":
                    # 分离alpha通道并调整透明度
                    r, g, b, alpha = watermark_image.split()
                    alpha = alpha.point(lambda x: int(x * opacity / 100))
                    watermark_image = Image.merge('RGBA', (r, g, b, alpha))
                else:
                    # 对于非RGBA图像，先转换为RGBA
                    watermark_image = watermark_image.convert("RGBA")
                    r, g, b, alpha = watermark_image.split()
                    alpha = alpha.point(lambda x: int(x * opacity / 100))
                    watermark_image = Image.merge('RGBA', (r, g, b, alpha))
            
            # 确保水印图片是RGBA模式
            if watermark_image.mode != "RGBA":
                watermark_image = watermark_image.convert("RGBA")
            
            # 解析位置
            x, y = self._parse_position(position, image.size, watermark_image.size)
            
            # 创建结果图像
            result = image.copy()
            
            # 粘贴水印图片
            result.paste(watermark_image, (x, y), watermark_image)
            return result
        except Exception as e:
            raise Exception(f"添加图片水印失败: {str(e)}")
    
    def _parse_position(self, position, image_size, watermark_size):
        """
        解析水印位置
        
        Args:
            position: 位置参数，可以是(x, y)元组或预设位置字符串
            image_size: 背景图片尺寸 (width, height)
            watermark_size: 水印尺寸 (width, height)
        
        Returns:
            (x, y) 位置坐标
        """
        img_width, img_height = image_size
        wm_width, wm_height = watermark_size
        
        # 如果位置是元组，直接返回
        if isinstance(position, tuple) and len(position) == 2:
            return position
        
        # 如果位置是字符串，解析预设位置
        if isinstance(position, str):
            position = position.lower()
            margin = 10  # 边距
            
            if position == 'top-left':
                return (margin, margin)
            elif position == 'top-right':
                return (img_width - wm_width - margin, margin)
            elif position == 'bottom-left':
                return (margin, img_height - wm_height - margin)
            elif position == 'bottom-right':
                return (img_width - wm_width - margin, img_height - wm_height - margin)
            elif position == 'center':
                return ((img_width - wm_width) // 2, (img_height - wm_height) // 2)
            elif position == 'top-center':
                return ((img_width - wm_width) // 2, margin)
            elif position == 'bottom-center':
                return ((img_width - wm_width) // 2, img_height - wm_height - margin)
            elif position == 'middle-left':
                return (margin, (img_height - wm_height) // 2)
            elif position == 'middle-right':
                return (img_width - wm_width - margin, (img_height - wm_height) // 2)
        
        # 默认返回左上角
        return (0, 0)