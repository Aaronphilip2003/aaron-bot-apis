from pydantic import BaseModel, Field
from typing import List, Optional

class QueryEntry(BaseModel):
    query: str = Field(..., title="Query", description="The query to search for.")

