#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google 文档列表查询工具
用于查找服务账号有权限访问的所有 Google 文档
"""

import os
import logging
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import SCOPES, SERVICE_ACCOUNT_FILE

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class GoogleDocsLister:
    """Google 文档列表查询工具类"""
    
    def __init__(self, credentials_file=None):
        """初始化查询工具"""
        self.credentials_file = credentials_file or SERVICE_ACCOUNT_FILE
        self.credentials = None
        self.drive_service = None
        self.sheets_service = None
        self.docs_service = None
        
    def connect(self):
        """连接到 Google API"""
        try:
            # 检查凭证文件是否存在
            if not os.path.exists(self.credentials_file):
                logging.error(f"凭证文件 {self.credentials_file} 不存在")
                return False
                
            logging.info(f"正在加载凭证文件: {self.credentials_file}")
            
            # 创建凭证
            self.credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file, scopes=SCOPES)
            
            # 输出服务账号邮箱
            logging.info(f"服务账号邮箱: {self.credentials.service_account_email}")
            
            # 创建 Drive 服务 (用于列出文件)
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
            
            # 创建 Sheets 服务 (用于操作表格)
            self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
            
            # 创建 Docs 服务 (用于操作文档)
            self.docs_service = build('docs', 'v1', credentials=self.credentials)
            
            logging.info("成功连接到 Google API")
            return True
            
        except Exception as e:
            logging.error(f"连接 Google API 失败: {e}")
            import traceback
            logging.error(traceback.format_exc())
            return False
    
    def list_accessible_files(self, file_type=None, max_results=100):
        """
        列出服务账号有权限访问的所有文件
        
        参数:
            file_type: 文件类型过滤，例如 'application/vnd.google-apps.spreadsheet' 表示只列出表格
            max_results: 最大结果数量
        """
        if not self.drive_service:
            if not self.connect():
                return []
                
        try:
            query = ""
            if file_type:
                query = f"mimeType='{file_type}'"
                
            logging.info(f"正在查询可访问的文件，查询条件: {query or '所有文件'}")
            
            # 列出文件
            results = self.drive_service.files().list(
                q=query,
                pageSize=max_results,
                fields="nextPageToken, files(id, name, mimeType, webViewLink)"
            ).execute()
            
            items = results.get('files', [])
            
            if not items:
                logging.info("未找到可访问的文件")
                return []
                
            logging.info(f"找到 {len(items)} 个可访问的文件")
            return items
            
        except HttpError as error:
            logging.error(f"查询文件失败: {error}")
            return []
    
    def list_accessible_spreadsheets(self, max_results=100):
        """列出服务账号有权限访问的所有表格"""
        return self.list_accessible_files(
            file_type='application/vnd.google-apps.spreadsheet',
            max_results=max_results
        )
    
    def list_accessible_documents(self, max_results=100):
        """列出服务账号有权限访问的所有文档"""
        return self.list_accessible_files(
            file_type='application/vnd.google-apps.document',
            max_results=max_results
        )
    
    def print_file_list(self, files):
        """打印文件列表"""
        if not files:
            print("未找到可访问的文件")
            return
            
        print(f"\n找到 {len(files)} 个可访问的文件:")
        print("-" * 80)
        print(f"{'序号':<5} {'文件名':<40} {'文件类型':<20} {'文件ID':<40}")
        print("-" * 80)
        
        for i, file in enumerate(files, 1):
            mime_type = file.get('mimeType', '')
            file_type = '未知'
            
            if 'spreadsheet' in mime_type:
                file_type = '表格'
            elif 'document' in mime_type:
                file_type = '文档'
            elif 'presentation' in mime_type:
                file_type = '演示文稿'
            elif 'folder' in mime_type:
                file_type = '文件夹'
                
            print(f"{i:<5} {file.get('name', '')[:38]:<40} {file_type:<20} {file.get('id', ''):<40}")
            
        print("-" * 80)
        print("如需访问这些文件，可以使用以下格式的URL:")
        print("- 表格: https://docs.google.com/spreadsheets/d/{fileId}/edit")
        print("- 文档: https://docs.google.com/document/d/{fileId}/edit")
        print("- 演示文稿: https://docs.google.com/presentation/d/{fileId}/edit")


def main():
    """主函数"""
    lister = GoogleDocsLister()
    
    if not lister.connect():
        logging.error("连接 Google API 失败")
        return 1
    
    # 列出所有可访问的文件
    print("\n=== 所有可访问的文件 ===")
    all_files = lister.list_accessible_files()
    lister.print_file_list(all_files)
    
    # 列出可访问的表格
    print("\n=== 可访问的表格 ===")
    spreadsheets = lister.list_accessible_spreadsheets()
    lister.print_file_list(spreadsheets)
    
    # 列出可访问的文档
    print("\n=== 可访问的文档 ===")
    documents = lister.list_accessible_documents()
    lister.print_file_list(documents)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
