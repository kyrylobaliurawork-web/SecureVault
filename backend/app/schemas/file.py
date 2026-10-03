from datetime import datetime

from pydantic import BaseModel


class FileResponse(BaseModel):
    id: int
    filename: str
    size: int
    content_type: str
    checksum: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }