import hashlib
import uuid
import os

from fastapi import HTTPException, UploadFile

from app.services.storage.local import LocalStorage


MAX_FILE_SIZE = 10 * 1024 * 1024


ALLOWED_CONTENT_TYPES = {
    "text/plain",
    "application/pdf",
    "image/jpeg",
    "image/png",
    "application/zip",
    "application/x-zip-compressed",
}


storage = LocalStorage()


def generate_storage_key() -> str:
    return str(uuid.uuid4())


def sanitize_filename(filename: str | None) -> str:
    if not filename:
        return "unnamed-file"

    filename = filename.replace("\\", "/")

    filename = os.path.basename(filename)

    if not filename:
        return "unnamed-file"

    return filename


def validate_file(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="File type is not allowed",
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 10 MB",
        )


def calculate_checksum(file: UploadFile) -> str:
    sha256 = hashlib.sha256()

    while chunk := file.file.read(1024 * 1024):
        sha256.update(chunk)

    file.file.seek(0)

    return sha256.hexdigest()