#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jenkins 操作模块，提供 Jenkins 服务器的各种操作功能
"""

import jenkins
import json
import time
import sys
from typing import Dict, List, Any, Optional, Union
from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务实例
mcp = FastMCP("jk_option")

# 全局定义 Jenkins 服务器地址、用户名和密码
JENKINS_URL = "http://jenkins.beijing.pundit.company:8080/"  # 请替换为您的 Jenkins 服务器地址
JENKINS_USERNAME = ""  # 请替换为您的 Jenkins 用户名
JENKINS_PASSWORD = ""  # 请替换为您的 Jenkins 密码


# 项目别名映射字典
PROJECT_ALIASES = {
    "GSP_Pgyer": "GoodsSort_Puzzle",
    "GSP_GP": "GoodsSort_Puzzle_Release",
    "GSP_IOS": "GoodsSort_Puzzle_IOS",
    # Key:跟大模型交流的时候的缩写，Value:实际的项目名称
    # 可以添加更多的别名映射
}


class JenkinsClient:
    """Jenkins 客户端类，封装 Jenkins 相关操作"""

    def __init__(self, url: str = JENKINS_URL, username: str = JENKINS_USERNAME, password: str = JENKINS_PASSWORD):
        """
        初始化 Jenkins 客户端
        
        Args:
            url: Jenkins 服务器地址
            username: Jenkins 用户名
            password: Jenkins 密码
        """
        self.url = url
        self.username = username
        self.password = password
        self.server = None
        self.connected = False

    def connect(self) -> bool:
        """
        连接到 Jenkins 服务器
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.server = jenkins.Jenkins(
                self.url, 
                username=self.username, 
                password=self.password
            )
            # 测试连接
            user = self.server.get_whoami()
            version = self.server.get_version()
            print(f"连接成功: Jenkins 版本 {version}, 用户 {user['fullName']}")
            self.connected = True
            return True
        except Exception as e:
            print(f"连接 Jenkins 服务器失败: {str(e)}")
            self.connected = False
            return False

    def _ensure_connected(self) -> bool:
        """
        确保已连接到 Jenkins 服务器
        
        Returns:
            bool: 是否已连接
        """
        if not self.connected:
            return self.connect()
        return True

    def _resolve_job_name(self, job_name: str) -> str:
        """
        解析项目名称，支持别名
        
        Args:
            job_name: 项目名称或别名
            
        Returns:
            str: 实际的项目名称
        """
        return PROJECT_ALIASES.get(job_name, job_name)

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """
        获取所有 Jenkins 项目列表
        
        Returns:
            List[Dict[str, Any]]: 项目列表
        """
        if not self._ensure_connected():
            return []
        
        try:
            jobs = self.server.get_all_jobs()
            job_list = []
            for job in jobs:
                job_list.append({
                    "name": job["name"],
                    "url": job["url"],
                    "fullname": job.get("fullname", job["name"])
                })
            return job_list
        except Exception as e:
            print(f"获取项目列表失败: {str(e)}")
            return []

    def get_job_parameters(self, job_name: str) -> Dict[str, Any]:
        """
        获取指定项目的构建参数
        
        Args:
            job_name: 项目名称或别名
            
        Returns:
            Dict[str, Any]: 构建参数信息
        """
        if not self._ensure_connected():
            return {}
        
        job_name = self._resolve_job_name(job_name)
        
        try:
            job_info = self.server.get_job_info(job_name)
            parameters = []
            
            # 查找参数化构建过程
            if 'property' in job_info:
                for prop in job_info['property']:
                    if 'parameterDefinitions' in prop:
                        for param in prop['parameterDefinitions']:
                            param_info = {
                                "name": param['name'],
                                "type": param['type'],
                                "description": param.get('description', ''),
                                "default_value": param.get('defaultValue', '')
                            }
                            
                            # 如果是选择参数，添加选项
                            if 'choices' in param:
                                param_info['choices'] = param['choices']
                            
                            parameters.append(param_info)
            
            return {
                "job_name": job_name,
                "parameters": parameters
            }
        except Exception as e:
            print(f"获取项目 '{job_name}' 参数失败: {str(e)}")
            return {}

    def build_job(self, job_name: str, parameters: Dict[str, Any] = None) -> Optional[int]:
        """
        使用指定参数构建项目
        
        Args:
            job_name: 项目名称或别名
            parameters: 构建参数
            
        Returns:
            Optional[int]: 构建编号，失败则返回 None
        """
        if not self._ensure_connected():
            return None
        
        job_name = self._resolve_job_name(job_name)
        
        try:
            queue_item = self.server.build_job(job_name, parameters=parameters or {})
            print(f"已触发构建 '{job_name}'，队列项 ID: {queue_item}")
            
            # 等待队列项转换为构建
            for _ in range(30):  # 最多等待30秒
                try:
                    build_number = self.server.get_queue_item(queue_item)['executable']['number']
                    print(f"构建已开始，构建编号: {build_number}")
                    return build_number
                except (KeyError, TypeError):
                    # 队列项尚未转换为构建
                    time.sleep(1)
            
            print("等待构建开始超时")
            return None
        except Exception as e:
            print(f"构建项目 '{job_name}' 失败: {str(e)}")
            return None

    def get_running_builds(self) -> List[Dict[str, Any]]:
        """
        获取当前所有正在运行的构建
        
        Returns:
            List[Dict[str, Any]]: 正在运行的构建列表
        """
        if not self._ensure_connected():
            return []
        
        try:
            running_builds = []
            for job in self.server.get_all_jobs():
                job_name = job['name']
                try:
                    job_info = self.server.get_job_info(job_name)
                    if 'builds' in job_info:
                        for build in job_info['builds']:
                            build_info = self.server.get_build_info(job_name, build['number'])
                            if build_info.get('building', False):
                                running_builds.append({
                                    "job_name": job_name,
                                    "build_number": build['number'],
                                    "url": build['url']
                                })
                except Exception as e:
                    print(f"获取项目 '{job_name}' 构建信息失败: {str(e)}")
                    continue
            
            return running_builds
        except Exception as e:
            print(f"获取正在运行的构建失败: {str(e)}")
            return []

    def stop_build(self, job_name: str, build_number: int) -> bool:
        """
        终止指定的构建
        
        Args:
            job_name: 项目名称或别名
            build_number: 构建编号
            
        Returns:
            bool: 是否成功终止
        """
        if not self._ensure_connected():
            return False
        
        job_name = self._resolve_job_name(job_name)
        
        try:
            self.server.stop_build(job_name, build_number)
            print(f"已终止项目 '{job_name}' 的构建 #{build_number}")
            return True
        except Exception as e:
            print(f"终止项目 '{job_name}' 的构建 #{build_number} 失败: {str(e)}")
            return False

    def get_build_status(self, job_name: str, build_number: int) -> Dict[str, Any]:
        """
        获取指定构建的状态
        
        Args:
            job_name: 项目名称或别名
            build_number: 构建编号
            
        Returns:
            Dict[str, Any]: 构建状态信息
        """
        if not self._ensure_connected():
            return {}
        
        job_name = self._resolve_job_name(job_name)
        
        try:
            build_info = self.server.get_build_info(job_name, build_number)
            return {
                "job_name": job_name,
                "build_number": build_number,
                "building": build_info.get('building', False),
                "result": build_info.get('result'),
                "duration": build_info.get('duration', 0),
                "timestamp": build_info.get('timestamp', 0),
                "url": build_info.get('url', '')
            }
        except Exception as e:
            print(f"获取项目 '{job_name}' 的构建 #{build_number} 状态失败: {str(e)}")
            return {}

    def add_alias(self, alias: str, job_name: str) -> bool:
        """
        添加项目别名
        
        Args:
            alias: 别名
            job_name: 实际项目名称
            
        Returns:
            bool: 是否成功添加
        """
        global PROJECT_ALIASES
        
        try:
            # 验证项目是否存在
            if self._ensure_connected():
                try:
                    self.server.get_job_info(job_name)
                    PROJECT_ALIASES[alias] = job_name
                    print(f"已添加别名: {alias} -> {job_name}")
                    return True
                except jenkins.NotFoundException:
                    print(f"项目 '{job_name}' 不存在，无法添加别名")
                    return False
            return False
        except Exception as e:
            print(f"添加别名失败: {str(e)}")
            return False


