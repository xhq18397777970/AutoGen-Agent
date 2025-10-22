import os
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
import httpx
import asyncio
from datetime import datetime

load_dotenv()

# ==================== 天气查询函数 ====================
async def get_weather(city: str) -> str:
    """查询指定城市的天气信息"""
    api_key = "becab1d22273f6792a96265302e1057b"  # 请替换为实际的API密钥
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
    return asyncio.run(get_weather(city))

# ==================== IP查询函数 ====================
async def get_ip_location(ip: str) -> str:
    """查询IP地址的归属地信息"""
    try:
        async with httpx.AsyncClient() as client:
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
"""
                return location_info
            else:
                return f"IP查询失败，状态码: {response.status_code}"
    except Exception as e:
        return f"IP查询错误: {str(e)}"

def get_ip_location_sync(ip: str) -> str:
    return asyncio.run(get_ip_location(ip))

# ==================== 日期查询函数 ====================
def get_current_date() -> str:
    """获取当前日期"""
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %A")

# ==================== 配置LLM ====================
llm_config = {
    "config_list": [
        {
            "model": "deepseek-chat",
            "api_key": "sk-faac378b82464d5cb37f0203686f48da",  # 请替换为实际的API密钥
            "base_url": "https://api.deepseek.com",
            "api_type": "openai",
        }
    ],
    "temperature": 0.1
}

# ==================== 优化后的Agent定义 ====================

# 1. 任务协调员Agent - 专门负责任务分解和协调
coordinator_assistant = AssistantAgent(
    name="coordinator_assistant",
    system_message="""# 角色
你是一个专业的任务拆解专家，专门分析用户意图并将其分解为可执行的具体任务。

# 核心能力
1. **意图识别**：准确理解用户的真实需求和目标
2. 任务分解：将复杂任务拆解为清晰的子任务序列
3. 依赖分析：识别子任务之间的依赖关系和执行顺序
4. Agent匹配：为每个子任务推荐最适合执行的Agent类型


""",
    llm_config=llm_config
)

# 2. 天气助手Agent - 只处理天气相关查询
weather_llm_config = llm_config.copy()
weather_llm_config["functions"] = [
    {
        "name": "get_weather",
        "description": "查询指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如 Beijing, New York"
                }
            },
            "required": ["city"]
        }
    }
]

weather_assistant = AssistantAgent(
    name="weather_assistant",
    system_message="""# 角色
你是一个专业的天气信息查询助手，专门通过MCP工具获取和提供准确的实时天气信息。

# 核心能力
1. **实时天气查询**：使用内置的 `get_weather_sync` 函数获取指定城市的实时天气数据
2. **数据解析展示**：将原始天气数据转换为用户友好的格式
3. **多城市支持**：可以同时查询多个城市的天气情况
4. **错误处理**：妥善处理查询失败的情况并提供友好的错误信息""",
    llm_config=weather_llm_config,
    function_map={"get_weather": get_weather_sync}
)

# 3. IP查询助手Agent - 只处理IP相关查询
ip_llm_config = llm_config.copy()
ip_llm_config["functions"] = [
    {
        "name": "get_ip_location",
        "description": "查询IP地址的归属地信息",
        "parameters": {
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string",
                    "description": "IP地址，如 8.8.8.8"
                }
            },
            "required": ["ip"]
        }
    }
]

ip_assistant = AssistantAgent(
    name="ip_assistant",
    system_message="""你是一个专业的IP地址查询助手。你的职责是：
1. 当且仅当收到IP地址查询请求时，使用get_ip_location函数查询
2. 只提供IP地址相关的准确信息，不回答其他问题
3. 如果收到非IP查询问题，回复："这是IP查询助手，我只处理IP地址查询，请将其他问题转给相应专家。"
4. 保持回答简洁专业

