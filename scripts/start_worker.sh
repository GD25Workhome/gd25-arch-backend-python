#!/bin/bash
# Celery Worker 启动脚本

# 激活虚拟环境（如果使用）
# source venv/bin/activate

# 获取配置
WORKER_LOGLEVEL=${WORKER_LOGLEVEL:-info}
WORKER_CONCURRENCY=${WORKER_CONCURRENCY:-4}
WORKER_QUEUE=${WORKER_QUEUE:-celery}

# 构建启动命令
CMD="celery -A app.tasks.celery_app worker --loglevel=${WORKER_LOGLEVEL} --concurrency=${WORKER_CONCURRENCY}"

# 添加队列配置（如果指定）
if [ -n "$WORKER_QUEUE" ]; then
    CMD="${CMD} -Q ${WORKER_QUEUE}"
fi

# 启动 Worker
echo "启动 Celery Worker..."
echo "日志级别: ${WORKER_LOGLEVEL}"
echo "并发数: ${WORKER_CONCURRENCY}"
echo "队列: ${WORKER_QUEUE}"
echo "命令: ${CMD}"
echo ""

exec $CMD

