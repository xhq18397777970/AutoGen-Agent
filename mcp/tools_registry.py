"""
MCP工具注册表
统一管理和定义所有可用的工具
"""
from typing import Dict, List, Any, Callable
from agents.weather_agent.weather_tools import get_weather_sync, get_weather_function_schema
from agents.ip_agent.ip_tools import get_ip_location_sync, get_ip_function_schema


class ToolsRegistry:
    """工具注册表类"""
    
    def __init__(self):
        """初始化工具注册表"""
        self._tools = {}
        self._schemas = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """注册默认工具"""
        # 注册天气查询工具
        self.register_tool(
            name="weather",
            function=get_weather_sync,
            schema=get_weather_function_schema(),
            description="天气查询工具，可以查询指定城市的天气信息"
        )
        
        # 注册IP查询工具
        self.register_tool(
            name="ip_location",
            function=get_ip_location_sync,
            schema=get_ip_function_schema(),
            description="IP地址查询工具，可以查询IP地址的归属地信息"
        )
    
    def register_tool(self, name: str, function: Callable, schema: Dict[str, Any], description: str = ""):
        """注册工具"""
        self._tools[name] = {
            "function": function,
            "schema": schema,
            "description": description
        }
        self._schemas[name] = schema
    
    def get_tool(self, name: str) -> Dict[str, Any]:
        """获取工具"""
        return self._tools.get(name)
    
    def get_tool_function(self, name: str) -> Callable:
        """获取工具函数"""
        tool = self._tools.get(name)
        return tool["function"] if tool else None
    
    def get_tool_schema(self, name: str) -> Dict[str, Any]:
        """获取工具schema"""
        return self._schemas.get(name)
    
    def get_all_tools(self) -> Dict[str, Dict[str, Any]]:
        """获取所有工具"""
        return self._tools.copy()
    
    def get_all_schemas(self) -> Dict[str, Dict[str, Any]]:
        """获取所有工具schema"""
        return self._schemas.copy()
    
    def list_tool_names(self) -> List[str]:
        """列出所有工具名称"""
        return list(self._tools.keys())
    
    def get_tools_info(self) -> List[Dict[str, str]]:
        """获取工具信息摘要"""
        info = []
        for name, tool in self._tools.items():
            info.append({
                "name": name,
                "description": tool["description"],
                "function_name": tool["schema"]["name"]
            })
        return info


# 全局工具注册表实例
tools_registry = ToolsRegistry()