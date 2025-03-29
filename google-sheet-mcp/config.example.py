"""配置模块，管理所有配置信息
此文件为配置示例，请复制为config.py并填入您的实际配置信息
"""

# Google API 认证配置
# SCOPES 定义API权限范围
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',  # 表格访问权限
    'https://www.googleapis.com/auth/drive.readonly',  # Drive读取权限
    'https://www.googleapis.com/auth/drive.metadata.readonly',  # Drive元数据读取权限
    'https://www.googleapis.com/auth/documents.readonly'  # Google Docs API读取权限
]
# 服务账号凭证文件路径，请参考CREDENTIALS_GUIDE.md生成此文件
SERVICE_ACCOUNT_FILE = 'credentials.json'

# 表格基本配置
# Google Sheets表格的ID，可以从URL中获取
# 例如：https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'
# 目标sheet页的索引，从0开始计数，例如第1个sheet的索引为0
TARGET_SHEET_INDEX = 0

# 周报表单配置
# 姓名所在的列（A列=0, B列=1, 以此类推）
NAME_COLUMN = 0  # A列
# 需要查找的人员姓名
TARGET_NAME = '您的姓名'  # 需要替换为实际要查找的姓名
# 本周工作内容所在的列
THIS_WEEK_COLUMN = 3  # D列
# 下周工作计划所在的列
NEXT_WEEK_COLUMN = 4  # E列
# 本周工作内容示例
THIS_WEEK_CONTENT = ''
# 下周工作计划示例
NEXT_WEEK_CONTENT = ''

# 下载文件配置
# 下载文件保存的目录
DOWNLOAD_DIR = 'downloads'
# 下载文件时的API请求间隔（秒），避免触发限流
RATE_LIMIT_DELAY = 1.5
