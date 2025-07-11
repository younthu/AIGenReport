#!/usr/bin/env python3
"""
LangServe启动脚本 - 美国本科留学选校报告生成服务
使用langserve命令行工具启动服务
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """启动LangServe服务"""
    
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent.absolute()
    
    # 设置工作目录
    os.chdir(current_dir)
    
    # 检查必要的文件
    workflow_file = current_dir / "university_selection_workflow.py"
    if not workflow_file.exists():
        print(f"错误: 找不到workflow文件 {workflow_file}")
        sys.exit(1)
    
    # 设置环境变量
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    
    # 从环境变量获取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print("启动美国本科留学选校报告生成服务...")
    print(f"工作目录: {current_dir}")
    print(f"服务地址: http://{host}:{port}")
    print(f"API文档: http://{host}:{port}/docs")
    print(f"健康检查: http://{host}:{port}/health")
    print("\n按 Ctrl+C 停止服务\n")
    
    try:
        # 使用langserve启动服务
        cmd = [
            "langserve", "run",
            "--host", host,
            "--port", str(port),
            "university_selection_workflow:UniversitySelectionWorkflow"
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"服务启动失败: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("错误: 找不到langserve命令")
        print("请先安装langserve: pip install langserve")
        sys.exit(1)


if __name__ == "__main__":
    main() 