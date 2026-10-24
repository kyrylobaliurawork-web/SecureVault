from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageService(ABC):
    """Interface for file storage backends (local disk, S3, ...)."""

    @abstractmethod
    def save(self, file, storage_key: str) -> None:
        """Store the content of an UploadFile under storage_key."""

    @abstractmethod
    def open(self, storage_key: str) -> BinaryIO:
        """Return a readable binary stream.

        Raises FileNotFoundError if the key does not exist.
        The caller is responsible for closing the stream.
        """

    @abstractmethod
    def delete(self, storage_key: str) -> None:
        """Delete the stored file. Must not fail if it is already gone."""
