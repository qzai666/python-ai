from flask import Flask, request, jsonify, render_template, send_from_directory
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import os
import time
from datetime import datetime

app = Flask(__name__)

# ======================
# 配置区（根据实际修改）
# ======================
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-123'),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
    STATIC_FOLDER='static',
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg'},
)

# 模型配置
MODEL_CONFIG = {
    "model": "wanx-v1",  # 默认模型
    "size": "1024*1024"
}

# ======================
# 核心功能
# ======================

def is_pythonanywhere():
    """检测是否运行在PythonAnywhere"""
    return 'PYTHONANYWHERE_DOMAIN' in os.environ

def can_access_internet():
    """检查是否能访问外部API（付费账户返回True）"""
    if not is_pythonanywhere():
        return True
    
    try:
        test_url = "https://dashscope.aliyuncs.com"
        response = requests.head(test_url, timeout=3)
        return response.status_code == 200
    except:
        return False

def generate_filename():
    """生成唯一文件名"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"ai_image_{timestamp}.png"

def save_image_from_url(url, filename):
    """保存图片到本地static目录"""
    os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)
    filepath = os.path.join(app.config['STATIC_FOLDER'], filename)
    
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filepath
    except Exception as e:
        app.logger.error(f"图片保存失败: {str(e)}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return None

# ======================
# 路由部分
# ======================

@app.route('/')
def index():
    return render_template('index.html', 
                         is_pa=is_pythonanywhere(),
                         is_pro=can_access_internet())

@app.route('/generate_image', methods=['POST'])
def handle_generation():
    start_time = time.time()
    
    # 1. 验证输入
    user_input = request.json.get('prompt', '').strip()
    if not user_input:
        return jsonify({'success': False, 'error': '请输入图片描述'}), 400
    
    if len(user_input) > 500:
        return jsonify({'success': False, 'error': '描述过长（最多500字符）'}), 400

    # 2. 检查运行环境
    use_mock = is_pythonanywhere() and not can_access_internet()
    
    if use_mock:
        return jsonify({
            'success': True,
            'images': ['/static/placeholder.png'],
            'usage': {'model': 'mock', 'count': 1},
            'note': 'PythonAnywhere免费账户使用模拟图片',
            'processing_time': round(time.time() - start_time, 1)
        })

    # 3. 调用真实API（付费账户路径）
    try:
        from dashscope import ImageSynthesis  # 延迟导入
        
        rsp = ImageSynthesis.call(
            model=MODEL_CONFIG['model'],
            prompt=user_input,
            size=MODEL_CONFIG['size']
        )
        
        if rsp.status_code != HTTPStatus.OK:
            return jsonify({
                'success': False,
                'error': rsp.message,
                'status_code': rsp.status_code
            }), 400

        # 4. 处理生成的图片
        image_urls = []
        for idx, result in enumerate(rsp.output.results):
            filename = f"gen_{idx}_{generate_filename()}"
            saved_path = save_image_from_url(result.url, filename)
            
            if saved_path:
                image_urls.append(f'/static/{filename}')

        if not image_urls:
            return jsonify({
                'success': False,
                'error': '所有图片保存失败'
            }), 500

        return jsonify({
            'success': True,
            'images': image_urls,
            'usage': dict(rsp.usage),
            'processing_time': round(time.time() - start_time, 1)
        })

    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Dashscope SDK不可用'
        }), 500
    except Exception as e:
        app.logger.error(f"生成失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'生成失败: {str(e)}'
        }), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """静态文件路由"""
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

# ======================
# 错误处理
# ======================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

# ======================
# 启动配置
# ======================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=not is_pythonanywhere()
    )