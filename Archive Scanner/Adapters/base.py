from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkResult:
    work_id: int
    title: str
    authors: list[str]
    summary: str
    url: str
    relationships: list[str]
    date_published: datetime
    word_count: int
    chapters: str
    is_complete: bool
    rating: str
    is_restricted: bool


class SiteAdapter(ABC):
    @abstractmethod
    async def authenticate(self, config: dict) -> bool:
        """Authenticate with the site using provided credentials."""
        ...

    @abstractmethod
    async def search(self, tag: str, max_pages: int) -> list[WorkResult]:
        """Search for works matching a relationship/character tag."""
        ...

    @abstractmethod
    async def validate_tag(self, tag: str) -> bool:
        """Check whether a tag exists and is valid on this site."""
        ...

    @abstractmethod
    def get_tag_format_help(self) -> str:
        """Return a human-readable string describing the expected tag format."""
        ...
