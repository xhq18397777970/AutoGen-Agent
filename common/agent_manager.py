"""
Agent管理器
统一管理和协调所有Agent
"""
from typing import Dict, List, Any
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

from agents.weather_agent.weather_agent import WeatherAgent
from agents.ip_agent.ip_agent import IPAgent
from agents.domain_agent.domain_agent import DomainAgent
from .config import config


class AgentManager:
    """Agent管理器类"""
    
    def __init__(self):
        """初始化Agent管理器"""
        self.llm_config = config.get_llm_config()
        self.agents = {}
        self.user_proxy = None
        self._initialize_agents()
    
    def _initialize_agents(self):
        """初始化所有Agent"""
        # 初始化天气Agent
        self.weather_agent = WeatherAgent(self.llm_config)
        self.agents["weather"] = self.weather_agent
        
        # 初始化IP查询Agent
        self.ip_agent = IPAgent(self.llm_config)
        self.agents["ip"] = self.ip_agent
        
        # 初始化域名查询Agent
        self.domain_agent = DomainAgent(self.llm_config)
        self.agents["domain"] = self.domain_agent
        
        # 初始化通用助手Agent
        self.general_agent = AssistantAgent(
            name="general_assistant",
            system_message="""你是一个通用助手，负责协调和回答一般性问题。你的职责是：
2. 识别用户需求并将其路由到专业助手
3. 当用户询问天气时，请转交给weather_assistant
4. 当用户询问IP地址时，请转交给ip_assistant
5. 当用户询问域名查询或域名状态时，请转交给domain_assistant
6. 协调多个专业助手的工作。""",
            llm_config=self.llm_config
        )
        self.agents["general"] = self.general_agent
        
        # 初始化路由助手Agent
        self.router_agent = AssistantAgent(
            name="router_assistant",
            system_message="""你是一个智能路由助手，负责分析用户意图并将任务分配给合适的专家。
根据问题类型选择专家：
- 天气相关：转给weather_assistant
- IP归属地：转给ip_assistant
- 域名查询、域名状态检测：转给domain_assistant

请先分析用户问题，然后决定由哪个专家处理""",
            llm_config=self.llm_config
        )
        self.agents["router"] = self.router_agent
        
        # 初始化用户代理
        self.user_proxy = UserProxyAgent(
            "user_proxy",
            code_execution_config=False,
            human_input_mode="ALWAYS"
        )
    
    def get_agent(self, agent_type: str):
        """获取指定类型的Agent"""
        if agent_type in self.agents:
            agent_obj = self.agents[agent_type]
            if hasattr(agent_obj, 'get_agent'):
                return agent_obj.get_agent()
            return agent_obj
        return None
    
    def get_all_agents(self) -> List:
        """获取所有Agent实例"""
        agent_list = [self.user_proxy]
        for agent_key in self.agents:
            agent = self.get_agent(agent_key)
            if agent:
                agent_list.append(agent)
        return agent_list
    
    def chat_with_agent(self, agent_type: str, message: str):
        """与指定Agent对话"""
        agent = self.get_agent(agent_type)
        if agent and self.user_proxy:
            self.user_proxy.initiate_chat(agent, message=message)
        else:
            print(f"Agent '{agent_type}' 不存在或用户代理未初始化")
    
    def start_group_chat(self, message: str = None):
        """启动群组聊天"""
        agents = self.get_all_agents()
        
        group_chat = GroupChat(
            agents=agents,
            messages=[],
            max_round=10
        )
        
        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=self.llm_config
        )
        
        default_message = message 
        
        self.user_proxy.initiate_chat(manager, message=default_message)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """获取所有Agent信息"""
        info = {}
        for agent_type, agent_obj in self.agents.items():
            if hasattr(agent_obj, 'get_capabilities'):
                info[agent_type] = {
                    "name": agent_obj.get_name(),
                    "capabilities": agent_obj.get_capabilities()
                }
            else:
                info[agent_type] = {
                    "name": agent_obj.name if hasattr(agent_obj, 'name') else agent_type,
                    "capabilities": ["通用对话", "任务协调"]
                }
        return info


# 全局Agent管理器实例
agent_manager = AgentManager()