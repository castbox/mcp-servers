#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件操作MCP模块
提供文件查看、创建和编辑等功能
"""

import os
import json
from typing import Dict, Any, List, Optional, Union
from file_option import FileOption
from mcp.server.fastmcp import FastMCP

# 创建MCP实例
mcp = FastMCP("file_option")


@mcp.tool()
async def read_file(file_path: str, encoding: str = 'utf-8') -> str:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径
        encoding: 文件编码，默认utf-8
        
    Returns:
        str: 文件内容
    """
    return FileOption.read_file(file_path, encoding)


@mcp.tool()
async def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    写入文件内容
    
    Args:
        file_path: 文件路径
        content: 文件内容
        encoding: 文件编码，默认utf-8
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.write_file(file_path, content, encoding)


@mcp.tool()
async def append_file(file_path: str, content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    追加内容到文件
    
    Args:
        file_path: 文件路径
        content: 要追加的内容
        encoding: 文件编码，默认utf-8
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.append_file(file_path, content, encoding)


@mcp.tool()
async def edit_file(file_path: str, old_content: str, new_content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    编辑文件内容（替换指定内容）
    
    Args:
        file_path: 文件路径
        old_content: 要替换的内容
        new_content: 新内容
        encoding: 文件编码，默认utf-8
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.edit_file(file_path, old_content, new_content, encoding)


@mcp.tool()
async def list_directory(directory_path: str) -> Dict[str, Any]:
    """
    列出目录内容
    
    Args:
        directory_path: 目录路径
        
    Returns:
        Dict[str, Any]: 目录内容信息
    """
    return FileOption.list_directory(directory_path)


@mcp.tool()
async def copy_file(source_path: str, destination_path: str) -> Dict[str, Any]:
    """
    复制文件
    
    Args:
        source_path: 源文件路径
        destination_path: 目标文件路径
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.copy_file(source_path, destination_path)


@mcp.tool()
async def move_file(source_path: str, destination_path: str) -> Dict[str, Any]:
    """
    移动文件
    
    Args:
        source_path: 源文件路径
        destination_path: 目标文件路径
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.move_file(source_path, destination_path)


@mcp.tool()
async def delete_file(file_path: str) -> Dict[str, Any]:
    """
    删除文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.delete_file(file_path)


@mcp.tool()
async def create_directory(directory_path: str) -> Dict[str, Any]:
    """
    创建目录
    
    Args:
        directory_path: 目录路径
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.create_directory(directory_path)


@mcp.tool()
async def delete_directory(directory_path: str, recursive: bool = False) -> Dict[str, Any]:
    """
    删除目录
    
    Args:
        directory_path: 目录路径
        recursive: 是否递归删除，默认False
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.delete_directory(directory_path, recursive)


@mcp.tool()
async def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        Dict[str, Any]: 文件信息
    """
    return FileOption.get_file_info(file_path)


@mcp.tool()
async def change_file_permissions(file_path: str, mode: int) -> Dict[str, Any]:
    """
    修改文件权限
    
    Args:
        file_path: 文件路径
        mode: 权限模式，如0o755
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    return FileOption.change_file_permissions(file_path, mode)


if __name__ == "__main__":
    # 运行MCP服务
    mcp.run(transport='stdio')
