from mcp.server.fastmcp import FastMCP
import subprocess
from typing import List, Optional

mcp = FastMCP("git_option")

def run_git_command(command: List[str], cwd: Optional[str] = None) -> str:
    try:
        result = subprocess.run(
            ['git'] + command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"错误: {e.stderr}"

@mcp.tool()
async def git_init(path: str) -> str:
    """初始化Git仓库"""
    return run_git_command(['init'], path)

@mcp.tool()
async def git_status(path: str) -> str:
    """获取Git仓库状态"""
    return run_git_command(['status'], path)

@mcp.tool()
async def git_add(path: str, files: str) -> str:
    """添加文件到暂存区"""
    return run_git_command(['add', files], path)

@mcp.tool()
async def git_commit(path: str, message: str) -> str:
    """提交更改"""
    return run_git_command(['commit', '-m', message], path)

@mcp.tool()
async def git_push(path: str, remote: str = 'origin', branch: str = 'main') -> str:
    """推送更改到远程仓库"""
    return run_git_command(['push', remote, branch], path)

@mcp.tool()
async def git_pull(path: str, remote: str = 'origin', branch: str = 'main') -> str:
    """从远程仓库拉取更改"""
    return run_git_command(['pull', remote, branch], path)

@mcp.tool()
async def git_branch(path: str) -> str:
    """列出所有分支"""
    return run_git_command(['branch'], path)

@mcp.tool()
async def git_checkout(path: str, branch: str) -> str:
    """切换分支"""
    return run_git_command(['checkout', branch], path)

@mcp.tool()
async def git_log(path: str, num_entries: int = 5) -> str:
    """查看提交历史"""
    return run_git_command(['log', f'-n{num_entries}', '--oneline'], path)

if __name__ == "__main__":
    mcp.run(transport='stdio')