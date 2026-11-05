#!/bin/bash
set -euo pipefail

exec > >(tee -a /var/log/securevault-bootstrap.log) 2>&1

REGION="us-east-1"
APP_SECRET="securevault/app"
GHCR_SECRET="securevault/ghcr"
S3_BUCKET="securevault-files-806116531925-us-east-1-an"

echo "Starting SecureVault initialization..."

# Install Docker, Compose, AWS CLI and jq
apt-get update -y
apt-get install -y docker.io docker-compose-v2 awscli jq

systemctl enable --now docker

mkdir -p /opt/securevault
cd /opt/securevault

# Wait for IAM permissions to become available
for attempt in $(seq 1 12); do
    if aws sts get-caller-identity --region "$REGION" >/dev/null 2>&1; then
        break
    fi
    echo "Waiting for EC2 IAM role..."
    sleep 10
done

# Retrieve GHCR credentials
GHCR_JSON=$(aws secretsmanager get-secret-value \
    --secret-id "$GHCR_SECRET" \
    --region "$REGION" \
    --query SecretString \
    --output text)

GHCR_USERNAME=$(echo "$GHCR_JSON" | jq -er '.username')
GHCR_TOKEN=$(echo "$GHCR_JSON" | jq -er '.token')

echo "$GHCR_TOKEN" | docker login ghcr.io \
    --username "$GHCR_USERNAME" \
    --password-stdin

unset GHCR_JSON GHCR_TOKEN

# Retrieve application secrets
APP_JSON=$(aws secretsmanager get-secret-value \
    --secret-id "$APP_SECRET" \
    --region "$REGION" \
    --query SecretString \
    --output text)

umask 077

echo "$APP_JSON" | jq -er '
    "DATABASE_URL=" + .DATABASE_URL + "\nSECRET_KEY=" + .SECRET_KEY
' > /opt/securevault/backend-secrets.env

unset APP_JSON GHCR_USERNAME

# Configure S3 storage
cat > /opt/securevault/backend.env <<EOF
STORAGE_BACKEND=s3
S3_BUCKET=$S3_BUCKET
AWS_REGION=$REGION
EOF

# Create Compose file on EC2
cat > /opt/securevault/compose.yaml <<'EOF'
services:
  backend:
    image: ghcr.io/kyrylobaliurawork-web/securevault-backend:latest
    restart: unless-stopped
    env_file:
      - backend-secrets.env
      - backend.env
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
      interval: 10s
      timeout: 5s
      retries: 5

  frontend:
    image: ghcr.io/kyrylobaliurawork-web/securevault-frontend:latest
    restart: unless-stopped
    ports:
      - "80:80"
    depends_on:
      backend:
        condition: service_healthy
EOF

chmod 600 /opt/securevault/backend-secrets.env
chmod 600 /opt/securevault/backend.env

# Pull images and start containers
docker compose -f /opt/securevault/compose.yaml pull
docker compose -f /opt/securevault/compose.yaml up -d

echo "SecureVault initialization completed."