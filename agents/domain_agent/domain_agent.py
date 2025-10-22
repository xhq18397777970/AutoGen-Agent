"""
域名查询Agent
专门处理域名基础信息查询和状态检测相关对话
"""
from autogen import AssistantAgent
from .domain_tools import (
    batch_get_domains_info_sync, 
    batch_check_domains_status_sync,
    get_batch_domains_info_schema,
    get_batch_domains_status_schema
)


class DomainAgent:
    """域名查询助手Agent包装类"""
    
    def __init__(self, llm_config: dict):
        """初始化Domain Agent"""
        self.llm_config = llm_config.copy()
        self.llm_config["functions"] = [
            get_batch_domains_info_schema(),
            get_batch_domains_status_schema()
        ]
        
        self.agent = AssistantAgent(
            name="domain_assistant",
            system_message="""你是一个专业的域名查询助手。你的职责是：
1. 当用户需要查询域名基础信息时，使用batch_get_domains_info函数批量查询
2. 当用户需要检测域名状态时，使用batch_check_domains_status函数批量检测
3. 提供详细的域名信息，包括状态、服务类型、负责人、项目等
4. 用专业、准确的中文回复查询结果
5. 支持批量处理，可以同时处理多个域名
6. 如果域名格式不正确，请提醒用户输入正确的域名格式
7. 专注于域名相关的问题，其他问题请转交给相关专家

支持的功能：
- 批量查询域名基础信息（状态、负责人、项目、组织等）
- 批量检测域名可用性状态（是否可申请）
- 域名格式验证和建议
- 域名管理相关咨询""",
            llm_config=self.llm_config,
            function_map={
                "batch_get_domains_info": batch_get_domains_info_sync,
                "batch_check_domains_status": batch_check_domains_status_sync
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
            "批量域名基础信息查询",
            "批量域名状态检测",
            "域名可用性分析",
            "域名管理信息查询",
            "域名格式验证",
            "域名负责人和项目信息查询"
        ]