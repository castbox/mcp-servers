# MCP Server Pool

这是一个 MCP（Model-Context-Protocol）Server 仓库，包含多种实用的 MCP 服务实现和从零开始的开发教程。

## 项目结构

```
mcp-servers/
├── git-options/        # Git 操作相关的 MCP 服务
├── google-sheet-mcp/   # Google Sheets 和文档操作相关的 MCP 服务
├── jk-option/          # Jenkins 操作相关的 MCP 服务
├── file-option/        # 文件操作相关的 MCP 服务
├── tutorial/           # 从 0 到 1 的 MCP 开发教程
└── ...                 # 其他 MCP 服务
```

## 服务列表

### Git 操作服务

位于 `git-options/` 目录，提供 Git 相关操作的 MCP 服务，包括：

- 初始化仓库
- 添加/提交更改
- 分支管理
- 远程仓库操作
- 凭证管理
- 用户配置

### Google Sheets MCP 工具

位于 `google-sheet-mcp/` 目录，提供与 Google Sheets 和 Google Docs 交互的 MCP 服务，包括：

- 文档列表查询：列出所有可访问的 Google 文件、表格和文档
- 文档下载：下载 Google 表格（支持 Excel、CSV、JSON 格式）和文档（支持 DOCX、TXT 格式）
- 周报更新：查找和更新 Google Sheets 中的周报内容
- 安全认证：使用 Google 服务账号进行安全认证

### Jenkins 操作工具

位于 `jk-option/` 目录，提供 Jenkins 服务器的各种操作功能，包括：

- 获取所有 Jenkins 项目列表
- 获取指定项目的构建参数
- 根据传入的参数触发构建
- 获取构建状态
- 终止指定构建
- 项目别名处理功能（例如将完整项目名映射为简短别名）

### 文件操作服务

位于 `file-option/` 目录，提供全面的文件系统操作功能，旨在解决Cherry Studio等对话软件在文件操作方面的局限性：

- 文件的读取与写入
- 文件的创建与删除
- 文件的复制与移动
- 目录的创建与删除
- 文件权限的修改
- 文件信息的获取

**特别注意**：使用文件操作服务时，请谨慎执行删除操作，因为这些操作是真实有效的，一旦执行将无法恢复。

## 从 0 到 1 的 MCP 开发教程

位于 `tutorial/` 目录，这是一个完整的教程，指导您如何从零开始开发 MCP 服务：

### 教程内容

1. **基础概念**

   - MCP 架构介绍
   - 服务设计原则
   - 开发环境搭建

2. **创建第一个 MCP 服务**

   - 项目结构设置
   - 基本框架编写
   - 工具函数定义

## 开发指南

### 环境要求

- Python 3.10+
- FastMCP 库

## 模块提交

为了保持仓库的一致性和可维护性，请遵循以下规范：

### 目录结构规范

1. **每个模块必须创建独立目录**

   - 每个 MCP 服务模块必须创建一个独立的目录
   - 目录名应使用小写字母和连字符，例如：`weather-service`、`text-translator`

2. **不需要包含项目基础框架文件**

   - 不要提交项目的基础框架文件
   - 专注于模块的具体实现

## 贡献指南

欢迎贡献新的 MCP 服务或改进现有服务！

## 许可证

[MIT License](LICENSE)