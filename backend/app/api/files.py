import uuid

from fastapi import APIRouter, Depends, File as FastAPIFile, HTTPException, UploadFile
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import File, User
from app.schemas.file import FileResponse
from app.services.file_service import calculate_checksum, storage


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
    storage_key = str(uuid.uuid4())

    checksum = calculate_checksum(file)

    file_path = storage.save(
        file,
        storage_key,
    )

    file_size = file_path.stat().st_size

    db_file = File(
        user_id=current_user.id,
        filename=file.filename,
        size=file_size,
        content_type=file.content_type or "application/octet-stream",
        storage_key=storage_key,
        checksum=checksum,
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


@router.get(
    "",
    response_model=list[FileResponse],
)
def list_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    files = db.query(File).filter(
        File.user_id == current_user.id
    ).all()

    return files


@router.get("/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id,
    ).first()

    if db_file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    file_path = storage.get(
        db_file.storage_key
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
    db_file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id,
    ).first()

    if db_file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    storage.delete(
        db_file.storage_key
    )

    db.delete(db_file)
    db.commit()

    return {
        "message": "File deleted successfully"
    }