# 多Agent智能助手系统

## 项目概述

这是一个基于AutoGen框架的模块化多Agent系统，采用清晰的文件夹结构组织不同功能的Agent。每个Agent专注于特定领域的任务，同时支持MCP工具集成。

## 项目结构

```
├── agents/                    # Agent模块目录
│   ├── weather_agent/         # 天气查询Agent
│   │   ├── __init__.py
│   │   ├── weather_tools.py   # 天气查询工具
│   │   └── weather_agent.py   # 天气Agent类
│   └── ip_agent/              # IP查询Agent
│       ├── __init__.py
│       ├── ip_tools.py        # IP查询工具
│       └── ip_agent.py        # IP Agent类
├── common/                    # 通用模块
│   ├── __init__.py
│   ├── config.py              # 配置管理
│   └── agent_manager.py       # Agent管理器
├── mcp/                       # MCP工具定义
│   ├── __init__.py
│   └── tools_registry.py      # 工具注册表
├── main.py                    # 主程序入口
├── test.py                    # 原始测试文件
├── .env.example               # 环境变量示例
└── requirements.txt           # 依赖包列表
```

## 功能特性

### 🤖 多Agent协作
- **天气查询Agent**: 专门处理天气相关查询
- **IP地址查询Agent**: 专门处理IP归属地查询
- **通用助手Agent**: 处理一般性问题和任务协调
- **智能路由Agent**: 分析用户意图并分配给合适的专家

### 🛠️ 模块化设计
- 每个Agent独立封装在自己的文件夹中
- 统一的工具注册表管理所有可用工具
- 配置集中管理，支持环境变量
- Agent管理器统一协调所有Agent

### 🔧 MCP工具支持
- 工具注册表统一管理所有工具
- 支持动态添加新工具
- 标准化的工具接口定义

## 安装和使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
复制 `.env.example` 为 `.env` 并配置相关API密钥：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
# LLM配置
LLM_MODEL=deepseek-chat
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.deepseek.com

# 天气API配置
WEATHER_API_KEY=your_weather_api_key_here
```

### 3. 运行程序
```bash
python main.py
```

## 使用方式

程序提供6种使用模式：

1. **天气查询助手** - 直接与天气Agent对话
2. **IP地址查询助手** - 直接与IP查询Agent对话
3. **多Agent协同聊天** - 所有Agent协同工作
4. **智能路由对话** - 通过路由Agent自动分配任务
5. **显示Agent信息** - 查看所有Agent的能力
6. **显示可用工具** - 查看所有注册的工具

## 扩展新Agent

### 1. 创建Agent文件夹
```bash
mkdir agents/new_agent
touch agents/new_agent/__init__.py
```

### 2. 创建工具模块
在 `agents/new_agent/new_tools.py` 中定义工具函数和schema。

### 3. 创建Agent类
在 `agents/new_agent/new_agent.py` 中创建Agent包装类。

### 4. 注册到系统
在 `common/agent_manager.py` 中添加新Agent的初始化。
在 `mcp/tools_registry.py` 中注册新工具。

## API密钥说明

- **LLM API**: 支持OpenAI兼容的API，默认使用DeepSeek
- **天气API**: 使用OpenWeatherMap API
- **IP查询**: 使用免费的ipapi.co服务

## 技术栈

- **AutoGen**: 多Agent框架
- **httpx**: 异步HTTP客户端
- **python-dotenv**: 环境变量管理
- **typing**: 类型注解支持

## 开发建议

1. **模块化原则**: 每个Agent应该独立封装，职责单一
2. **配置统一**: 所有配置通过config模块管理
3. **工具注册**: 新工具应该注册到tools_registry
4. **错误处理**: 所有API调用都应该有适当的错误处理
5. **文档完善**: 每个模块都应该有清晰的文档说明

## 许可证

MIT License