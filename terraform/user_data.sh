#!/bin/bash
set -euo pipefail

exec > >(tee -a /var/log/securevault-bootstrap.log) 2>&1

REGION="${aws_region}"
S3_BUCKET="${s3_bucket}"

echo "Starting SecureVault bootstrap..."

apt-get update -y
apt-get install -y docker.io docker-compose-v2 jq curl unzip

curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" \
    -o "/tmp/awscliv2.zip"

unzip -q /tmp/awscliv2.zip -d /tmp

/tmp/aws/install

rm -rf /tmp/aws /tmp/awscliv2.zip

systemctl enable --now docker

mkdir -p /opt/securevault
chmod 755 /opt/securevault

cat > /opt/securevault/deploy.sh <<'DEPLOY'
#!/bin/bash
set -euo pipefail

REGION="${aws_region}"
S3_BUCKET="${s3_bucket}"

APP_SECRET="securevault/app"
GHCR_SECRET="securevault/ghcr"

cd /opt/securevault

echo "Retrieving GHCR credentials..."

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

echo "Retrieving application secrets..."

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

cat > /opt/securevault/backend.env <<EOF
STORAGE_BACKEND=s3
S3_BUCKET=$S3_BUCKET
AWS_REGION=$REGION
EOF

cat > /opt/securevault/compose.yaml <<'COMPOSE'
services:
  backend:
    image: ghcr.io/kyrylobaliurawork-web/securevault-backend:latest
    restart: unless-stopped
    env_file:
      - backend-secrets.env
      - backend.env

  frontend:
    image: ghcr.io/kyrylobaliurawork-web/securevault-frontend:latest
    restart: unless-stopped
    ports:
      - "80:80"
    depends_on:
      - backend
COMPOSE

chmod 600 /opt/securevault/backend-secrets.env
chmod 600 /opt/securevault/backend.env

docker compose -f /opt/securevault/compose.yaml pull
docker compose -f /opt/securevault/compose.yaml up -d

docker logout ghcr.io

echo "SecureVault deployment completed."
DEPLOY

chmod 700 /opt/securevault/deploy.sh

echo "Bootstrap completed."
echo "After adding both Secrets Manager values, run:"
echo "sudo /opt/securevault/deploy.sh"