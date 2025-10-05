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
            # 保持原图模式，只在需要时转换为RGBA
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
                if image.mode == 'RGBA':
                    # 创建白色背景
                    rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                    # 将RGBA图像粘贴到RGB背景上
                    rgb_image.paste(image, mask=image.split()[-1])
                    image = rgb_image
                elif image.mode != 'RGB':
                    image = image.convert("RGB")
                
                # 保存JPEG，使用最高质量
                image.save(file_path, format=file_format, quality=quality, optimize=True, subsampling=0)
            else:
                # 对于PNG等格式，保持原模式，使用无损压缩
                image.save(file_path, format=file_format, optimize=True)
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
                - rotation: 旋转角度
                - custom_position: 自定义位置 (x, y) 元组
        
        Returns:
            添加水印后的图像
        """
        try:
            print(f"开始添加文本水印: {text}")
            print(f"位置参数: {position}")
            print(f"其他参数: {kwargs}")
            
            # 获取参数
            font_path = kwargs.get('font_path', None)
            base_font_size = kwargs.get('font_size', 48)  # 基础字体大小
            color = kwargs.get('color', (255, 255, 255, 200))  # 默认改为白色半透明，提高可见性
            opacity = kwargs.get('opacity', 80)  # 默认透明度改为80，确保在各种背景上都可见
            rotation = kwargs.get('rotation', 0)
            
            # 根据图片尺寸自适应调整字体大小
            img_width, img_height = image.size
            # 以图片宽度的1/20作为参考字体大小
            adaptive_font_size = max(base_font_size, int(min(img_width, img_height) / 20))
            # 确保字体大小在合理范围内
            font_size = min(adaptive_font_size, 200)  # 最大200像素
            print(f"自适应字体大小: {font_size} (基础: {base_font_size}, 图片尺寸: {img_width}x{img_height})")
            
            print(f"处理前颜色: {color}, 透明度: {opacity}")
            
            # 直接使用用户选择的颜色值，仅调整透明度
            # 透明度逻辑：opacity值越大越透明（即不透明度越小）
            if len(color) == 3:
                r, g, b = color
                # 透明度逻辑：opacity值越大越透明，所以alpha值应该越小
                a = int(255 * (100 - opacity) / 100)  # 100-opacity转换为不透明度
                color = (r, g, b, a)  # 保持RGB顺序
            elif len(color) == 4:
                r, g, b, original_a = color
                # 透明度逻辑：opacity值越大越透明，所以alpha值应该越小
                a = int(original_a * (100 - opacity) / 100)
                color = (r, g, b, a)  # 保持RGBA顺序
            
            print(f"处理后颜色: {color}")
            
            # 加载字体，确保使用指定的字体大小，并支持中文字体
            try:
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    print(f"使用字体文件: {font_path}, 字体大小: {font_size}")
                else:
                    # 尝试使用支持中文的系统字体
                    chinese_fonts = [
                        "msyh.ttc",      # 微软雅黑
                        "simhei.ttf",    # 黑体
                        "simsun.ttc",    # 宋体
                        "simkai.ttf",    # 楷体
                        "arial.ttf",     # Arial
                        "arialuni.ttf"   # Arial Unicode
                    ]
                    
                    font = None
                    for font_name in chinese_fonts:
                        try:
                            font = ImageFont.truetype(font_name, font_size)
                            print(f"使用中文字体: {font_name}, 字体大小: {font_size}")
                            break
                        except:
                            continue
                    
                    # 如果没有找到合适的中文字体，使用默认字体
                    if font is None:
                        font = ImageFont.load_default()
                        print(f"未找到合适的字体，使用默认字体，字体大小: {font_size}")
            except Exception as e:
                # 备用方案：使用默认字体
                font = ImageFont.load_default()
                print(f"加载字体失败，使用默认字体: {e}")
            
            # 计算文本大小 - 使用更大的测试图像
            dummy_image = Image.new("RGBA", (2000, 500), (0, 0, 0, 0))
            dummy_draw = ImageDraw.Draw(dummy_image)
            
            try:
                # 新版本PIL
                bbox = dummy_draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                print(f"新版本PIL计算文本大小: {text_width} x {text_height}")
            except:
                # 兼容旧版本PIL
                text_width, text_height = dummy_draw.textsize(text, font=font)
                print(f"旧版本PIL计算文本大小: {text_width} x {text_height}")
            
            # 如果计算出来的文本大小明显小于字体大小，说明字体可能没有正确应用
            # 这种情况下我们使用字体大小来估算文本尺寸
            if text_width < font_size or text_height < font_size // 2:
                # 使用字体大小估算文本尺寸
                text_width = len(text) * font_size * 0.7  # 估算宽度
                text_height = font_size  # 高度等于字体大小
                print(f"重新估算文本大小: {text_width} x {text_height}")
            
            # 确保文本大小不为0
            if text_width == 0 or text_height == 0:
                # 使用字体大小估算文本尺寸
                text_width = len(text) * font_size * 0.7
                text_height = font_size
                print(f"文本大小为0，使用估算大小: {text_width} x {text_height}")
            
            # 创建水印图像 - 增加额外的边距
            margin = max(30, int(text_width // 4), int(text_height // 4))  # 动态边距
            watermark_width = int(text_width + margin * 2)
            watermark_height = int(text_height + margin * 2)
            watermark_image = Image.new("RGBA", (watermark_width, watermark_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark_image)
            
            print(f"创建水印图像大小: {watermark_width} x {watermark_height}")
            
            draw_x = (watermark_width - text_width) // 2
            draw_y = (watermark_height - text_height) // 2
            print(f"文本绘制位置: ({draw_x}, {draw_y})")
            
            # # 添加描边效果以增强可见性
            # # 先绘制描边（黑色）
            # outline_color = (0, 0, 0, 180)  # 黑色半透明
            # for dx in [-2, -1, 0, 1, 2]:
            #     for dy in [-2, -1, 0, 1, 2]:
            #         if dx != 0 or dy != 0:  # 不在中心位置
            #             draw.text((draw_x + dx, draw_y + dy), text, font=font, fill=outline_color)
            
            # 再绘制主文本
            draw.text((draw_x, draw_y), text, font=font, fill=color)
            
            # 旋转水印
            if rotation != 0:
                print(f"旋转水印: {rotation}度")
                watermark_image = watermark_image.rotate(rotation, expand=1, fillcolor=(0, 0, 0, 0))
            
            # 解析位置
            custom_position = kwargs.get('custom_position', None)
            x, y = self._parse_position(position, image.size, watermark_image.size, custom_position)
            print(f"水印最终位置: ({x}, {y})")
            print(f"背景图像大小: {image.size}")
            print(f"水印图像大小: {watermark_image.size}")
            
            # 创建结果图像
            result = image.copy()
            
            # 如果原图不是RGBA模式，需要转换为RGBA以支持透明度
            if result.mode != "RGBA":
                result = result.convert("RGBA")
            
            # 粘贴水印
            result.paste(watermark_image, (x, y), watermark_image)
            print("文本水印添加完成")
            
            # 如果原图不是RGBA模式，转换回原图模式以保持质量
            if image.mode != "RGBA" and result.mode == "RGBA":
                if image.mode == "RGB":
                    result = result.convert("RGB")
                elif image.mode == "L":
                    result = result.convert("L")
                # 其他模式保持RGBA
                
            return result
        except Exception as e:
            print(f"添加文本水印失败: {str(e)}")
            import traceback
            traceback.print_exc()
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
                - rotation: 旋转角度
                - custom_position: 自定义位置 (x, y) 元组
        
        Returns:
            添加水印后的图像
        """
        try:
            print("开始添加图片水印")
            print(f"位置参数: {position}")
            print(f"其他参数: {kwargs}")
            
            # 获取参数
            scale = kwargs.get('scale', 1.0)
            opacity = kwargs.get('opacity', 100)
            rotation = kwargs.get('rotation', 0)
            
            # 调整水印图片大小
            if scale != 1.0:
                new_width = int(watermark_image.width * scale)
                new_height = int(watermark_image.height * scale)
                watermark_image = watermark_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"调整水印图片大小: {new_width} x {new_height}")
            
            # 处理透明度
            # 透明度逻辑：opacity值越大越透明（即不透明度越小）
            if opacity < 100:
                if watermark_image.mode == "RGBA":
                    # 分离alpha通道并调整透明度
                    r, g, b, alpha = watermark_image.split()
                    # 透明度逻辑：opacity值越大越透明，所以alpha值应该越小
                    alpha = alpha.point(lambda x: int(x * (100 - opacity) / 100))
                    watermark_image = Image.merge('RGBA', (r, g, b, alpha))
                else:
                    # 对于非RGBA图像，先转换为RGBA
                    watermark_image = watermark_image.convert("RGBA")
                    r, g, b, alpha = watermark_image.split()
                    # 透明度逻辑：opacity值越大越透明，所以alpha值应该越小
                    alpha = alpha.point(lambda x: int(x * (100 - opacity) / 100))
                    watermark_image = Image.merge('RGBA', (r, g, b, alpha))
                print(f"调整水印透明度: {opacity}% (值越大越透明)")
            
            # 确保水印图片是RGBA模式
            if watermark_image.mode != "RGBA":
                watermark_image = watermark_image.convert("RGBA")
            
            # 旋转水印
            if rotation != 0:
                watermark_image = watermark_image.rotate(rotation, expand=1)
                print(f"旋转水印: {rotation}度")
            
            # 解析位置
            custom_position = kwargs.get('custom_position', None)
            x, y = self._parse_position(position, image.size, watermark_image.size, custom_position)
            print(f"水印最终位置: ({x}, {y})")
            print(f"背景图像大小: {image.size}")
            print(f"水印图像大小: {watermark_image.size}")
            
            # 创建结果图像
            result = image.copy()
            
            # 如果原图不是RGBA模式，需要转换为RGBA以支持透明度
            if result.mode != "RGBA":
                result = result.convert("RGBA")
            
            # 粘贴水印图片
            result.paste(watermark_image, (x, y), watermark_image)
            print("图片水印添加完成")
            
            # 如果原图不是RGBA模式，转换回原图模式以保持质量
            if image.mode != "RGBA" and result.mode == "RGBA":
                if image.mode == "RGB":
                    result = result.convert("RGB")
                elif image.mode == "L":
                    result = result.convert("L")
                # 其他模式保持RGBA
                
            return result
        except Exception as e:
            print(f"添加图片水印失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"添加图片水印失败: {str(e)}")
    
    def _parse_position(self, position, image_size, watermark_size, custom_position=None):
        """
        解析水印位置
        
        Args:
            position: 位置参数，可以是(x, y)元组或预设位置字符串
            image_size: 背景图片尺寸 (width, height)
            watermark_size: 水印尺寸 (width, height)
            custom_position: 自定义位置 (x, y) 元组
        
        Returns:
            (x, y) 位置坐标
        """
        img_width, img_height = image_size
        wm_width, wm_height = watermark_size
        
        print(f"解析位置: {position}")
        print(f"背景尺寸: {image_size}, 水印尺寸: {watermark_size}")
        
        # 如果提供了自定义位置，优先使用
        if custom_position is not None and isinstance(custom_position, tuple) and len(custom_position) == 2:
            print(f"使用自定义位置: {custom_position}")
            return custom_position
        
        # 如果位置是元组，直接返回
        if isinstance(position, tuple) and len(position) == 2:
            print(f"使用自定义位置: {position}")
            return position
        
        # 如果位置是字符串，解析预设位置
        if isinstance(position, str):
            position = position.lower()
            margin = 20  # 增大边距
            
            if position == 'top-left':
                result = (margin, margin)
            elif position == 'top-right':
                result = (img_width - wm_width - margin, margin)
            elif position == 'bottom-left':
                result = (margin, img_height - wm_height - margin)
            elif position == 'bottom-right':
                result = (img_width - wm_width - margin, img_height - wm_height - margin)
            elif position == 'center':
                result = ((img_width - wm_width) // 2, (img_height - wm_height) // 2)
            elif position == 'top-center':
                result = ((img_width - wm_width) // 2, margin)
            elif position == 'bottom-center':
                result = ((img_width - wm_width) // 2, img_height - wm_height - margin)
            elif position == 'middle-left':
                result = (margin, (img_height - wm_height) // 2)
            elif position == 'middle-right':
                result = (img_width - wm_width - margin, (img_height - wm_height) // 2)
            else:
                result = (20, 20)  # 默认位置改为(20, 20)
            
            print(f"解析后位置: {result}")
            return result
        
        # 默认返回左上角附近
        print("使用默认位置: (20, 20)")
        return (20, 20)