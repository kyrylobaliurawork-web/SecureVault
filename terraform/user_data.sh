#!/bin/bash
set -euxo pipefail
apt-get update -y
apt-get install -y ca-certificates curl gnupg docker.io docker-compose-v2
systemctl enable --now docker
usermod -aG docker ubuntu
mkdir -p /opt/securevault
chown ubuntu:ubuntu /opt/securevault
echo "SecureVault EC2 initialization completed"
