from flask import Flask, request, jsonify, render_template
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import os

app = Flask(__name__)

# 环境检测
IS_PYTHONANYWHERE = 'PYTHONANYWHERE_DOMAIN' in os.environ

# 生产环境配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

model = "flux-schnell"

# 只在非PythonAnywhere环境导入Dashscope
if not IS_PYTHONANYWHERE:
    from dashscope import ImageSynthesis
else:
    # PythonAnywhere上的替代方案
    print("Running on PythonAnywhere - Using mock image generation")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        user_input = request.json.get('prompt', '')
        if not user_input:
            return jsonify({'error': '请输入图片描述'}), 400
        
        if len(user_input) > 500:
            return jsonify({'error': '图片描述过长，请控制在500字符以内'}), 400
        
        # PythonAnywhere环境使用模拟响应
        if IS_PYTHONANYWHERE:
            mock_image_path = '/static/placeholder.png'
            return jsonify({
                'success': True,
                'images': [mock_image_path],
                'usage': {'image_count': 1},
                'note': 'Running on PythonAnywhere (free tier) - using mock image'
            })
        
        # 正常调用Dashscope API
        rsp = ImageSynthesis.call(
            model=model,
            prompt=user_input,
            size='1024*1024'
        )
        
        if rsp.status_code == HTTPStatus.OK:
            image_urls = []
            for result in rsp.output.results:
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                os.makedirs('static', exist_ok=True)
                file_path = f'static/{file_name}'
                
                # 下载图片（添加超时和错误处理）
                try:
                    response = requests.get(result.url, timeout=10)
                    response.raise_for_status()
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    image_urls.append(f'/static/{file_name}')
                except requests.RequestException as e:
                    print(f"下载图片失败: {e}")
                    continue
            
            if not image_urls:
                return jsonify({'error': '所有图片下载失败'}), 500
                
            return jsonify({
                'success': True,
                'images': image_urls,
                'usage': rsp.usage
            })
        else:
            return jsonify({
                'error': f'生成失败: {rsp.message}',
                'status_code': rsp.status_code
            }), 400
            
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port, debug=not IS_PYTHONANYWHERE)