from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ArticleBase(BaseModel):
    title: str
    plan_content: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    owner_id: int
    status: str
    created_at: datetime
    draft_content: Optional[str] = None
    final_content: Optional[str] = None

    class Config:
        orm_mode = True
        
class PlanUpdateRequest(BaseModel):
    new_plan: str