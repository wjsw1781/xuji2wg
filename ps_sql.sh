#!/usr/bin/env bash
# ── minimal postgres install & bootstrap for Anvil ──
set -e

DB_NAME="anvildb"
DB_USER="anvil_user"
DB_PASS="VerySecret!"
DB_PORT=25332        # 改成你想要的端口

echo "[1/3] Install PostgreSQL (system default version)…"
apt-get update -qq
DEBIAN_FRONTEND=noninteractive \
  apt-get install -y postgresql postgresql-contrib

# 取实际版本号
PG_VER=$(ls /etc/postgresql | head -n1)
PG_CONF="/etc/postgresql/$PG_VER/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VER/main/pg_hba.conf"

echo "[2/3] Configure to listen on 0.0.0.0:$DB_PORT …"
sed -ri "s/^#?listen_addresses\s*=.*$/listen_addresses = '*'/;" "$PG_CONF"
sed -ri "s/^#?port\s*=.*$/port = $DB_PORT/;" "$PG_CONF"
echo "host all all 0.0.0.0/0 md5" >> "$PG_HBA"
systemctl restart postgresql

echo "[3/3] Create role/database (idempotent)…"
# 如果角色不存在就创建
sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" \
  | grep -q 1 || \
  sudo -u postgres psql -c "CREATE ROLE $DB_USER LOGIN PASSWORD '$DB_PASS'"

# 如果数据库不存在就创建
sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" \
  | grep -q 1 || \
  sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER ENCODING 'UTF8'"

echo
echo "✅  PostgreSQL ready."
echo "export ANVIL_DATA_DB_URL=postgresql://$DB_USER:$DB_PASS@127.0.0.1:$DB_PORT/$DB_NAME"
echo
