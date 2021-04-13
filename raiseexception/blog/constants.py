from enum import Enum


class PostState(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'


class PostCommentState(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
