#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
周报更新工具
用于查找特定人员并更新他们的周报内容
"""

import os
import logging
import sys
import argparse
from google_sheets_connector import GoogleSheetsConnector
from config import (
    SPREADSHEET_ID, TARGET_SHEET_INDEX, NAME_COLUMN,
    TARGET_NAME, THIS_WEEK_COLUMN, NEXT_WEEK_COLUMN,
    THIS_WEEK_CONTENT, NEXT_WEEK_CONTENT
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class WeeklyReportUpdater:
    """周报更新工具类"""
    
    def __init__(self, spreadsheet_id=None, sheet_index=None):
        """初始化周报更新工具"""
        self.spreadsheet_id = spreadsheet_id or SPREADSHEET_ID
        self.sheet_index = sheet_index or TARGET_SHEET_INDEX
        self.connector = GoogleSheetsConnector(self.spreadsheet_id)
        
    def connect(self):
        """连接到 Google Sheets"""
        return self.connector.connect()
        
    def get_sheet_info(self):
        """获取工作表信息"""
        sheet_props = self.connector.get_sheet_by_index(self.sheet_index)
        if not sheet_props:
            return None
            
        sheet_title = sheet_props.get('title', '未知')
        logging.info(f"工作表标题: {sheet_title}")
        return sheet_props
        
    def find_person_row(self, name=None):
        """查找指定人员所在的行"""
        target_name = name or TARGET_NAME
        logging.info(f"正在查找人员: {target_name}")
        
        # 获取工作表信息
        sheet_props = self.get_sheet_info()
        if not sheet_props:
            return None
            
        sheet_title = sheet_props.get('title', '未知')
        
        # 获取所有数据
        values = self.connector.get_values(f"'{sheet_title}'")
        if not values:
            logging.error("获取表格数据失败")
            return None
            
        # 查找人员所在行
        for i, row in enumerate(values):
            if len(row) > NAME_COLUMN and row[NAME_COLUMN] == target_name:
                logging.info(f"找到人员 {target_name} 在第 {i+1} 行")
                return i
                
        logging.error(f"未找到人员: {target_name}")
        return None
        
    def get_current_content(self, row_index):
        """获取当前的周报内容"""
        if row_index is None:
            return None, None
            
        # 获取工作表信息
        sheet_props = self.get_sheet_info()
        if not sheet_props:
            return None, None
            
        sheet_title = sheet_props.get('title', '未知')
        
        # 获取指定行的数据
        row_values = self.connector.get_values(f"'{sheet_title}'!{row_index+1}:{row_index+1}")
        if not row_values or not row_values[0]:
            logging.error(f"获取第 {row_index+1} 行数据失败")
            return None, None
            
        row_data = row_values[0]
        
        # 获取本周工作内容和下周计划
        this_week = row_data[THIS_WEEK_COLUMN] if len(row_data) > THIS_WEEK_COLUMN else ""
        next_week = row_data[NEXT_WEEK_COLUMN] if len(row_data) > NEXT_WEEK_COLUMN else ""
        
        logging.info(f"当前本周工作内容: {this_week}")
        logging.info(f"当前下周工作计划: {next_week}")
        
        return this_week, next_week
        
    def update_weekly_report(self, name=None, this_week=None, next_week=None):
        """更新周报内容"""
        target_name = name or TARGET_NAME
        this_week_content = this_week or THIS_WEEK_CONTENT
        next_week_content = next_week or NEXT_WEEK_CONTENT
        
        # 查找人员所在行
        row_index = self.find_person_row(target_name)
        if row_index is None:
            return False
            
        # 获取工作表信息
        sheet_props = self.get_sheet_info()
        if not sheet_props:
            return False
            
        sheet_title = sheet_props.get('title', '未知')
        
        # 更新本周工作内容
        if this_week_content:
            this_week_range = f"'{sheet_title}'!{chr(65+THIS_WEEK_COLUMN)}{row_index+1}"
            this_week_values = [[this_week_content]]
            if not self.connector.update_values(this_week_range, this_week_values):
                logging.error("更新本周工作内容失败")
                return False
            logging.info(f"成功更新本周工作内容: {this_week_content}")
            
        # 更新下周工作计划
        if next_week_content:
            next_week_range = f"'{sheet_title}'!{chr(65+NEXT_WEEK_COLUMN)}{row_index+1}"
            next_week_values = [[next_week_content]]
            if not self.connector.update_values(next_week_range, next_week_values):
                logging.error("更新下周工作计划失败")
                return False
            logging.info(f"成功更新下周工作计划: {next_week_content}")
            
        return True


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='周报更新工具')
    parser.add_argument('--name', type=str, help='要查找的人员姓名')
    parser.add_argument('--this-week', type=str, help='本周工作内容')
    parser.add_argument('--next-week', type=str, help='下周工作计划')
    parser.add_argument('--test', action='store_true', help='测试模式，只查找人员不更新内容')
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    updater = WeeklyReportUpdater()
    if not updater.connect():
        logging.error("连接 Google Sheets 失败")
        return 1
        
    # 测试模式，只查找人员并显示当前内容
    if args.test:
        row_index = updater.find_person_row(args.name)
        if row_index is not None:
            updater.get_current_content(row_index)
        return 0
        
    # 更新周报
    if updater.update_weekly_report(args.name, args.this_week, args.next_week):
        logging.info("周报更新成功")
        return 0
    else:
        logging.error("周报更新失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
