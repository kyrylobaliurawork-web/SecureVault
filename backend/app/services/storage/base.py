from abc import ABC, abstractmethod
from pathlib import Path


class StorageService(ABC):

    @abstractmethod
    def save(self, file, storage_key: str) -> Path:
        pass

    @abstractmethod
    def get(self, storage_key: str) -> Path:
        pass

    @abstractmethod
    def delete(self, storage_key: str) -> None:
        pass