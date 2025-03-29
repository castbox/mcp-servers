from mcp.server.fastmcp import FastMCP
import subprocess
import os
import json
import inspect
from typing import List, Optional, Dict, Any, Union

# 导入项目中的功能模块
from download_docs import GoogleDocsDownloader
from list_accessible_docs import GoogleDocsLister
from weekly_report_updater import WeeklyReportUpdater
from config import SPREADSHEET_ID, TARGET_SHEET_INDEX

mcp = FastMCP("google_sheet_mcp")


@mcp.tool()
async def readme() -> str:
    """
    显示Google Sheets MCP工具的帮助信息
    
    返回:
        str: 帮助信息文本
    """
    help_text = """
    === Google Sheets MCP 工具帮助 ===
    
    本工具提供以下功能：
    
    1. 文档列表查询功能：
       - list_all_files(): 列出所有可访问的文件
       - list_spreadsheets(): 列出所有可访问的表格
       - list_documents(): 列出所有可访问的文档
    
    2. 文档下载功能：
       - download_spreadsheet(spreadsheet_id, format): 下载指定表格
         * spreadsheet_id: 表格ID
         * format: 下载格式，支持 'csv'、'json'、'excel'，默认为'excel'
       - download_document(document_id, format): 下载指定文档
         * document_id: 文档ID
         * format: 下载格式，支持 'txt'、'docx'，默认为'docx'
       - download_all_files(format_sheet, format_doc): 下载所有可访问的文件
         * format_sheet: 表格下载格式，默认为'excel'
         * format_doc: 文档下载格式，默认为'docx'
    
    3. 周报更新功能：
       - find_person(name): 查找指定人员在周报中的行
         * name: 人员姓名
       - get_weekly_report(name): 获取指定人员的周报内容
         * name: 人员姓名
       - update_weekly_report(name, this_week, next_week): 更新指定人员的周报
         * name: 人员姓名
         * this_week: 本周工作内容
         * next_week: 下周工作计划
       - update_weekly_report_by_config(this_week, next_week): 根据默认配置更新周报
         * this_week: 本周工作内容
         * next_week: 下周工作计划
         * 注意：该方法使用config.py中的TARGET_NAME作为人员姓名
    
    4. 配置管理功能：
       - get_config(): 获取config.py中的所有配置项
         * 返回所有当前配置项，包括表格ID、目标sheet索引、周报相关配置等
    
    使用示例：
    1. 列出所有可访问的表格：list_spreadsheets()
    2. 下载指定表格为Excel：download_spreadsheet("表格ID", "excel")
    3. 更新周报：update_weekly_report("张三", "完成了A项目", "开始B项目")
    4. 查看当前配置：get_config()
    5. 根据默认配置更新周报：update_weekly_report_by_config("完成了项目X", "开始项目Y")
    """
    return help_text


@mcp.tool()
async def list_all_files(max_results: int = 100) -> List[Dict[str, str]]:
    """
    列出所有可访问的文件
    
    参数:
        max_results: 最大结果数量，默认100
    
    返回:
        List[Dict[str, str]]: 文件列表，每个文件包含id、name、mimeType等信息
    """
    lister = GoogleDocsLister()
    if not lister.connect():
        return [{"error": "连接Google API失败"}]
    
    files = lister.list_accessible_files(max_results=max_results)
    return files


@mcp.tool()
async def list_spreadsheets(max_results: int = 100) -> List[Dict[str, str]]:
    """
    列出所有可访问的表格
    
    参数:
        max_results: 最大结果数量，默认100
    
    返回:
        List[Dict[str, str]]: 表格列表，每个表格包含id、name等信息
    """
    lister = GoogleDocsLister()
    if not lister.connect():
        return [{"error": "连接Google API失败"}]
    
    spreadsheets = lister.list_accessible_files(
        file_type='application/vnd.google-apps.spreadsheet',
        max_results=max_results
    )
    return spreadsheets


@mcp.tool()
async def list_documents(max_results: int = 100) -> List[Dict[str, str]]:
    """
    列出所有可访问的文档
    
    参数:
        max_results: 最大结果数量，默认100
    
    返回:
        List[Dict[str, str]]: 文档列表，每个文档包含id、name等信息
    """
    lister = GoogleDocsLister()
    if not lister.connect():
        return [{"error": "连接Google API失败"}]
    
    documents = lister.list_accessible_files(
        file_type='application/vnd.google-apps.document',
        max_results=max_results
    )
    return documents


