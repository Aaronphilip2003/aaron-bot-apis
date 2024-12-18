from pydantic import BaseModel, Field
from typing import List, Optional

class AddEntry(BaseModel):
    content: str = Field(..., title="Content", description="The main content of the entry.")
    tags: List[str] = Field(..., title="Tags", description="List of tags associated with the entry.")
    metadata: Optional[dict] = Field(None, title="Metadata", description="Optional metadata such as mood or activity type.")
