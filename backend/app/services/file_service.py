import hashlib
import os
import uuid

from fastapi import HTTPException, UploadFile
import magic

from app.services.storage.local import LocalStorage


MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "text/plain",
    "application/pdf",
    "image/jpeg",
    "image/png",
    "application/zip",
}

mime_detector = magic.Magic(mime=True)

storage = LocalStorage()


def generate_storage_key() -> str:
    return str(uuid.uuid4())


def sanitize_filename(filename: str | None) -> str:
    if not filename:
        return "unnamed-file"

    filename = filename.replace("\\", "/")
    filename = os.path.basename(filename)

    if not filename or filename in {".", ".."}:
        return "unnamed-file"

    filename = "".join(
        char for char in filename
        if char.isprintable()
    )

    return filename[:255] or "unnamed-file"


def validate_file(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty files are not allowed",
        )

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 10 MB",
        )

    sample = file.file.read(8192)
    file.file.seek(0)

    if not sample:
        raise HTTPException(
            status_code=400,
            detail="Could not read file",
        )

    detected_type = mime_detector.from_buffer(sample)

    if detected_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="File content type is not allowed",
        )

    if (
        file.content_type
        and file.content_type != "application/octet-stream"
        and file.content_type != detected_type
    ):
        raise HTTPException(
            status_code=400,
            detail="Declared file type does not match file content",
        )


def calculate_checksum(file: UploadFile) -> str:
    sha256 = hashlib.sha256()

    while chunk := file.file.read(1024 * 1024):
        sha256.update(chunk)

    file.file.seek(0)

    return sha256.hexdigest()