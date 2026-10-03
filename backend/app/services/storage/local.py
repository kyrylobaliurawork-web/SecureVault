from pathlib import Path
import shutil

from app.services.storage.base import StorageService


class LocalStorage(StorageService):

    def __init__(self, base_path: str = "storage"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, file, storage_key: str) -> Path:

        destination = self.base_path / storage_key

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return destination

    def get(self, storage_key: str) -> Path:

        path = self.base_path / storage_key

        if not path.exists():
            raise FileNotFoundError(
                "File not found"
            )

        return path

    def delete(self, storage_key: str) -> None:

        path = self.base_path / storage_key

        if path.exists():
            path.unlink()