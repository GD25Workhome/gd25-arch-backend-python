#!/bin/bash
# 开发环境启动脚本

# 激活虚拟环境（如果使用）
# source venv/bin/activate

# 启动开发服务器（带自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8090

