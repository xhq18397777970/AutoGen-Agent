"""
IP地址查询Agent
专门处理IP地址归属地查询和相关对话
"""
from autogen import AssistantAgent
from .ip_tools import get_ip_location_sync, get_ip_function_schema


class IPAgent:
    """IP地址查询助手Agent包装类"""
    
    def __init__(self, llm_config: dict):
        """初始化IP Agent"""
        self.llm_config = llm_config.copy()
        self.llm_config["functions"] = [get_ip_function_schema()]
        
        self.agent = AssistantAgent(
            name="ip_assistant",
            system_message="""你是一个专业的IP地址查询助手。你的职责是：
1. 当用户询问IP地址归属地时，使用get_ip_location函数查询
2. 提供详细的IP地理位置信息
3. 用专业、准确的中文回复查询结果
4. 可以解释IP地址的基本信息和地理位置含义
5. 如果IP地址格式不正确，请提醒用户输入正确的IP格式
6. 专注于IP相关的问题，其他问题请转交给相关专家""",
            llm_config=self.llm_config,
            function_map={
                "get_ip_location": get_ip_location_sync
            }
        )
    
    def get_agent(self) -> AssistantAgent:
        """获取AutoGen Agent实例"""
        return self.agent
    
    def get_name(self) -> str:
        """获取Agent名称"""
        return self.agent.name
    
    def get_capabilities(self) -> list:
        """获取Agent能力描述"""
        return [
            "IP地址归属地查询",
            "IP地理位置分析",
            "网络运营商识别",
            "IP地址格式验证"
        ]