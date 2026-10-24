import boto3
import pytest
from moto import mock_aws

import app.api.files as files_api
from app.services.storage.s3 import S3Storage

PDF_CONTENT = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n%%EOF\n"


def upload_pdf(client, headers, filename="test.pdf"):
    return client.post(
        "/files",
        headers=headers,
        files={"file": (filename, PDF_CONTENT, "application/pdf")},
    )


@pytest.fixture
def s3_client_and_storage(client, monkeypatch):
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-central-1")
        s3.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-central-1"},
        )
        storage = S3Storage(bucket="test-bucket", client=s3)
        monkeypatch.setattr(files_api, "storage", storage)
        yield s3


def test_upload_download_delete_via_s3(client, create_user, s3_client_and_storage):
    s3 = s3_client_and_storage
    user = create_user()

    upload_response = upload_pdf(client, user["headers"])
    assert upload_response.status_code == 200
    file_id = upload_response.json()["id"]

    keys = [o["Key"] for o in s3.list_objects_v2(Bucket="test-bucket")["Contents"]]
    assert len(keys) == 1

    download_response = client.get(f"/files/{file_id}", headers=user["headers"])
    assert download_response.status_code == 200
    assert download_response.content == PDF_CONTENT
    assert "test.pdf" in download_response.headers["content-disposition"]

    delete_response = client.delete(f"/files/{file_id}", headers=user["headers"])
    assert delete_response.status_code == 200
    assert "Contents" not in s3.list_objects_v2(Bucket="test-bucket")
