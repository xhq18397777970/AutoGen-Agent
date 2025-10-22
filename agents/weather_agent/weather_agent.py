"""
天气查询Agent
专门处理天气相关的查询和对话
"""
from autogen import AssistantAgent
from .weather_tools import get_weather_sync, get_weather_function_schema


class WeatherAgent:
    """天气查询助手Agent包装类"""
    
    def __init__(self, llm_config: dict):
        """初始化天气Agent"""
        self.llm_config = llm_config.copy()
        self.llm_config["functions"] = [get_weather_function_schema()]
        
        self.agent = AssistantAgent(
            name="weather_assistant",
            system_message="""你是一个专业的天气查询助手。你的职责是：
1. 当用户询问天气时，使用get_weather函数查询指定城市的天气
2. 如果用户询问多个城市，请逐个查询并汇总结果
3. 用友好、专业的中文回复天气信息
4. 可以提供穿衣建议、出行建议等额外信息
5. 如果城市名称不明确，请询问用户具体的城市名称
6. 专注于天气相关的问题，其他问题请转交给相关专家""",
            llm_config=self.llm_config,
            function_map={
                "get_weather": get_weather_sync
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
            "天气查询",
            "多城市天气对比",
            "天气建议",
            "出行建议"
        ]