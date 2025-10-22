"""
配置管理模块
统一管理所有Agent的配置信息
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

# 加载环境变量
load_dotenv()


class Config:
    """配置管理类"""
    
    def __init__(self):
        """初始化配置"""
        self.llm_config = self._get_llm_config()
        self.weather_api_key = self._get_weather_api_key()
    
    def _get_llm_config(self) -> Dict[str, Any]:
        """获取LLM配置"""
        return {
            "config_list": [
                {
                    "model": os.getenv("LLM_MODEL", "deepseek-chat"),
                    "api_key": os.getenv("LLM_API_KEY", "sk-bbb938ce229d471b964eafee206668f3"),
                    "base_url": os.getenv("LLM_BASE_URL", "https://api.deepseek.com"),
                    "api_type": "openai",
                }
            ]
        }
    
    def _get_weather_api_key(self) -> str:
        """获取天气API密钥"""
        return os.getenv("WEATHER_API_KEY", "becab1d22273f6792a96265302e1057b")
    
    def get_llm_config(self) -> Dict[str, Any]:
        """获取LLM配置"""
        return self.llm_config.copy()
    
    def get_weather_api_key(self) -> str:
        """获取天气API密钥"""
        return self.weather_api_key


# 全局配置实例
config = Config()