#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google Sheets 连接器
参考 l10n_engine.py 中的实现方式，简化连接 Google Sheets 的过程
"""

import os
import logging
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import SCOPES, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, TARGET_SHEET_INDEX

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class GoogleSheetsConnector:
    """Google Sheets 连接器类"""
    
    def __init__(self, spreadsheet_id=None):
        """初始化连接器"""
        self.spreadsheet_id = spreadsheet_id or SPREADSHEET_ID
        self.service = None
        self.sheet = None
        
    def connect(self):
        """连接到 Google Sheets API"""
        try:
            # 检查凭证文件是否存在
            if not os.path.exists(SERVICE_ACCOUNT_FILE):
                logging.error(f"凭证文件 {SERVICE_ACCOUNT_FILE} 不存在")
                return False
                
            logging.info(f"正在加载凭证文件: {SERVICE_ACCOUNT_FILE}")
            
            # 直接创建凭证，参考 l10n_engine.py 的实现方式
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            
            # 输出服务账号邮箱
            logging.info(f"服务账号邮箱: {credentials.service_account_email}")
            logging.info(f"请确保已将表格共享给服务账号: {credentials.service_account_email}")
            
            # 创建服务
            self.service = build('sheets', 'v4', credentials=credentials)
            self.sheet = self.service.spreadsheets()
            
            logging.info("成功连接到 Google Sheets API")
            return True
            
        except Exception as e:
            logging.error(f"连接 Google Sheets API 失败: {e}")
            import traceback
            logging.error(traceback.format_exc())
            return False
    
    def get_spreadsheet_info(self):
        """获取表格信息"""
        if not self.service or not self.sheet:
            if not self.connect():
                return None
                
        try:
            logging.info(f"正在获取表格信息，表格ID: {self.spreadsheet_id}")
            return self.sheet.get(spreadsheetId=self.spreadsheet_id).execute()
        except Exception as e:
            logging.error(f"获取表格信息失败: {e}")
            return None
    
    def get_sheet_by_index(self, sheet_index):
        """根据索引获取工作表"""
        spreadsheet = self.get_spreadsheet_info()
        if not spreadsheet:
            logging.error(f"无法获取第{sheet_index+1}个sheet，请检查表格ID和sheet索引")
            return None
            
        try:
            sheet_properties = spreadsheet['sheets'][sheet_index]['properties']
            logging.info(f"成功获取工作表: {sheet_properties['title']}")
            return sheet_properties
        except (IndexError, KeyError) as e:
            logging.error(f"获取工作表失败: {e}")
            return None
    
    def get_values(self, range_name):
        """获取指定范围的值"""
        if not self.service or not self.sheet:
            if not self.connect():
                return None
                
        try:
            logging.info(f"正在获取范围 {range_name} 的值")
            result = self.sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            return result.get('values', [])
        except Exception as e:
            logging.error(f"获取值失败: {e}")
            return None
    
    def update_values(self, range_name, values):
        """更新指定范围的值"""
        if not self.service or not self.sheet:
            if not self.connect():
                return False
                
        try:
            logging.info(f"正在更新范围 {range_name} 的值")
            request = self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body={'values': values}
            )
            response = request.execute()
            logging.info(f"更新成功: {response}")
            return True
        except Exception as e:
            logging.error(f"更新值失败: {e}")
            return False


def test_connection():
    """测试连接功能"""
    connector = GoogleSheetsConnector()
    if connector.connect():
        logging.info("连接测试成功")
        
        # 获取表格信息
        spreadsheet_info = connector.get_spreadsheet_info()
        if spreadsheet_info:
            logging.info(f"表格标题: {spreadsheet_info.get('properties', {}).get('title', '未知')}")
            
        # 获取指定工作表
        sheet_props = connector.get_sheet_by_index(TARGET_SHEET_INDEX)
        if sheet_props:
            logging.info(f"工作表标题: {sheet_props.get('title', '未知')}")
            
        return True
    else:
        logging.error("连接测试失败")
        return False


if __name__ == "__main__":
    test_connection()
