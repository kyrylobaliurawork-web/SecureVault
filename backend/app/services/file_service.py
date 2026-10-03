import hashlib
import uuid

from app.services.storage.local import LocalStorage


storage = LocalStorage()


def generate_storage_key() -> str:
    return str(uuid.uuid4())


def calculate_checksum(file) -> str:
    sha256 = hashlib.sha256()

    while chunk := file.file.read(1024 * 1024):
        sha256.update(chunk)

    file.file.seek(0)

    return sha256.hexdigest()