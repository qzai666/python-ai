import sys
import os

# 添加项目路径到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# 设置环境变量（请替换为你的实际 API 密钥）
os.environ['DASHSCOPE_API_KEY'] = '你的实际API密钥'

# 导入应用
from ai.ai_1 import app as application

if __name__ == "__main__":
    application.run() 