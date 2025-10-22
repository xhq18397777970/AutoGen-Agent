"""
多Agent系统主程序
重构后的模块化入口程序
"""
from common.agent_manager import agent_manager
from mcp.tools_registry import tools_registry


def display_menu():
    """显示菜单选项"""
    print("\n" + "="*50)
    print("🤖 多Agent智能助手系统")
    print("="*50)
    print("1. 天气查询助手")
    print("2. IP地址查询助手") 
    print("3. 多Agent协同聊天")
    print("4. 智能路由对话")
    print("5. 显示Agent信息")
    print("6. 显示可用工具")
    print("0. 退出系统")
    print("="*50)


def display_agent_info():
    """显示Agent信息"""
    print("\n📋 Agent信息:")
    print("-" * 40)
    agent_info = agent_manager.get_agent_info()
    for agent_type, info in agent_info.items():
        print(f"🔸 {info['name']} ({agent_type})")
        for capability in info['capabilities']:
            print(f"   • {capability}")
        print()


def display_tools_info():
    """显示工具信息"""
    print("\n🛠️ 可用工具:")
    print("-" * 40)
    tools_info = tools_registry.get_tools_info()
    for tool in tools_info:
        print(f"🔧 {tool['name']}")
        print(f"   描述: {tool['description']}")
        print(f"   函数: {tool['function_name']}")
        print()


def chat_with_weather_assistant():
    """与天气助手对话"""
    print("\n🌤️ 启动天气查询助手")
    print("输入'quit'退出对话")
    user_input = input("请输入您的天气查询问题: ").strip()
    if user_input.lower() != 'quit':
        agent_manager.chat_with_agent("weather", user_input)


def chat_with_ip_assistant():
    """与IP助手对话"""
    print("\n🌐 启动IP查询助手")
    print("输入'quit'退出对话")
    user_input = input("请输入您的IP查询问题: ").strip()
    if user_input.lower() != 'quit':
        agent_manager.chat_with_agent("ip", user_input)


def start_group_chat():
    """启动多Agent协同聊天"""
    print("\n👥 启动多Agent协同聊天")
    print("输入'quit'退出对话")
    agent_manager.start_group_chat()


def chat_with_router():
    """通过路由助手进行智能对话"""
    print("\n🧠 启动智能路由对话")
    print("输入'quit'退出对话")
    user_input = input("请输入您的问题: ").strip()
    if user_input.lower() != 'quit':
        agent_manager.chat_with_agent("router", user_input)


def main():
    """主程序"""
    print("🚀 系统初始化完成!")
    
    while True:
        try:
            display_menu()
            choice = input("\n请选择功能 (0-6): ").strip()
            
            if choice == "0":
                print("\n👋 感谢使用多Agent智能助手系统，再见!")
                break
            elif choice == "1":
                chat_with_weather_assistant()
            elif choice == "2":
                chat_with_ip_assistant()
            elif choice == "3":
                start_group_chat()
            elif choice == "4":
                chat_with_router()
            elif choice == "5":
                display_agent_info()
            elif choice == "6":
                display_tools_info()
            else:
                print("❌ 无效选择，请输入0-6之间的数字")
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，系统退出")
            break
        except Exception as e:
            print(f"\n❌ 系统错误: {str(e)}")
            print("请重试或联系管理员")


if __name__ == "__main__":
    main()