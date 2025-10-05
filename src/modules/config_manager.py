#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块
负责管理应用配置和水印模板
"""

import json
import os
from pathlib import Path

class ConfigManager:
    """
    配置管理器类
    """
    
    def __init__(self):
        """
        初始化配置管理器
        """
        self.config_dir = Path.home() / ".photot_watermark"
        self.config_file = self.config_dir / "config.json"
        self.templates_dir = self.config_dir / "templates"
        self.config = self._get_default_config()
        self.templates = {}
        
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
        # 加载配置
        self.load_config()
        self.load_all_templates()
    
    def _get_default_config(self):
        """
        获取默认配置
        """
        return {
            "app": {
                "window_geometry": {
                    "width": 1200,
                    "height": 700,
                    "x": 100,
                    "y": 100
                },
                "last_export_dir": "",
                "last_import_dir": "",
                "auto_save_template": True,
                "auto_load_last_template": True,
                "last_template": ""
            },
            "watermark": {
                "text": {
                    "content": "水印文本",
                    "font_size": 24,
                    "color": [255, 255, 255, 128],
                    "opacity": 50,
                    "rotation": 0
                },
                "image": {
                    "scale": 1.0,
                    "opacity": 50,
                    "rotation": 0
                },
                "position": "top-left",
                "last_template": ""
            },
            "export": {
                "format": "JPEG",
                "quality": 95,
                "naming_rule": "original",
                "prefix": "wm_",
                "suffix": "_watermarked",
                "resize_enabled": False,
                "max_width": 1920,
                "max_height": 1080,
                "last_export_dir": ""
            }
        }
    
    def load_config(self):
        """
        加载配置
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 深度合并配置
                    self._deep_merge(self.config, loaded_config)
                print(f"配置已从 {self.config_file} 加载")
            else:
                print("使用默认配置")
        except Exception as e:
            print(f"加载配置失败: {e}")
            # 使用默认配置
    
    def save_config(self):
        """
        保存配置
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"配置已保存到 {self.config_file}")
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def _deep_merge(self, target, source):
        """
        深度合并字典
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def get_setting(self, key_path, default=None):
        """
        获取配置项
        
        Args:
            key_path: 配置项路径，如 "app.window_geometry.width"
            default: 默认值
        
        Returns:
            配置项值
        """
        keys = key_path.split('.')
        current = self.config
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    def set_setting(self, key_path, value):
        """
        设置配置项
        
        Args:
            key_path: 配置项路径，如 "app.window_geometry.width"
            value: 配置项值
        """
        keys = key_path.split('.')
        current = self.config
        
        # 遍历到最后一个键的父级
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        # 设置值
        current[keys[-1]] = value
    
    def save_template(self, template_name, template_data):
        """
        保存水印模板
        
        Args:
            template_name: 模板名称
            template_data: 模板数据
        """
        try:
            template_file = self.templates_dir / f"{template_name}.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            
            self.templates[template_name] = template_data
            print(f"模板 '{template_name}' 已保存")
        except Exception as e:
            print(f"保存模板失败: {e}")
            raise Exception(f"保存模板失败: {str(e)}")
    
    def load_template(self, template_name):
        """
        加载水印模板
        
        Args:
            template_name: 模板名称
        
        Returns:
            模板数据
        """
        try:
            template_file = self.templates_dir / f"{template_name}.json"
            if template_file.exists():
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                print(f"模板 '{template_name}' 已加载")
                return template_data
            else:
                raise Exception(f"模板 '{template_name}' 不存在")
        except Exception as e:
            print(f"加载模板失败: {e}")
            raise Exception(f"加载模板失败: {str(e)}")
    
    def load_all_templates(self):
        """
        加载所有模板
        """
        try:
            self.templates = {}
            for template_file in self.templates_dir.glob("*.json"):
                template_name = template_file.stem
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        self.templates[template_name] = json.load(f)
                except Exception as e:
                    print(f"加载模板 '{template_name}' 失败: {e}")
            
            print(f"已加载 {len(self.templates)} 个模板")
        except Exception as e:
            print(f"加载所有模板失败: {e}")
    
    def delete_template(self, template_name):
        """
        删除水印模板
        
        Args:
            template_name: 模板名称
        """
        try:
            template_file = self.templates_dir / f"{template_name}.json"
            if template_file.exists():
                template_file.unlink()
                if template_name in self.templates:
                    del self.templates[template_name]
                print(f"模板 '{template_name}' 已删除")
            else:
                raise Exception(f"模板 '{template_name}' 不存在")
        except Exception as e:
            print(f"删除模板失败: {e}")
            raise Exception(f"删除模板失败: {str(e)}")
    
    def get_template_names(self):
        """
        获取所有模板名称
        
        Returns:
            模板名称列表
        """
        return list(self.templates.keys())
    
    def get_last_template_name(self):
        """
        获取上一次使用的模板名称
        
        Returns:
            模板名称，如果没有则返回None
        """
        return self.get_setting("app.last_template", "")
    
    def set_last_template_name(self, template_name):
        """
        设置上一次使用的模板名称
        
        Args:
            template_name: 模板名称
        """
        self.set_setting("app.last_template", template_name)
        self.save_config()
    
    def should_auto_load_last_template(self):
        """
        检查是否应该自动加载上一次模板
        
        Returns:
            bool: 是否应该自动加载
        """
        return self.get_setting("app.auto_load_last_template", True)
    
    def get_default_template_name(self):
        """
        获取默认模板名称
        
        Returns:
            默认模板名称，如果没有则返回None
        """
        # 如果有模板，返回第一个模板名称
        template_names = self.get_template_names()
        if template_names:
            return template_names[0]
        return None
    
    def create_watermark_template(self, text_settings, image_settings, position_settings):
        """
        创建水印模板数据
        
        Args:
            text_settings: 文本水印设置
            image_settings: 图片水印设置
            position_settings: 位置设置
        
        Returns:
            模板数据字典
        """
        return {
            "text": text_settings,
            "image": image_settings,
            "position": position_settings,
            "timestamp": self._get_current_timestamp()
        }
    
    def _get_current_timestamp(self):
        """
        获取当前时间戳
        
        Returns:
            时间戳字符串
        """
        from datetime import datetime
        return datetime.now().isoformat()