@mcp.tool()
async def get_all_jobs() -> List[Dict[str, Any]]:
    """
    获取所有 Jenkins 项目
    
    Returns:
        List[Dict[str, Any]]: 项目列表
    """
    client = JenkinsClient()
    if not client.connect():
        #返回连接失败错误信息，按照List格式返回
        return [{"error": "连接失败"}]

    return client.get_all_jobs()

@mcp.tool()
async def get_job_parameters(job_name: str) -> Dict[str, Any]:
    """
    获取指定项目的详细信息
    
    Args:
        job_name: 项目名称或别名
        
    Returns:
        Dict[str, Any]: 项目信息
    """
    client = JenkinsClient()
    if not client.connect():
        #返回连接失败错误信息，按照Dict格式返回
        return {"error": "连接失败"}
    
    return client.get_job_parameters(job_name)


@mcp.tool()
async def build_job(job_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    根据指定的参数进行项目构建
    
    Args:
        job_name: 项目名称或别名
        parameters: 构建参数
        
    Returns:
        Dict[str, Any]: 构建结果
    """
    client = JenkinsClient()
    if not client.connect():
        #返回连接失败错误信息，按照Dict格式返回
        return {"error": "连接失败"}
    
    return client.build_job(job_name, parameters)


@mcp.tool()
async def get_build_status(job_name: str, build_number: int) -> Dict[str, Any]:
    """
    获取指定构建的状态
    
    Args:
        job_name: 项目名称或别名
        build_number: 构建编号
        
    Returns:
        Dict[str, Any]: 构建状态
    """
    client = JenkinsClient()
    if not client.connect():
        #返回连接失败错误信息，按照Dict格式返回
        return {"error": "连接失败"}
    
    return client.get_build_status(job_name, build_number)


@mcp.tool()
async def stop_build(job_name: str, build_number: int) -> Dict[str, Any]:
    """
    终止指定构建
    
    Args:
        job_name: 项目名称或别名
        build_number: 构建编号
        
    Returns:
        Dict[str, Any]: 终止结果
    """
    client = JenkinsClient()
    if not client.connect():
        #返回连接失败错误信息，按照Dict格式返回
        return {"error": "连接失败"}
    
    return client.stop_build(job_name, build_number)



if __name__ == "__main__":
    mcp.run(transport='stdio')