#!/bin/bash
# 雾室 vapelab 数据库备份脚本
# 添加到 crontab: 0 3 * * * /var/www/vapelab/deploy/backup.sh

BACKUP_DIR="/var/www/vapelab/backups"
DB_FILE="/var/www/vapelab/backend/vapelab.db"
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

DATE=$(date +%Y%m%d_%H%M%S)
cp "$DB_FILE" "$BACKUP_DIR/vapelab_$DATE.db"

# 压缩
gzip "$BACKUP_DIR/vapelab_$DATE.db"

# 清理 7 天前的备份
find "$BACKUP_DIR" -name "vapelab_*.db.gz" -mtime +$RETENTION_DAYS -delete

echo "备份完成: vapelab_$DATE.db.gz ($(ls -lh "$BACKUP_DIR/vapelab_$DATE.db.gz" | awk '{print $5}'))"
