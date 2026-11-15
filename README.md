# SecureVault

## About the Project

SecureVault is a web application project that I developed together with its cloud infrastructure.

I created the website and used **Terraform** to build the AWS infrastructure where the application runs.

## AWS Architecture

The project uses the following AWS services:

- **Amazon VPC** — creates a private network for the infrastructure.
- **Public Subnet** — used for the EC2 instance.
- **Private Subnets** — used for the database.
- **Internet Gateway** — provides internet access to the public subnet.
- **Amazon EC2** — a virtual server where the application runs.
- **Amazon RDS (PostgreSQL)** — managed database service.
- **Amazon S3** — used for file storage.
- **AWS Secrets Manager** — stores application secrets and credentials.
- **AWS IAM** — manages permissions and access.
- **AWS Systems Manager (SSM)** — allows access to EC2 without opening an SSH port.

## Application

The website was developed as part of this project. It works together with the backend and PostgreSQL database.

The application is deployed using Docker and Docker Compose. Docker images are stored in GitHub Container Registry (GHCR).

During deployment, the EC2 instance retrieves the required configuration and credentials from AWS Secrets Manager.

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript/TypeScript

### Backend
- Python
- SQLAlchemy
- Alembic
- Psycopg

### Database
- PostgreSQL

### Cloud & Infrastructure
- Amazon Web Services (AWS)
- Terraform
- AWS IAM
- AWS Secrets Manager
- AWS Systems Manager
- Amazon S3
- Amazon EC2
- Amazon RDS

### DevOps & Deployment
- Docker
- Docker Compose
- GitHub Container Registry (GHCR)

## Project Structure

The Terraform configuration includes these main files:

- `main.tf` — main infrastructure resources.
- `provider.tf` — AWS provider configuration.
- `variables.tf` — project variables.
- `outputs.tf` — output values.
- `versions.tf` — Terraform and provider versions.

The application deployment directory on EC2 contains:

- `compose.yaml` — Docker Compose configuration.
- `deploy.sh` — deployment script.
- `backend.env` — non-sensitive backend configuration.
- `backend-secrets.env` — sensitive backend configuration retrieved from AWS Secrets Manager.

## Requirements

Before starting, make sure you have:

- Terraform installed.
- AWS CLI installed.
- An AWS account with the required permissions.
- Git installed.

Check the installations:

```bash
terraform version
aws --version
git --version
```

## Deployment Guide

### 1. Configure AWS CLI

Run:

```bash
aws configure
```

Enter your AWS Access Key, Secret Access Key and default region.

For this project, the AWS region is:

```text
us-east-1
```

Check the connection:

```bash
aws sts get-caller-identity
```

### 2. Open the Terraform Directory

```bash
cd terraform
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Check the Configuration

```bash
terraform fmt -recursive
terraform validate
```

### 5. Create a Deployment Plan

```bash
terraform plan
```

Check which AWS resources will be created before continuing.

### 6. Deploy the Infrastructure

```bash
terraform apply
```

Enter `yes` when Terraform asks for confirmation.

After deployment, check the outputs:

```bash
terraform output
```

## Application Configuration

### AWS Secrets Manager

After running `terraform apply`, configure the following secrets in AWS Secrets Manager.

**1. `securevault/app`**

This secret stores the application configuration:

```json
{
  "DATABASE_URL": "postgresql+psycopg://DB_USERNAME:URL_ENCODED_PASSWORD@YOUR_RDS_ENDPOINT:5432/securevault?sslmode=require",
  "SECRET_KEY": "YOUR_RANDOM_APPLICATION_SECRET"
}
```

The fields are:

- `DATABASE_URL` — PostgreSQL connection string from Amazon RDS.
- `SECRET_KEY` — a randomly generated secret key used by the application.

The database URL consists of:

- `postgresql+psycopg` — SQLAlchemy PostgreSQL dialect using the Psycopg driver.
- `DB_USERNAME` — PostgreSQL username.
- `URL_ENCODED_PASSWORD` — database password with special characters URL-encoded.
- `YOUR_RDS_ENDPOINT` — the RDS endpoint.
- `5432` — PostgreSQL default port.
- `securevault` — database name.
- `sslmode=require` — requires an encrypted SSL connection to RDS.

The backend must include the `psycopg` package in its Python dependencies.

#### Special Characters in DATABASE_URL

A database password may contain special characters such as `$`, `!`, `@`, `#`, `%`, `:`, `/` or parentheses.

Because `DATABASE_URL` is a connection string, special characters in the password must be URL-encoded (percent-encoded).

Examples:

| Original character | Encoded value |
|---|---|
| `$` | `%24` |
| `!` | `%21` |
| `<` | `%3C` |
| `>` | `%3E` |
| `(` | `%28` |
| `)` | `%29` |
| `@` | `%40` |
| `:` | `%3A` |
| `/` | `%2F` |
| `#` | `%23` |
| `%` | `%25` |

For example:

Original password:

```text
My$Pass!2026
```

URL-encoded password:

```text
My%24Pass%212026
```

Only the password part must be encoded, not the entire connection string.

The actual password stored in RDS must remain unchanged. Use its encoded representation only in `DATABASE_URL`.

**2. `securevault/ghcr`**

This secret stores GitHub Container Registry credentials:

```json
{
  "username": "YOUR_GITHUB_USERNAME",
  "token": "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
}
```

The fields are:

- `username` — your GitHub username.
- `token` — GitHub Personal Access Token with `read:packages` permission.

This secret is required when using private Docker images from GHCR.

**If the Docker images are public, GHCR authentication is not required.**

