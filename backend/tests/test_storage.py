import io

import boto3
import pytest
from moto import mock_aws

from app.services.storage.local import LocalStorage
from app.services.storage.s3 import S3Storage


class FakeUpload:
    def __init__(self, data: bytes):
        self.file = io.BytesIO(data)


@pytest.fixture
def local_storage(tmp_path):
    return LocalStorage(base_path=str(tmp_path / "storage"))


@pytest.fixture
def s3_storage():
    with mock_aws():
        client = boto3.client("s3", region_name="eu-central-1")
        client.create_bucket(
            Bucket="test-bucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-central-1"},
        )
        yield S3Storage(bucket="test-bucket", client=client)


@pytest.fixture(params=["local", "s3"])
def storage(request, local_storage, s3_storage):
    return local_storage if request.param == "local" else s3_storage


def test_save_and_open_roundtrip(storage):
    storage.save(FakeUpload(b"hello secure vault"), "key-1")

    stream = storage.open("key-1")
    try:
        assert stream.read() == b"hello secure vault"
    finally:
        stream.close()


def test_open_missing_key_raises(storage):
    with pytest.raises(FileNotFoundError):
        storage.open("does-not-exist")


def test_delete_removes_file(storage):
    storage.save(FakeUpload(b"data"), "key-2")
    storage.delete("key-2")

    with pytest.raises(FileNotFoundError):
        storage.open("key-2")


def test_delete_missing_key_does_not_fail(storage):
    storage.delete("never-existed")
