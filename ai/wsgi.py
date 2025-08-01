import sys
import os

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_1 import app

if __name__ == "__main__":
    app.run() 