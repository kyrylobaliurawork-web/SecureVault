from pathlib import Path
from typing import BinaryIO
import shutil

from app.services.storage.base import StorageService


class LocalStorage(StorageService):

    def __init__(self, base_path: str = "storage"):
        self.base_path = Path(base_path)

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(self, file, storage_key: str) -> None:
        destination = self.base_path / storage_key

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

    def open(self, storage_key: str) -> BinaryIO:
        path = self.base_path / storage_key

        if not path.exists():
            raise FileNotFoundError(
                "Stored file does not exist"
            )

        return path.open("rb")

    def delete(self, storage_key: str) -> None:
        path = self.base_path / storage_key

        if path.exists():
            path.unlink()
