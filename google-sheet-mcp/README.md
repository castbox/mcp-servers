# Google Sheets MCP 工具

这个项目提供了一个与Google Sheets和Google Docs进行交互，支持文档列表查询、文件下载和周报更新等功能。通过MCP协议，您可以在各种环境中方便地调用这些功能。

## 功能特点

- **文档列表查询**：列出所有可访问的Google文件、表格和文档
- **文档下载**：下载Google表格（支持Excel、CSV、JSON格式）和文档（支持DOCX、TXT格式）
- **周报更新**：查找和更新Google Sheets中的周报内容
- **MCP接口**：提供标准化的方法调用接口，可与各种客户端集成
- **安全认证**：使用Google服务账号进行安全认证

## 项目结构

项目采用模块化设计，包含以下主要文件：

- `main.py` - MCP服务主入口，注册和暴露所有方法
- `config.example.py` - 配置模板，用于创建实际的配置文件
- `google_sheets_connector.py` - Google Sheets连接器
- `download_docs.py` - 文档下载工具
- `list_accessible_docs.py` - 文档列表查询工具
- `weekly_report_updater.py` - 周报更新工具
- `requirements.txt` - 项目依赖文件
- `CREDENTIALS_GUIDE.md` - 凭证获取和配置指南

## 安装与配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置Google API凭证

请参考`CREDENTIALS_GUIDE.md`文件，完成以下步骤：

1. 在Google Cloud Console创建项目
2. 启用必要的API（Google Sheets API、Google Drive API、Google Docs API）
3. 创建服务账号并下载凭证文件
4. 将凭证文件命名为`credentials.json`并放在项目根目录
5. 与服务账号共享需要访问的Google文档

### 3. 创建配置文件

1. 复制`config.example.py`为`config.py`
2. 编辑`config.py`，设置您的表格ID、目标sheet索引和其他配置

## MCP工具使用方法

### 配置MCP服务

要在Windsurf或其他支持MCP的环境中使用此工具，需要在MCP配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "google_sheet_mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/google-sheet-mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

说明：
- `command`: 执行命令（这里使用`uv`，也可以使用`python`）
- `args`: 命令参数
  - `--directory`: 指定工作目录
  - `run`: uv命令的子命令
  - `main.py`: 要执行的Python文件


## 可用方法

### 文档列表查询

- `list_all_files(max_results=100)`: 列出所有可访问的文件
- `list_spreadsheets(max_results=100)`: 列出所有可访问的表格
- `list_documents(max_results=100)`: 列出所有可访问的文档

### 文档下载

- `download_spreadsheet(spreadsheet_id, format="excel", delay=1.5)`: 下载指定表格
- `download_document(document_id, format="docx", delay=1.5)`: 下载指定文档
- `download_all_files(format_sheet="excel", format_doc="docx", delay=1.5)`: 下载所有可访问的文件

### 周报更新

- `find_person(name, spreadsheet_id=SPREADSHEET_ID, sheet_index=TARGET_SHEET_INDEX)`: 查找指定人员
- `get_weekly_report(name, spreadsheet_id=SPREADSHEET_ID, sheet_index=TARGET_SHEET_INDEX)`: 获取周报内容
- `update_weekly_report(name, this_week, next_week, spreadsheet_id=SPREADSHEET_ID, sheet_index=TARGET_SHEET_INDEX)`: 更新周报
- `update_weekly_report_by_config(this_week, next_week)`: 根据配置更新周报

### 配置查询

- `get_config()`: 获取配置信息

### 帮助信息

- `readme()`: 显示帮助信息

## 使用示例


### 与大模型交互生成周报

通过与AI大模型的交互，可以实现更智能化的周报生成和更新。以下是一些常见的交互场景：

#### 场景一：基于Git提交记录生成周报

你可以要求大模型查看某个时间段内的Git提交记录，并将其整理成周报格式：

> “请查看过去一周内我的所有Git提交记录，并将其整理成周报格式。下周我计划完成用户认证模块的开发，请使用周报更新工具更新我的周报。”

大模型将会：
1. 查询指定时间段内的Git提交记录
2. 分析提交内容，并将其整理成有条理的周报格式
3. 调用MCP工具更新周报

#### 场景二：多渠道信息整合生成周报

你可以要求大模型整合多个来源的信息，如Git提交、项目管理工具的任务、日历上的会议等：

> “请查看我过去一周的Git提交记录、Jira上完成的任务以及日历上的会议内容，生成一份完整的周报，并更新到我的周报表格中。”

大模型将会整合多渠道信息，生成更全面的周报内容。

#### 场景三：自动下载和分析文档

你可以要求大模型下载特定的Google表格或文档，并进行分析：

> “请列出我可访问的所有表格，然后下载其中标题包含“项目进度”的表格，并分析其中的数据，生成一份项目进度报告。”

大模型将会：
1. 调用`list_spreadsheets()`列出所有表格
2. 过滤出相关表格
3. 使用`download_spreadsheet()`下载目标表格
4. 分析数据并生成报告


## 安全注意事项

- **不要**将`credentials.json`和`config.py`提交到公共代码库
- 建议在`.gitignore`中添加这些文件
- 定期轮换服务账号密钥，特别是在怀疑凭证可能泄露时
- 仅授予服务账号所需的最小权限

## 故障排除

### 常见问题

1. **403 Forbidden错误**：检查API是否启用、文档是否共享给服务账号
2. **身份验证失败**：确认凭证文件路径和内容正确
3. **找不到人员**：检查姓名和表格配置是否正确

### 日志

工具会在控制台输出详细日志，帮助诊断问题。