请严格遵守职责范围，只处理IP地址查询。""",
    llm_config=ip_llm_config,
    function_map={"get_ip_location": get_ip_location_sync}
)

# 4. 日期助手Agent - 只处理日期查询
date_llm_config = llm_config.copy()
date_llm_config["functions"] = [
    {
        "name": "get_current_date",
        "description": "获取当前日期信息",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

date_assistant = AssistantAgent(
    name="date_assistant",
    system_message="""你是一个日期查询助手。你的职责是：
1. 当且仅当收到日期查询请求时，使用get_current_date函数查询当前日期
2. 只回答日期相关问题，不回答其他问题
3. 如果收到非日期问题，回复："这是日期助手，我只处理日期查询，请将其他问题转给相应专家。"
4. 保持回答简洁""",
    llm_config=date_llm_config,
    function_map={
        "get_current_date": get_current_date
    }
)

# 5. 汇总助手Agent - 负责最终结果汇总
summary_assistant = AssistantAgent(
    name="summary_assistant",
    system_message="""你是汇总助手，负责收集所有专业助手的回答并整理成完整回复。你的职责是：
1. 等待所有专业助手完成各自任务
2. 收集他们的专业回答
3. 整理成结构化的完整回复给用户
4. 不修改专业助手提供的具体内容
5. 确保回复完整、清晰、有条理

请按以下格式汇总：
【问题汇总】
1. 原始问题1 → 专业回答
2. 原始问题2 → 专业回答

所有问题都已得到专业解答。""",
    llm_config=llm_config
)

# ==================== 用户代理 ====================
user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config=False,
    human_input_mode="NEVER"
)

# ==================== 优化的群组聊天 ====================
def start_optimized_group_chat():
    """启动优化后的多Agent协同聊天"""
    
    # 创建群组聊天，明确指定发言顺序
    group_chat = GroupChat(
        agents=[user_proxy, coordinator_assistant, weather_assistant, ip_assistant, date_assistant, summary_assistant],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin"  # 使用轮询方式控制发言顺序
    )
    
    # 创建群组聊天管理器
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config
    )
    
    # 启动群组聊天
    user_proxy.initiate_chat(
        manager,
        message="""你好！我有几个问题需要帮助：
        1. 我想知道北京和纽约的天气情况
        2. 我还想查询一下IP地址 8.8.8.8 的信息  
        3. 另外，能告诉我今天日期吗？
        请帮我处理这些问题。"""
    )

# ==================== 改进的智能路由 ====================
def start_smart_routing_chat():
    """启动智能路由对话，由协调员控制流程"""
    
    # 创建专门的路由群组
    routing_agents = [user_proxy, coordinator_assistant, weather_assistant, ip_assistant, date_assistant]
    
    routing_chat = GroupChat(
        agents=routing_agents,
        messages=[],
        max_round=8
    )
    
    routing_manager = GroupChatManager(
        groupchat=routing_chat,
        llm_config=llm_config
    )
    
    user_proxy.initiate_chat(
        routing_manager,
        message="请帮我查询北京天气、8.8.8.8的IP信息和当前日期"
    )



# ==================== 主程序 ====================
if __name__ == "__main__":
    print("=== 优化版多Agent系统启动 ===")
    print("1. 优化多Agent协同聊天")
    print("2. 智能路由对话") 
    print("3. 单独天气查询")
    print("4. 单独IP查询")
    
    choice = input("请选择对话模式 (1-4): ").strip()
    
    if choice == "1":
        print("\n=== 启动优化多Agent协同聊天 ===")
        start_optimized_group_chat()
    elif choice == "2":
        print("\n=== 启动智能路由对话 ===")
        start_smart_routing_chat()
    elif choice == "3":
        print("\n=== 启动天气查询 ===")
        user_proxy.initiate_chat(weather_assistant, message="查询北京天气")
    elif choice == "4":
        print("\n=== 启动IP查询 ===")
        user_proxy.initiate_chat(ip_assistant, message="查询8.8.8.8的信息")
    else:
        print("使用默认的优化多Agent协同")
        start_optimized_group_chat()