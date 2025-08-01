# AI 图片生成器

一个基于 Flask 的 AI 图片生成 Web 应用，使用阿里云 DashScope API 生成图片。

## 功能特性

- 🎨 根据文字描述生成图片
- 🌐 简洁美观的 Web 界面
- ⚡ 实时生成和显示
- 📱 响应式设计，支持移动端

## 技术栈

- **后端**: Flask, Python
- **前端**: HTML, CSS, JavaScript
- **AI API**: 阿里云 DashScope

## 快速开始

### 本地运行

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **设置环境变量**
   ```bash
   export DASHSCOPE_API_KEY="你的API密钥"
   ```

3. **启动应用**
   ```bash
   python app.py
   ```

4. **访问应用**
   打开浏览器访问: http://localhost:3000

### 部署到服务器

1. **上传代码到服务器**
2. **安装依赖**: `pip install -r requirements.txt`
3. **设置环境变量**: `DASHSCOPE_API_KEY`
4. **配置 WSGI**: 使用 `wsgi.py`
5. **启动服务**: `python wsgi.py`

## 项目结构

```
.
├── app.py              # 主应用文件
├── wsgi.py             # WSGI 配置文件
├── requirements.txt    # Python 依赖
├── templates/          # HTML 模板
│   └── index.html     # 前端页面
└── static/            # 静态文件（自动创建）
```

## API 接口

### POST /generate_image

生成图片的 API 接口。

**请求参数:**
```json
{
  "prompt": "图片描述文字"
}
```

**响应格式:**
```json
{
  "success": true,
  "images": ["/static/image1.png"],
  "usage": {...}
}
```

## 注意事项

- 需要有效的阿里云 DashScope API 密钥
- 生成的图片会保存在 `static/` 目录
- 建议在生产环境使用云存储服务

## 许可证

MIT License