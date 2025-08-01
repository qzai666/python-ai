# AI 图片生成器部署指南

## 环境要求
- Python 3.7+
- Flask
- dashscope
- requests

## 部署方案

### 方案一：PythonAnywhere（推荐，免费）

1. **注册 PythonAnywhere 账号**
   - 访问 https://www.pythonanywhere.com
   - 注册免费账号

2. **上传代码**
   ```bash
   # 在 PythonAnywhere 的 Bash 控制台中
   git clone <你的代码仓库地址>
   # 或者手动上传文件
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **设置环境变量**
   ```bash
   export DASHSCOPE_API_KEY="你的API密钥"
   ```

5. **配置 Web 应用**
   - 进入 Web 页面
   - 添加新的 Web 应用
   - 选择 Flask
   - 设置源代码目录为你的项目目录
   - 设置 WSGI 文件路径为 `ai/wsgi.py`

6. **配置域名**
   - 在 Web 应用设置中配置你的域名
   - 或者使用 PythonAnywhere 提供的免费域名

### 方案二：Vercel（免费，简单）

1. **准备 vercel.json**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "ai/wsgi.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "ai/wsgi.py"
       }
     ]
   }
   ```

2. **部署到 Vercel**
   ```bash
   npm i -g vercel
   vercel
   ```

### 方案三：Heroku（付费）

1. **创建 Procfile**
   ```
   web: gunicorn ai.wsgi:app
   ```

2. **安装 gunicorn**
   ```bash
   pip install gunicorn
   ```

3. **部署到 Heroku**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### 方案四：自建服务器（VPS）

1. **安装 Nginx**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **配置 Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static {
           alias /path/to/your/app/static;
       }
   }
   ```

3. **使用 Gunicorn 运行**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 127.0.0.1:5000 ai.wsgi:app
   ```

## 环境变量设置

确保设置以下环境变量：
- `DASHSCOPE_API_KEY`: 你的阿里云 API 密钥
- `SECRET_KEY`: Flask 密钥（可选）

## 注意事项

1. **API 密钥安全**
   - 不要在代码中硬编码 API 密钥
   - 使用环境变量存储敏感信息

2. **文件存储**
   - 生成的图片会保存在 `static/` 目录
   - 考虑使用云存储服务（如阿里云 OSS）

3. **性能优化**
   - 添加图片缓存
   - 限制并发请求
   - 添加请求频率限制

4. **监控和日志**
   - 添加错误日志记录
   - 监控 API 调用次数和费用

## 域名配置

1. **购买域名**（如阿里云、腾讯云）
2. **DNS 解析**指向你的服务器 IP
3. **SSL 证书**（推荐使用 Let's Encrypt）

## 常见问题

1. **API 调用失败**
   - 检查 API 密钥是否正确
   - 确认网络连接正常
   - 查看服务器日志

2. **图片无法显示**
   - 检查 static 目录权限
   - 确认 Nginx 配置正确

3. **性能问题**
   - 考虑使用 CDN
   - 优化图片大小
   - 添加缓存机制 