@mcp.tool()
async def download_spreadsheet(spreadsheet_id: str, format: str = "excel", delay: float = 1.5) -> Dict[str, Any]:
    """
    下载指定的表格
    
    参数:
        spreadsheet_id: 表格ID
        format: 下载格式，支持 'csv'、'json'、'excel'，默认为'excel'
        delay: API请求间隔延迟，单位秒，默认1.5
    
    返回:
        Dict[str, Any]: 下载结果信息
    """
    if format not in ['csv', 'json', 'excel']:
        return {"error": f"不支持的格式: {format}，请使用 csv、json 或 excel 格式"}
    
    downloader = GoogleDocsDownloader(rate_limit_delay=delay)
    if not downloader.connect():
        return {"error": "连接Google API失败"}
    
    success = downloader.download_spreadsheet(spreadsheet_id, format)
    if success:
        return {"status": "success", "message": f"表格下载完成，已保存到 downloads 目录"}
    else:
        return {"error": "表格下载失败"}


@mcp.tool()
async def download_document(document_id: str, format: str = "docx", delay: float = 1.5) -> Dict[str, Any]:
    """
    下载指定的文档
    
    参数:
        document_id: 文档ID
        format: 下载格式，支持 'txt'、'docx'，默认为'docx'
        delay: API请求间隔延迟，单位秒，默认1.5
    
    返回:
        Dict[str, Any]: 下载结果信息
    """
    if format not in ['txt', 'docx']:
        return {"error": f"不支持的格式: {format}，请使用 txt 或 docx 格式"}
    
    downloader = GoogleDocsDownloader(rate_limit_delay=delay)
    if not downloader.connect():
        return {"error": "连接Google API失败"}
    
    success = downloader.download_document(document_id, format)
    if success:
        return {"status": "success", "message": f"文档下载完成，已保存到 downloads 目录"}
    else:
        return {"error": "文档下载失败"}


@mcp.tool()
async def download_all_files(format_sheet: str = "excel", format_doc: str = "docx", delay: float = 1.5) -> Dict[str, Any]:
    """
    下载所有可访问的文件
    
    参数:
        format_sheet: 表格下载格式，支持 'csv'、'json'、'excel'，默认为'excel'
        format_doc: 文档下载格式，支持 'txt'、'docx'，默认为'docx'
        delay: API请求间隔延迟，单位秒，默认1.5
    
    返回:
        Dict[str, Any]: 下载结果信息
    """
    if format_sheet not in ['csv', 'json', 'excel']:
        return {"error": f"不支持的表格格式: {format_sheet}，请使用 csv、json 或 excel 格式"}
    
    if format_doc not in ['txt', 'docx']:
        return {"error": f"不支持的文档格式: {format_doc}，请使用 txt 或 docx 格式"}
    
    downloader = GoogleDocsDownloader(rate_limit_delay=delay)
    if not downloader.connect():
        return {"error": "连接Google API失败"}
    
    # 下载表格
    spreadsheets = downloader.list_accessible_files(
        file_type='application/vnd.google-apps.spreadsheet'
    )
    
    sheet_count = 0
    if spreadsheets:
        for sheet in spreadsheets:
            sheet_id = sheet.get('id')
            downloader.download_spreadsheet(sheet_id, format_sheet)
            sheet_count += 1
    
    # 下载文档
    documents = downloader.list_accessible_files(
        file_type='application/vnd.google-apps.document'
    )
    
    doc_count = 0
    if documents:
        for doc in documents:
            doc_id = doc.get('id')
            downloader.download_document(doc_id, format_doc)
            doc_count += 1
    
    return {
        "status": "success", 
        "message": f"下载完成，共下载 {sheet_count} 个表格和 {doc_count} 个文档，已保存到 downloads 目录"
    }


