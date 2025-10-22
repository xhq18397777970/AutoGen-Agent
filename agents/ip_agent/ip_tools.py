"""
IP地址查询工具模块
提供IP地址归属地查询功能
"""
import httpx
import asyncio
from typing import Dict, Any


async def get_ip_location(ip: str) -> str:
    """查询IP地址的归属地信息"""
    try:
        async with httpx.AsyncClient() as client:
            # 使用ipapi.co免费API
            response = await client.get(f"http://ipapi.co/{ip}/json/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    return f"IP查询失败: {data.get('reason', '未知错误')}"
                
                location_info = f"""
IP地址: {ip}
国家: {data.get('country_name', '未知')}
地区: {data.get('region', '未知')}
城市: {data.get('city', '未知')}
运营商: {data.get('org', '未知')}
时区: {data.get('timezone', '未知')}
经纬度: {data.get('latitude', '未知')}, {data.get('longitude', '未知')}
"""
                return location_info
            else:
                return f"IP查询失败，状态码: {response.status_code}"
    except Exception as e:
        return f"IP查询错误: {str(e)}"


def get_ip_location_sync(ip: str) -> str:
    """同步版本的IP查询函数"""
    return asyncio.run(get_ip_location(ip))


def get_ip_function_schema() -> Dict[str, Any]:
    """获取IP查询函数的schema定义"""
    return {
        "name": "get_ip_location",
        "description": "查询IP地址的归属地信息",
        "parameters": {
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string",
                    "description": "IP地址，如 8.8.8.8, 114.114.114.114"
                }
            },
            "required": ["ip"]
        }
    }