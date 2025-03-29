#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件操作模块：提供查看、创建和编辑本地文件的功能
"""

import os
import json
import shutil
import datetime
import stat
from pathlib import Path
from typing import Dict, List, Any, Optional, Union


class FileOption:
    """文件操作类，提供文件的基本操作功能"""
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> str:
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            encoding: 文件编码，默认utf-8
            
        Returns:
            str: 文件内容
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            return f"读取文件失败: {str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        写入文件内容
        
        Args:
            file_path: 文件路径
            content: 文件内容
            encoding: 文件编码，默认utf-8
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            return {
                "success": True,
                "message": f"文件写入成功: {file_path}",
                "path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"文件写入失败: {str(e)}",
                "path": file_path
            }
    
    @staticmethod
    def append_file(file_path: str, content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        追加内容到文件
        
        Args:
            file_path: 文件路径
            content: 要追加的内容
            encoding: 文件编码，默认utf-8
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)
            
            return {
                "success": True,
                "message": f"内容追加成功: {file_path}",
                "path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"内容追加失败: {str(e)}",
                "path": file_path
            }
    
    @staticmethod
    def edit_file(file_path: str, old_content: str, new_content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        编辑文件内容（替换指定内容）
        
        Args:
            file_path: 文件路径
            old_content: 要替换的内容
            new_content: 新内容
            encoding: 文件编码，默认utf-8
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"文件不存在: {file_path}",
                    "path": file_path
                }
                
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                
            # 替换内容
            if old_content not in content:
                return {
                    "success": False,
                    "message": f"未找到要替换的内容",
                    "path": file_path
                }
                
            new_content_full = content.replace(old_content, new_content)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(new_content_full)
                
            return {
                "success": True,
                "message": f"文件编辑成功: {file_path}",
                "path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"文件编辑失败: {str(e)}",
                "path": file_path
            }
    
    @staticmethod
    def list_directory(directory_path: str) -> Dict[str, Any]:
        """
        列出目录内容
        
        Args:
            directory_path: 目录路径
            
        Returns:
            Dict[str, Any]: 目录内容信息
        """
        try:
            if not os.path.exists(directory_path):
                return {
                    "success": False,
                    "message": f"目录不存在: {directory_path}",
                    "path": directory_path
                }
                
            if not os.path.isdir(directory_path):
                return {
                    "success": False,
                    "message": f"路径不是目录: {directory_path}",
                    "path": directory_path
                }
                
            items = []
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                item_stat = os.stat(item_path)
                
                # 获取文件/目录信息
                is_dir = os.path.isdir(item_path)
                size = item_stat.st_size if not is_dir else None
                modified_time = datetime.datetime.fromtimestamp(item_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                # 获取权限信息
                permissions = stat.filemode(item_stat.st_mode)
                
                items.append({
                    "name": item,
                    "path": item_path,
                    "is_directory": is_dir,
                    "size": size,
                    "modified_time": modified_time,
                    "permissions": permissions
                })
                
            return {
                "success": True,
                "message": f"目录内容获取成功: {directory_path}",
                "path": directory_path,
                "items": items,
                "total_items": len(items)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"获取目录内容失败: {str(e)}",
                "path": directory_path
            }
    
    @staticmethod
    def copy_file(source_path: str, destination_path: str) -> Dict[str, Any]:
        """
        复制文件
        
        Args:
            source_path: 源文件路径
            destination_path: 目标文件路径
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            if not os.path.exists(source_path):
                return {
                    "success": False,
                    "message": f"源文件不存在: {source_path}",
                    "source": source_path,
                    "destination": destination_path
                }
                
            # 确保目标目录存在
            os.makedirs(os.path.dirname(os.path.abspath(destination_path)), exist_ok=True)
            
            # 复制文件
            shutil.copy2(source_path, destination_path)
            
            return {
                "success": True,
                "message": f"文件复制成功: {source_path} -> {destination_path}",
                "source": source_path,
                "destination": destination_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"文件复制失败: {str(e)}",
                "source": source_path,
                "destination": destination_path
            }
    
    @staticmethod
    def move_file(source_path: str, destination_path: str) -> Dict[str, Any]:
        """
        移动文件
        
        Args:
            source_path: 源文件路径
            destination_path: 目标文件路径
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            if not os.path.exists(source_path):
                return {
                    "success": False,
                    "message": f"源文件不存在: {source_path}",
                    "source": source_path,
                    "destination": destination_path
                }
                
            # 确保目标目录存在
            os.makedirs(os.path.dirname(os.path.abspath(destination_path)), exist_ok=True)
            
            # 移动文件
            shutil.move(source_path, destination_path)
            
            return {
                "success": True,
                "message": f"文件移动成功: {source_path} -> {destination_path}",
                "source": source_path,
                "destination": destination_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"文件移动失败: {str(e)}",
                "source": source_path,
                "destination": destination_path
            }
    
    @staticmethod
    def delete_file(file_path: str) -> Dict[str, Any]:
        """
        删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"文件不存在: {file_path}",
                    "path": file_path
                }
                
            if os.path.isdir(file_path):
                return {
                    "success": False,
                    "message": f"路径是目录而非文件: {file_path}",
                    "path": file_path
                }
                
            # 删除文件
            os.remove(file_path)
            
            return {
                "success": True,
                "message": f"文件删除成功: {file_path}",
                "path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"文件删除失败: {str(e)}",
                "path": file_path
            }
    
    @staticmethod
    def create_directory(directory_path: str) -> Dict[str, Any]:
        """
        创建目录
        
        Args:
            directory_path: 目录路径
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            if os.path.exists(directory_path):
                if os.path.isdir(directory_path):
                    return {
                        "success": True,
                        "message": f"目录已存在: {directory_path}",
                        "path": directory_path
                    }
                else:
                    return {
                        "success": False,
                        "message": f"路径已存在但不是目录: {directory_path}",
                        "path": directory_path
                    }
            
            # 创建目录
            os.makedirs(directory_path, exist_ok=True)
            
            return {
                "success": True,
                "message": f"目录创建成功: {directory_path}",
                "path": directory_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"目录创建失败: {str(e)}",
                "path": directory_path
            }
    
    @staticmethod
    def delete_directory(directory_path: str, recursive: bool = False) -> Dict[str, Any]:
        """
        删除目录
        
        Args:
            directory_path: 目录路径
            recursive: 是否递归删除，默认False
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            if not os.path.exists(directory_path):
                return {
                    "success": False,
                    "message": f"目录不存在: {directory_path}",
                    "path": directory_path
                }
                
            if not os.path.isdir(directory_path):
                return {
                    "success": False,
                    "message": f"路径不是目录: {directory_path}",
                    "path": directory_path
                }
            
            # 检查目录是否为空
            if not recursive and len(os.listdir(directory_path)) > 0:
                return {
                    "success": False,
                    "message": f"目录不为空，无法删除: {directory_path}",
                    "path": directory_path
                }
            
            # 删除目录
            if recursive:
                shutil.rmtree(directory_path)
            else:
                os.rmdir(directory_path)
            
            return {
                "success": True,
                "message": f"目录删除成功: {directory_path}",
                "path": directory_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"目录删除失败: {str(e)}",
                "path": directory_path
            }
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 文件信息
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"文件不存在: {file_path}",
                    "path": file_path
                }
            
            stat_info = os.stat(file_path)
            file_info = {
                "path": file_path,
                "name": os.path.basename(file_path),
                "size": stat_info.st_size,
                "is_directory": os.path.isdir(file_path),
                "created_time": datetime.datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                "modified_time": datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                "accessed_time": datetime.datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
                "permissions": stat.filemode(stat_info.st_mode),
                "permissions_octal": oct(stat_info.st_mode)[-3:],
            }
            
            # 获取文件类型
            if os.path.isdir(file_path):
                file_type = "directory"
            elif os.path.islink(file_path):
                file_type = "symlink"
            elif os.path.isfile(file_path):
                # 尝试根据扩展名判断文件类型
                extension = os.path.splitext(file_path)[1].lower()
                if extension in [".txt", ".md", ".log", ".csv"]:
                    file_type = "text"
                elif extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
                    file_type = "image"
                elif extension in [".mp4", ".avi", ".mov", ".mkv"]:
                    file_type = "video"
                elif extension in [".mp3", ".wav", ".flac", ".aac"]:
                    file_type = "audio"
                elif extension in [".py", ".js", ".java", ".c", ".cpp", ".go", ".rb"]:
                    file_type = "code"
                elif extension in [".zip", ".tar", ".gz", ".rar", ".7z"]:
                    file_type = "archive"
                elif extension in [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]:
                    file_type = "document"
                else:
                    file_type = "file"
            else:
                file_type = "unknown"
                
            file_info["type"] = file_type
            
            return {
                "success": True,
                "message": f"文件信息获取成功: {file_path}",
                "path": file_path,
                "info": file_info
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"获取文件信息失败: {str(e)}",
                "path": file_path
            }
    
    @staticmethod
    def change_file_permissions(file_path: str, mode: int) -> Dict[str, Any]:
        """
        修改文件权限
        
        Args:
            file_path: 文件路径
            mode: 权限模式，如0o755
            
        Returns:
            Dict[str, Any]: 操作结果
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"文件不存在: {file_path}",
                    "path": file_path
                }
            
            # 修改文件权限
            os.chmod(file_path, mode)
            
            # 获取新的权限信息
            new_permissions = stat.filemode(os.stat(file_path).st_mode)
            new_permissions_octal = oct(os.stat(file_path).st_mode)[-3:]
            
            return {
                "success": True,
                "message": f"文件权限修改成功: {file_path}",
                "path": file_path,
                "permissions": new_permissions,
                "permissions_octal": new_permissions_octal
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"文件权限修改失败: {str(e)}",
                "path": file_path
            }


def main():
    """测试文件操作功能"""
    # 测试目录
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")
    
    # 创建测试目录
    print("\n1. 创建测试目录")
    result = FileOption.create_directory(test_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 创建测试文件
    test_file = os.path.join(test_dir, "test.txt")
    print("\n2. 创建测试文件")
    result = FileOption.write_file(test_file, "这是一个测试文件\n包含多行内容\n用于测试文件操作功能")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 读取文件内容
    print("\n3. 读取文件内容")
    content = FileOption.read_file(test_file)
    print(content)
    
    # 追加文件内容
    print("\n4. 追加文件内容")
    result = FileOption.append_file(test_file, "\n这是追加的内容")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 再次读取文件内容
    print("\n5. 再次读取文件内容")
    content = FileOption.read_file(test_file)
    print(content)
    
    # 编辑文件内容
    print("\n6. 编辑文件内容")
    result = FileOption.edit_file(test_file, "这是一个测试文件", "这是一个已修改的测试文件")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 再次读取文件内容
    print("\n7. 再次读取文件内容")
    content = FileOption.read_file(test_file)
    print(content)
    
    # 获取文件信息
    print("\n8. 获取文件信息")
    result = FileOption.get_file_info(test_file)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 列出目录内容
    print("\n9. 列出目录内容")
    result = FileOption.list_directory(test_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 复制文件
    test_file_copy = os.path.join(test_dir, "test_copy.txt")
    print("\n10. 复制文件")
    result = FileOption.copy_file(test_file, test_file_copy)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 列出目录内容
    print("\n11. 列出目录内容")
    result = FileOption.list_directory(test_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 移动文件
    test_file_moved = os.path.join(test_dir, "test_moved.txt")
    print("\n12. 移动文件")
    result = FileOption.move_file(test_file_copy, test_file_moved)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 列出目录内容
    print("\n13. 列出目录内容")
    result = FileOption.list_directory(test_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 删除文件
    print("\n14. 删除文件")
    result = FileOption.delete_file(test_file_moved)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 列出目录内容
    print("\n15. 列出目录内容")
    result = FileOption.list_directory(test_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 递归删除目录
    print("\n16. 递归删除目录")
    result = FileOption.delete_directory(test_dir, recursive=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n测试完成！")


if __name__ == "__main__":
    main()
