"""
天气查询工具模块
提供天气相关的API调用功能
"""
import httpx
import asyncio
from typing import Dict, Any


async def get_weather(city: str) -> str:
    """查询指定城市的天气信息"""
    api_key = "becab1d22273f6792a96265302e1057b"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_cn"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(base_url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return f"""
城市: {data.get('name', city)}
天气: {data['weather'][0]['description']}
温度: {data['main']['temp']}°C
湿度: {data['main']['humidity']}%
风速: {data['wind']['speed']} m/s
"""
            else:
                return f"获取天气信息失败: {resp.status_code}"
    except Exception as e:
        return f"天气查询错误: {str(e)}"


def get_weather_sync(city: str) -> str:
    """同步版本的天气查询函数"""
    return asyncio.run(get_weather(city))


def get_weather_function_schema() -> Dict[str, Any]:
    """获取天气查询函数的schema定义"""
    return {
        "name": "get_weather",
        "description": "查询指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如 Beijing, Shanghai, New York"
                }
            },
            "required": ["city"]
        }
    }