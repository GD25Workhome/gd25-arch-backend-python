#!/bin/bash
# 生产环境启动脚本

# 激活虚拟环境（如果使用）
# source venv/bin/activate

# 启动生产服务器（多进程模式）
# 注意：需要安装 gunicorn: pip install gunicorn
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8100 \
    --access-logfile - \
    --error-logfile -

