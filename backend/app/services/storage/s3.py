from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError

from app.services.storage.base import StorageService


class _KeepOpen:
    """boto3 closes the file object after upload_fileobj.

    The upload endpoint still needs the file afterwards (size, rewind),
    so we hand boto3 a wrapper whose close() does nothing.
    """

    def __init__(self, fileobj):
        self._fileobj = fileobj

    def __getattr__(self, name):
        return getattr(self._fileobj, name)

    def close(self):
        pass


class S3Storage(StorageService):
    """Stores files in an S3 bucket.

    Credentials are not passed here: boto3 picks them up from the
    environment (on EC2/EKS this is the attached IAM role).
    Encryption at rest is configured on the bucket itself.
    """

    def __init__(self, bucket: str, region: str | None = None, client=None):
        self.bucket = bucket
        self.client = client or boto3.client("s3", region_name=region)

    def save(self, file, storage_key: str) -> None:
        self.client.upload_fileobj(
            _KeepOpen(file.file),
            self.bucket,
            storage_key,
        )

    def open(self, storage_key: str) -> BinaryIO:
        try:
            response = self.client.get_object(
                Bucket=self.bucket,
                Key=storage_key,
            )
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code")

            if code in {"NoSuchKey", "404"}:
                raise FileNotFoundError(
                    "Stored file does not exist"
                ) from exc

            raise

        return response["Body"]

    def delete(self, storage_key: str) -> None:
        self.client.delete_object(
            Bucket=self.bucket,
            Key=storage_key,
        )