### Using Private Docker Images from GHCR

If you want to use private Docker images instead of public ones, follow these steps.

**1. Create a GitHub Personal Access Token**

In GitHub:

1. Open Settings.
2. Go to Developer settings.
3. Open Personal access tokens.
4. Create a new token.
5. Grant the `read:packages` permission.
6. Generate and copy the token.

For private packages owned by an organization, make sure the token has the necessary access to those packages.

**2. Configure the `securevault/ghcr` Secret**

Open AWS Secrets Manager and select `securevault/ghcr`.

Set its JSON value:

```json
{
  "username": "YOUR_GITHUB_USERNAME",
  "token": "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
}
```

Replace both values with your actual GitHub credentials.

**3. Configure Docker Image Names**

Open `compose.yaml` in the application deployment directory.

The image names are specified in the `image` fields:

```yaml
services:
  backend:
    image: ghcr.io/YOUR_GITHUB_USERNAME/YOUR_BACKEND_IMAGE:latest

  frontend:
    image: ghcr.io/YOUR_GITHUB_USERNAME/YOUR_FRONTEND_IMAGE:latest
```

Replace:

- `YOUR_GITHUB_USERNAME` with the GitHub account or organization that owns the packages.
- `YOUR_BACKEND_IMAGE` with the backend package name.
- `YOUR_FRONTEND_IMAGE` with the frontend package name.

Use the exact package names and tags available in GitHub Container Registry.

For example, my Docker Compose configuration uses the following images:

```yaml
services:
  backend:
    image: ghcr.io/kyrylobaliurawork-web/securevault-backend:latest

  frontend:
    image: ghcr.io/kyrylobaliurawork-web/securevault-frontend:latest
```

Replace the image names with your own GitHub Container Registry username, repository and package names or just use mine.

**4. Deployment Authentication**

The `deploy.sh` script retrieves the GHCR credentials from AWS Secrets Manager and uses them to authenticate with GitHub Container Registry before downloading private images.

After pulling the images, the script removes the temporary GHCR login credentials.

No GitHub token needs to be stored directly in `compose.yaml` or committed to the repository.

### Generate an Application Secret Key

Generate a random secret key for the backend.

For example, using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Store the generated value in the `SECRET_KEY` field of `securevault/app`.

**Security note:** Terraform creates the secrets, but their values must be configured separately. Never upload real credentials, passwords, tokens or secret values to GitHub.

## Application Environment Configuration

The deployment script creates or updates the following configuration files on EC2.

**`backend.env`**

Contains non-sensitive configuration:

```env
STORAGE_BACKEND=s3
S3_BUCKET=YOUR_S3_BUCKET_NAME
AWS_REGION=us-east-1
```

**`backend-secrets.env`**

Contains sensitive configuration retrieved from AWS Secrets Manager:

```env
DATABASE_URL=postgresql+psycopg://DB_USERNAME:URL_ENCODED_PASSWORD@YOUR_RDS_ENDPOINT:5432/securevault?sslmode=require
SECRET_KEY=YOUR_RANDOM_APPLICATION_SECRET
```

These files are used by Docker Compose to pass configuration to the backend container.

Do not commit these files to GitHub.

## Start the Application

The EC2 instance installs Docker, Docker Compose and other required tools using its User Data script.

The deployment script is located at:

```text
/opt/securevault/deploy.sh
```

To deploy the application, connect to EC2 using AWS Systems Manager Session Manager and run:

```bash
sudo /opt/securevault/deploy.sh
```

The deployment script performs the following operations:

1. Retrieves GHCR credentials if private images are used.
2. Retrieves application secrets from AWS Secrets Manager.
3. Creates or updates backend environment configuration files.
4. Pulls the latest frontend and backend Docker images.
5. Starts the application using Docker Compose.
6. Removes temporary GHCR login credentials.

## Checking the Application

After deployment, check if the application is available through the EC2 public address.

To check the running containers, use:

```bash
sudo docker ps
```

The frontend and backend containers should have the `Up` status.

**Troubleshooting note:**

If the frontend is running and the website loads correctly, but an error occurs when sending a request to the backend or accessing database-related functionality, the issue may be caused by an incorrect `DATABASE_URL`.

Check the following:

- The RDS endpoint is correct.
- The database name and username are correct.
- The database password is correct.
- The password is URL-encoded if it contains special characters.
- The connection string uses the correct PostgreSQL driver (`psycopg`(our one) or `asyncpg`, depending on the backend configuration).
- SSL is enabled with `sslmode=require` if required by the RDS connection.

Also make sure that the database credentials match the actual credentials configured in Amazon RDS and AWS Secrets Manager.

## Destroying the Infrastructure

When you no longer need the AWS infrastructure, run:

```bash
cd terraform
terraform destroy
```

Confirm the operation when Terraform asks.

**Warning:** This command deletes the infrastructure and may cause data loss. Save important data before running it.

## Security

Some security features used in this project:

- RDS is located in private subnets.
- Database access is allowed only from the EC2 Security Group.
- Public access to the S3 bucket is blocked.
- Encryption is enabled for S3 and RDS.
- Application secrets are stored in AWS Secrets Manager.
- EC2 uses an IAM Role to access AWS services.
- AWS Systems Manager is used instead of opening an SSH port.
- Database connections use SSL.
- Sensitive configuration files are not committed to GitHub.
- Private GHCR credentials are retrieved from AWS Secrets Manager instead of being stored in the Docker Compose configuration.

The infrastructure is designed to be budget-friendly. Some additional features, such as Multi-AZ deployment and automatic backups, are not enabled to keep AWS costs lower.
