# Jenkins 操作工具 (jk_option)

这是一个基于 python-jenkins 库的 Jenkins 操作工具，提供了一系列便捷的 Jenkins 服务器操作功能，并通过 MCP 框架暴露为可调用的工具。

## 功能特性

1. 连接 Jenkins 服务器
2. 获取所有项目列表
3. 获取指定项目的构建参数
4. 根据传入的参数触发构建
5. 获取构建状态
6. 终止指定构建
7. 项目别名处理功能（例如将"GoodsSortPuzzle"映射为"GSP"）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

在 `jk_option.py` 文件中，您需要配置以下全局变量：

```python
# 全局定义 Jenkins 服务器地址、用户名和密码
JENKINS_URL = "http://your-jenkins-server:8080/"  # 请替换为您的 Jenkins 服务器地址
JENKINS_USERNAME = "your-username"  # 请替换为您的 Jenkins 用户名
JENKINS_PASSWORD = "your-password"  # 请替换为您的 Jenkins 密码
```

## 项目别名配置

您可以在 `PROJECT_ALIASES` 字典中配置项目别名，例如：

```python
PROJECT_ALIASES = {
    "GSP_Pgyer": "GoodsSort_Puzzle",
    "GSP_GP": "GoodsSort_Puzzle_Release",
    "GSP_IOS": "GoodsSort_Puzzle_IOS",
    # 可以添加更多的别名映射
}
```

这样您就可以使用别名来引用项目，而不需要记住完整的项目名称。

## MCP 配置

在 MCP 配置文件中添加以下配置：

```json
{
    "mcpServers": {
      "jk_option":{
        "command":"uv",
        "args":[
            "--directory",
            "文件夹所在路径[示例：/Users/xxx/mcp/jenkins]",
            "run",
            "jk_option.py"
        ]
      }
    }
}
```

## MCP 工具使用

本工具通过 MCP 框架暴露了以下功能：

1. `get_all_jobs`: 获取所有 Jenkins 项目
2. `get_job_parameters`: 获取指定项目的构建参数
3. `build_job`: 根据指定的参数进行项目构建
4. `get_build_status`: 获取指定构建的状态
5. `stop_build`: 终止指定构建

## 使用示例

### 获取所有项目

```python
from mcp.client import MCPClient

client = MCPClient()
jobs = client.call("jk_option", "get_all_jobs")
print(jobs)
```

### 获取项目参数

```python
params = client.call("jk_option", "get_job_parameters", job_name="GSP_Pgyer")
print(params)
```

### 触发构建

```python
build_number = client.call("jk_option", "build_job", 
                          job_name="GSP_GP", 
                          parameters={"Branch": "develop", "ProjectVersion": "1.0.0", "BuildEnv": "Release"})
print(f"构建编号: {build_number}")
```

### 获取构建状态

```python
status = client.call("jk_option", "get_build_status", job_name="GSP_GP", build_number=123)
print(status)
```

### 终止构建

```python
result = client.call("jk_option", "stop_build", job_name="GSP_GP", build_number=123)
print(result)
```

## 注意事项

1. 确保您的 Jenkins 服务器可以从运行此工具的机器上访问
2. 确保提供的用户名和密码有足够的权限执行相应操作
3. 如果遇到 python-jenkins 库的导入问题，请参考代码中的灵活导入机制

## 故障排除

如果遇到 "module 'jenkins' has no attribute 'Jenkins'" 错误，这可能是因为存在另一个同名的 jenkins 模块导致冲突。解决方案是通过创建一个灵活的导入机制，首先尝试从 site-packages 中直接导入 jenkins 模块，如果失败则提供一个基于 requests 的备选实现。
