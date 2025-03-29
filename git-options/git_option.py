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

@mcp.tool()
async def git_remote_list(path: str) -> str:
    """列出所有远程仓库"""
    return run_git_command(['remote', '-v'], path)

@mcp.tool()
async def git_remote_add(path: str, name: str, url: str) -> str:
    """添加远程仓库"""
    return run_git_command(['remote', 'add', name, url], path)

@mcp.tool()
async def git_remote_set_url(path: str, name: str, url: str) -> str:
    """修改远程仓库地址"""
    return run_git_command(['remote', 'set-url', name, url], path)

@mcp.tool()
async def git_remote_remove(path: str, name: str) -> str:
    """删除远程仓库"""
    return run_git_command(['remote', 'remove', name], path)

@mcp.tool()
async def git_credential_store(path: str, username: str, password: str) -> str:
    """设置Git凭证存储（用户名和密码/令牌）"""
    # 设置凭证存储模式为缓存
    run_git_command(['config', '--global', 'credential.helper', 'store'], path)
    
    # 创建一个临时脚本来输入凭证
    import os
    import tempfile
    
    fd, temp_path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(f"protocol=https\nhost=github.com\nusername={username}\npassword={password}\n")
        
        # 使用git credential approve命令存储凭证
        result = subprocess.run(
            ['git', 'credential', 'approve'],
            input=open(temp_path, 'r').read(),
            text=True,
            shell=True,
            capture_output=True
        )
        
        if result.returncode == 0:
            return "凭证已成功存储"
        else:
            return f"存储凭证时出错: {result.stderr}"
    finally:
        os.unlink(temp_path)

@mcp.tool()
async def git_config_user(path: str, name: str, email: str) -> str:
    """设置Git用户名和邮箱"""
    name_result = run_git_command(['config', '--global', 'user.name', name], path)
    email_result = run_git_command(['config', '--global', 'user.email', email], path)
    return f"用户名设置: {name_result}\n邮箱设置: {email_result}"

@mcp.tool()
async def git_log(path: str, num_entries: int = 5) -> str:
    """查看提交历史"""
    return run_git_command(['log', f'-n{num_entries}', '--oneline'], path)

@mcp.tool()
async def git_log_advanced(path: str, author: str = None, since: str = None, until: str = None, 
                         grep: str = None, format: str = "%h %ad %s", date_format: str = "short", 
                         num_entries: int = None) -> str:
    """高级查看提交历史
    
    参数:
        path: 仓库路径
        author: 作者名称或邮箱，例如 "yuzhou"
        since: 开始时间，例如 "1 week ago", "2023-01-01"
        until: 结束时间，例如 "yesterday", "2023-12-31"
        grep: 在提交信息中搜索的关键词
        format: 输出格式，默认为 "%h %ad %s"（哈希值、日期、提交信息）
        date_format: 日期格式，可选值包括 "short", "relative", "iso", "local" 等
        num_entries: 显示的条目数量，不设置则显示全部
    """
    command = ['log']
    
    if author:
        command.append(f'--author="{author}"')
    
    if since:
        command.append(f'--since="{since}"')
    
    if until:
        command.append(f'--until="{until}"')
    
    if grep:
        command.append(f'--grep="{grep}"')
    
    if format:
        command.append(f'--pretty=format:"{format}"')
    
    if date_format:
        command.append(f'--date={date_format}')
    
    if num_entries:
        command.append(f'-n{num_entries}')
    
    return run_git_command(command, path)

@mcp.tool()
async def git_diff(path: str, commit1: str = None, commit2: str = None, file_path: str = None, cached: bool = False) -> str:
    """查看差异
    
    参数:
        path: 仓库路径
        commit1: 第一个提交或分支，不指定则与当前工作区比较
        commit2: 第二个提交或分支，不指定则与第一个提交比较
        file_path: 指定文件路径，不指定则比较所有文件
        cached: 是否比较暂存区和最新提交，默认为False
    
    返回:
        str: diff结果文本
    """
    command = ['diff']
    
    # 比较暂存区和最新提交
    if cached:
        command.append('--cached')
    
    # 指定提交或分支进行比较
    if commit1 and commit2:
        command.append(f'{commit1}..{commit2}')
    elif commit1:
        command.append(commit1)
    
    # 指定文件路径
    if file_path:
        command.append('--')
        command.append(file_path)
    
    # 添加颜色输出
    command.append('--color')
    
    return run_git_command(command, path)
    
if __name__ == "__main__":
    mcp.run(transport='stdio')