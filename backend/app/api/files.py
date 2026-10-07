from fastapi import (APIRouter, Depends, File as FastAPIFile, HTTPException, UploadFile)

from fastapi.responses import FileResponse as FastAPIFileResponse

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import File, User
from app.schemas.file import FileResponse
from app.services.file_service import (calculate_checksum, generate_storage_key, sanitize_filename, storage, validate_file)

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)

@router.post(
    "",
    response_model=FileResponse,
)
def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_file(file)

    storage_key = generate_storage_key()

    filename = sanitize_filename(
        file.filename
    )

    checksum = calculate_checksum(file)

    try:
        storage.save(
            file,
            storage_key,
        )

        file_size = file.file.seek(0, 2)
        file.file.seek(0)

        db_file = File(
            user_id=current_user.id,
            filename=filename,
            size=file_size,
            content_type=file.content_type
            or "application/octet-stream",
            storage_key=storage_key,
            checksum=checksum,
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file

    except Exception:
        db.rollback()

        try:
            storage.delete(storage_key)
        except Exception:
            pass

        raise


@router.get(
    "",
    response_model=list[FileResponse],
)
def list_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    files = (
        db.query(File)
        .filter(
            File.user_id == current_user.id
        )
        .all()
    )

    return files


@router.get("/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_file = (
        db.query(File)
        .filter(
            File.id == file_id,
            File.user_id == current_user.id,
        )
        .first()
    )

    if db_file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    try:
        file_path = storage.get(
            db_file.storage_key
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Stored file not found",
        )

    return FastAPIFileResponse(
        path=file_path,
        filename=db_file.filename,
        media_type=db_file.content_type,
    )


@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_file = (
        db.query(File)
        .filter(
            File.id == file_id,
            File.user_id == current_user.id,
        )
        .first()
    )

    if db_file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    storage_key = db_file.storage_key

    try:
        storage.delete(
            storage_key
        )

        db.delete(db_file)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "message": "File deleted successfully"
    }