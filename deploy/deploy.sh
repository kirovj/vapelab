#!/bin/bash
# 雾室 vapelab 部署脚本
# 用法: bash deploy/deploy.sh

set -e

APP_DIR="/var/www/vapelab"
PYTHON="$APP_DIR/.venv/bin/python"

echo "=== 拉取最新代码 ==="
cd "$APP_DIR"
git pull origin main

echo "=== 安装后端依赖 ==="
$PYTHON -m pip install -r backend/requirements.txt

echo "=== 数据库迁移 ==="
cd "$APP_DIR/backend"
$PYTHON -m alembic upgrade head

echo "=== 构建前端 ==="
cd "$APP_DIR/frontend"
npm install --production
npm run build

echo "=== 重启服务 ==="
sudo systemctl restart vapelab
sudo systemctl reload nginx

echo "=== 部署完成 ==="
