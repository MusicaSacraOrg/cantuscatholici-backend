from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReviewCommentBase(BaseModel):
    content: str | None = None


class ReviewCommentCreate(ReviewCommentBase):
    pass


class ReviewComment(ReviewCommentBase):
    id: int
    review_request_id: int
    created_by_user_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ReviewRequestBase(BaseModel):
    description: str | None = None
    new_entity_id: int
    original_id: int | None = None


class ReviewRequestCreate(ReviewRequestBase):
    pass


class ReviewRequest(ReviewRequestBase):
    id: int
    requester_id: int
    editor_id: int | None = None
    created_at: datetime | None = None
    closed_at: datetime | None = None
    comments: list[ReviewComment] = []

    model_config = ConfigDict(from_attributes=True)


class ReviewApprove(BaseModel):
    editor_id: int


class ReviewRequestUpdate(BaseModel):
    description: str | None = None

