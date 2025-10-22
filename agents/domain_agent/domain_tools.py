"""
域名查询工具模块
提供域名基础信息查询和状态检测功能
"""
import hashlib
import httpx
import asyncio
import time
from typing import Dict, Any, List


class DomainAPIClient:
    """域名API客户端类，封装鉴权和请求逻辑"""
    
    def __init__(self, app_code='xhq', erp='xiehanqi.jackson', business_id='6abe3998080d92d648d7ad461bd67f38'):
        self.app_code = app_code
        self.erp = erp
        self.business_id = business_id
        self.base_url = "http://api-np.jd.local/V1/Dns"
    
    def _generate_auth_headers(self):
        """生成鉴权请求头"""
        timestamp = str(int(time.time()))
        time_str = time.strftime("%H%M%Y%m%d", time.localtime(int(timestamp)))
        sign_str = f"{self.erp}#{self.business_id}NP{time_str}"
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
        return {
            "Content-type": "application/json",
            "appCode": self.app_code,
            "erp": self.erp,
            "timestamp": timestamp,
            "sign": sign
        }


async def batch_get_domains_info(domains: str) -> str:
    """批量获取域名基础信息"""
    try:
        # 解析域名列表（支持逗号或换行分隔）
        domain_list = []
        for domain in domains.replace('\n', ',').split(','):
            domain = domain.strip()
            if domain:
                domain_list.append(domain)
        
        if not domain_list:
            return "错误: 请提供有效的域名列表"
        
        client = DomainAPIClient()
        headers = client._generate_auth_headers()
        url = f"{client.base_url}/domainsInfo"
        
        async with httpx.AsyncClient(timeout=30) as http_client:
            response = await http_client.post(
                url, 
                headers=headers, 
                json={"domains": domain_list}
            )
            
            if response.status_code == 200:
                result = response.json()
                return _format_domains_info_result(result, domain_list)
            else:
                return f"域名信息查询失败，状态码: {response.status_code}"
                
    except Exception as e:
        return f"域名信息查询错误: {str(e)}"


async def batch_check_domains_status(domains: str) -> str:
    """批量检测域名状态"""
    try:
        # 解析域名列表
        domain_list = []
        for domain in domains.replace('\n', ',').split(','):
            domain = domain.strip()
            if domain:
                domain_list.append(domain)
        
        if not domain_list:
            return "错误: 请提供有效的域名列表"
        
        client = DomainAPIClient()
        headers = client._generate_auth_headers()
        url = f"{client.base_url}/domainCheck"
        
        results = []
        
        async with httpx.AsyncClient(timeout=30) as http_client:
            for i, domain in enumerate(domain_list, 1):
                try:
                    response = await http_client.get(
                        url, 
                        headers=headers, 
                        params={"domain": domain}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        status_info = _format_single_domain_status(result, domain)
                        results.append(f"[{i}/{len(domain_list)}] {status_info}")
                    else:
                        results.append(f"[{i}/{len(domain_list)}] {domain}: 检测失败 (状态码: {response.status_code})")
                    
                    # 避免请求过于频繁
                    if i < len(domain_list):
                        await asyncio.sleep(0.5)
                        
                except Exception as e:
                    results.append(f"[{i}/{len(domain_list)}] {domain}: 检测异常 - {str(e)}")
        
        return f"域名状态批量检测结果:\n{'='*60}\n" + "\n".join(results)
        
    except Exception as e:
        return f"域名状态检测错误: {str(e)}"


def _format_domains_info_result(response_data: Dict, domains: List[str]) -> str:
    """格式化域名信息查询结果"""
    if response_data.get('resStatus') != 200:
        return f"查询失败: {response_data.get('resMsg', '未知错误')}"
    
    data = response_data.get('data', {})
    count = data.get('count', 0)
    infos = data.get('infos', [])
    
    if not infos:
        return f"未找到域名信息 (查询域名: {', '.join(domains)})"
    
    result_lines = [f"域名基础信息查询结果 (共 {count} 个域名)"]
    result_lines.append("=" * 60)
    
    for i, info in enumerate(infos, 1):
        result_lines.append(f"\n📌 域名 #{i}: {info.get('domain', 'N/A')}")
        result_lines.append(f"   状态: {info.get('status_desc', 'N/A')} (代码: {info.get('status', 'N/A')})")
        result_lines.append(f"   服务类型: {info.get('service_type', 'N/A')}")
        result_lines.append(f"   网络: {info.get('network', 'N/A')}")
        result_lines.append(f"   重要性: {info.get('primary', 'N/A')}")
        result_lines.append(f"   应用环境: {info.get('app_env', 'N/A')}")
        
        if info.get('project_name'):
            project_info = info.get('project_name')
            if info.get('project_id'):
                project_info += f" (ID: {info.get('project_id')})"
            result_lines.append(f"   项目: {project_info}")
        
        result_lines.append(f"   负责人: {info.get('owner', 'N/A')}")
        
        if info.get('manage_name'):
            manage_info = info.get('manage_name')
            if info.get('manage_erp'):
                manage_info += f" ({info.get('manage_erp')})"
            result_lines.append(f"   管理员: {manage_info}")
        
        if info.get('org_fullname'):
            result_lines.append(f"   组织: {info.get('org_fullname')}")
        
        if info.get('remark'):
            result_lines.append(f"   备注: {info.get('remark')}")
    
    return "\n".join(result_lines)


def _format_single_domain_status(response_data: Dict, domain: str) -> str:
    """格式化单个域名状态检测结果"""
    if response_data.get('resStatus') != 200:
        return f"{domain}: 检测失败 - {response_data.get('resMsg', '未知错误')}"
    
    data = response_data.get('data', {})
    status = data.get('status')
    msg = data.get('msg', '')
    
    status_descriptions = {
        -1: "可申请 ✅",
        1: "DNS已解析 🔗", 
        2: "商家域名 🏪",
        3: "NP系统预留 🔒"
    }
    
    availability = status_descriptions.get(status, f"未知状态({status})")
    return f"{domain}: {msg} - {availability}"


# 同步版本的函数
def batch_get_domains_info_sync(domains: str) -> str:
    """同步版本的批量域名信息查询"""
    return asyncio.run(batch_get_domains_info(domains))


def batch_check_domains_status_sync(domains: str) -> str:
    """同步版本的批量域名状态检测"""
    return asyncio.run(batch_check_domains_status(domains))


# MCP工具schema定义
def get_batch_domains_info_schema() -> Dict[str, Any]:
    """获取批量域名信息查询工具的schema定义"""
    return {
        "name": "batch_get_domains_info",
        "description": "批量查询域名的基础信息，包括状态、服务类型、负责人、项目等详细信息",
        "parameters": {
            "type": "object",
            "properties": {
                "domains": {
                    "type": "string",
                    "description": "要查询的域名列表，多个域名用逗号或换行分隔，如: 'example.com,test.jd.local' 或 'example.com\\ntest.jd.local'"
                }
            },
            "required": ["domains"]
        }
    }


def get_batch_domains_status_schema() -> Dict[str, Any]:
    """获取批量域名状态检测工具的schema定义"""
    return {
        "name": "batch_check_domains_status", 
        "description": "批量检测域名状态，判断域名是否空闲可申请，返回每个域名的可用性状态",
        "parameters": {
            "type": "object",
            "properties": {
                "domains": {
                    "type": "string", 
                    "description": "要检测状态的域名列表，多个域名用逗号或换行分隔，如: 'example.com,test.jd.local' 或 'example.com\\ntest.jd.local'"
                }
            },
            "required": ["domains"]
        }
    }