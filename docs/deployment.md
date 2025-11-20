# 📦 打包和分发指南

## 📋 目录
- [打包方式](#打包方式)
- [安装方法](#安装方法)
- [Docker部署](#docker部署)
- [云平台部署](#云平台部署)

---

## 📦 打包方式

### 方式1：源码分发
```bash
# 创建源码包
python setup.py sdist

# 创建wheel包
python setup.py bdist_wheel

# 查看生成的包
ls dist/
```

### 方式2：PyPI发布
```bash
# 安装发布工具
pip install twine

# 上传到PyPI（测试）
twine upload --repository testpypi dist/*

# 上传到PyPI（正式）
twine upload dist/*
```

### 方式3：可执行文件
```bash
# 使用PyInstaller打包
pip install pyinstaller

# 创建可执行文件
pyinstaller --onefile main.py

# 查看生成的文件
ls dist/
```

---

## 🚀 安装方法

### 方法1：从源码安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/literature_agent.git
cd literature_agent

# 安装依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

### 方法2：从PyPI安装
```bash
# 正式版本
pip install literature-agent-system

# 开发版本
pip install literature-agent-system[dev]

# 包含PDF功能
pip install literature-agent-system[pdf]
```

### 方法3：conda安装
```bash
# 创建conda环境
conda create -n literature-agent python=3.9
conda activate literature-agent

# 安装依赖
conda install pandas openpyxl python-dotenv
pip install literature-agent-system
```

---

## 🐳 Docker部署

### 1. 创建Dockerfile
```dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 设置环境变量
ENV PYTHONPATH=/app

# 暴露端口（如果有Web界面）
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]
```

### 2. 构建Docker镜像
```bash
# 构建镜像
docker build -t literature-agent .

# 运行容器
docker run -v $(pwd)/data:/app/data literature-agent
```

### 3. Docker Compose
```yaml
version: '3.8'

services:
  literature-agent:
    build: .
    volumes:
      - ./data:/app/data
      - ./.env:/app/.env
    environment:
      - PYTHONPATH=/app
    command: python main.py
    
  # 可选：添加数据库
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: literature_agent
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## ☁️ 云平台部署

### AWS部署
```bash
# 使用AWS CLI
aws s3 cp dist/ s3://your-bucket/literature-agent/

# 使用AWS EC2
sudo yum install python3 python3-pip
pip3 install literature-agent-system
```

### Google Cloud Platform
```bash
# 使用Google Cloud Storage
gsutil cp dist/* gs://your-bucket/

# 使用Google Cloud Run
gcloud builds submit --tag gcr.io/PROJECT-ID/literature-agent
gcloud run deploy --image gcr.io/PROJECT-ID/literature-agent
```

### Azure部署
```bash
# 使用Azure Container Instances
az container create \
  --resource-group myResourceGroup \
  --name literature-agent \
  --image literature-agent:latest \
  --cpu 1 \
  --memory 2
```

---

## 📋 版本管理

### 语义化版本控制
```
主版本号.次版本号.修订号

例如：1.0.0
- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正
```

### 发布流程
```bash
# 1. 更新版本号
vim setup.py  # 修改version

# 2. 更新CHANGELOG
vim CHANGELOG.md

# 3. 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 4. 构建和发布
python setup.py sdist bdist_wheel
twine upload dist/*
```

---

## 🔧 配置管理

### 环境变量配置
```bash
# 生产环境
export LLM_MODEL=gpt-4
export OPENAI_API_BASE=https://api.openai.com/v1
export OPENAI_API_KEY=your-production-key

# 开发环境
export LLM_MODEL=gpt-3.5-turbo
export OPENAI_API_BASE=https://api.openai.com/v1
export OPENAI_API_KEY=your-dev-key
```

### 配置文件管理
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API配置
    OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    
    # 数据路径
    DATA_DIR = os.getenv('DATA_DIR', 'data')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
    
    # 性能配置
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '10'))

class DevelopmentConfig(Config):
    DEBUG = True
    LLM_MODEL = 'gpt-3.5-turbo'

class ProductionConfig(Config):
    DEBUG = False
    LLM_MODEL = 'gpt-4'
```

---

## 📊 监控和日志

### 日志配置
```python
# logging_config.py
import logging
from datetime import datetime

def setup_logging():
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 文件处理器
    file_handler = logging.FileHandler(
        f'logs/literature_agent_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 根日志器配置
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
```

### 性能监控
```python
# monitor.py
import time
import psutil
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.2f}秒")
        print(f"内存使用变化: {(end_memory - start_memory) / 1024 / 1024:.2f}MB")
        
        return result
    return wrapper
```

---

## 🔒 安全考虑

### API密钥管理
```bash
# 使用环境变量
export OPENAI_API_KEY=your-secret-key

# 使用密钥管理服务
aws secretsmanager get-secret-value --secret-id literature-agent-api-key
```

### 数据安全
```python
# 数据加密
from cryptography.fernet import Fernet

def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data
```

---

## 🚀 CI/CD集成

### GitHub Actions示例
```yaml
name: Build and Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Build package
      run: |
        python setup.py sdist bdist_wheel
    
    - name: Publish to PyPI
      if: github.event_name == 'push' && github.ref == 'refs/heads/main'
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

---

## 📞 支持和维护

### 技术支持
- 📧 邮件：support@literature-agent.com
- 💬 在线客服：https://chat.literature-agent.com
- 📖 文档：https://docs.literature-agent.com

### 社区支持
- 🐛 问题反馈：GitHub Issues
- 💡 功能建议：GitHub Discussions
- 🌟 星标支持：给项目点星

### 商业支持
- 🔧 定制开发
- 🏢 企业培训
- 📊 数据分析服务