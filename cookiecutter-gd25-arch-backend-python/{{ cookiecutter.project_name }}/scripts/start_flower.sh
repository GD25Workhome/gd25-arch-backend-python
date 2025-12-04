#!/bin/bash
# Flower 监控服务启动脚本

# 激活虚拟环境（如果使用）
# source venv/bin/activate

# 获取配置
FLOWER_PORT=${FLOWER_PORT:-5555}
FLOWER_BASIC_AUTH=${FLOWER_BASIC_AUTH:-""}
FLOWER_URL_PREFIX=${FLOWER_URL_PREFIX:-""}

# 构建启动命令
CMD="celery -A app.tasks.celery_app flower --port=${FLOWER_PORT}"

# 添加基本认证（如果配置）
if [ -n "$FLOWER_BASIC_AUTH" ]; then
    CMD="${CMD} --basic_auth=${FLOWER_BASIC_AUTH}"
fi

# 添加 URL 前缀（如果配置）
if [ -n "$FLOWER_URL_PREFIX" ]; then
    CMD="${CMD} --url_prefix=${FLOWER_URL_PREFIX}"
fi

# 添加 Broker API 配置（解决 Management API 连接问题）
# 如果配置了 RabbitMQ Management API 地址，使用它
if [ -n "$RABBITMQ_MANAGEMENT_URL" ]; then
    CMD="${CMD} --broker_api=${RABBITMQ_MANAGEMENT_URL}"
fi

# 启动 Flower
echo "启动 Flower 监控服务..."
echo "访问地址: http://localhost:${FLOWER_PORT}${FLOWER_URL_PREFIX}"
echo "命令: ${CMD}"
echo ""

exec $CMD