@mcp.tool()
async def find_person(name: str, spreadsheet_id: str = SPREADSHEET_ID, sheet_index: int = TARGET_SHEET_INDEX) -> Dict[str, Any]:
    """
    查找指定人员在周报中的行
    
    参数:
        name: 人员姓名
        spreadsheet_id: 表格ID，默认使用配置中的ID
        sheet_index: 工作表索引，默认使用配置中的索引
    
    返回:
        Dict[str, Any]: 查找结果信息
    """
    updater = WeeklyReportUpdater(spreadsheet_id, sheet_index)
    if not updater.connect():
        return {"error": "连接Google Sheets失败"}
    
    row_index = updater.find_person_row(name)
    if row_index is None:
        return {"error": f"未找到人员: {name}"}
    
    sheet_props = updater.get_sheet_info()
    sheet_title = sheet_props.get('title', '未知') if sheet_props else '未知'
    
    return {
        "status": "success",
        "name": name,
        "row_index": row_index,
        "row_number": row_index + 1,
        "sheet_title": sheet_title
    }


@mcp.tool()
async def get_weekly_report(name: str, spreadsheet_id: str = SPREADSHEET_ID, sheet_index: int = TARGET_SHEET_INDEX) -> Dict[str, Any]:
    """
    获取指定人员的周报内容
    
    参数:
        name: 人员姓名
        spreadsheet_id: 表格ID，默认使用配置中的ID
        sheet_index: 工作表索引，默认使用配置中的索引
    
    返回:
        Dict[str, Any]: 周报内容
    """
    updater = WeeklyReportUpdater(spreadsheet_id, sheet_index)
    if not updater.connect():
        return {"error": "连接Google Sheets失败"}
    
    row_index = updater.find_person_row(name)
    if row_index is None:
        return {"error": f"未找到人员: {name}"}
    
    this_week, next_week = updater.get_current_content(row_index)
    if this_week is None or next_week is None:
        return {"error": f"获取周报内容失败"}
    
    return {
        "status": "success",
        "name": name,
        "this_week": this_week,
        "next_week": next_week
    }


@mcp.tool()
async def update_weekly_report(name: str, this_week: str, next_week: str, spreadsheet_id: str = SPREADSHEET_ID, sheet_index: int = TARGET_SHEET_INDEX) -> Dict[str, Any]:
    """
    更新指定人员的周报
    
    参数:
        name: 人员姓名
        this_week: 本周工作内容
        next_week: 下周工作计划
        spreadsheet_id: 表格ID，默认使用配置中的ID
        sheet_index: 工作表索引，默认使用配置中的索引
    
    返回:
        Dict[str, Any]: 更新结果信息
    """
    updater = WeeklyReportUpdater(spreadsheet_id, sheet_index)
    if not updater.connect():
        return {"error": "连接Google Sheets失败"}
    
    success = updater.update_weekly_report(name, this_week, next_week)
    if not success:
        return {"error": f"更新周报失败"}
    
    return {
        "status": "success",
        "message": f"已成功更新 {name} 的周报",
        "name": name,
        "this_week": this_week,
        "next_week": next_week
    }


@mcp.tool()
async def get_config() -> Dict[str, Any]:
    """
    获取config.py中的所有配置项
    
    返回:
        Dict[str, Any]: 配置信息字典
    """
    import config
    import inspect
    
    # 获取config模块中的所有变量
    config_dict = {}
    for name, value in inspect.getmembers(config):
        # 排除内置属性和方法
        if not name.startswith('__') and not inspect.ismodule(value) and not inspect.isfunction(value) and not inspect.isclass(value):
            # 对于列表类型，转换为字符串以便于显示
            if isinstance(value, list):
                config_dict[name] = [str(item) for item in value]
            else:
                config_dict[name] = value
    
    return {
        "status": "success",
        "config": config_dict
    }


@mcp.tool()
async def update_weekly_report_by_config(this_week: str, next_week: str) -> Dict[str, Any]:
    """
    根据config.py中的默认配置更新周报
    
    参数:
        this_week: 本周工作内容
        next_week: 下周工作计划
    
    返回:
        Dict[str, Any]: 更新结果信息
    """
    import config
    
    # 从配置中获取默认值
    name = config.TARGET_NAME
    spreadsheet_id = config.SPREADSHEET_ID
    sheet_index = config.TARGET_SHEET_INDEX
    
    updater = WeeklyReportUpdater(spreadsheet_id, sheet_index)
    if not updater.connect():
        return {"error": "连接Google Sheets失败"}
    
    success = updater.update_weekly_report(name, this_week, next_week)
    if not success:
        return {"error": f"更新周报失败"}
    
    return {
        "status": "success",
        "message": f"已成功更新 {name} 的周报",
        "name": name,
        "this_week": this_week,
        "next_week": next_week
    }


if __name__ == "__main__":
    mcp.run(transport='stdio')