from dataclasses import dataclass

from src.services.enums import AccessLevel


@dataclass
class SessionInfo:
    access_level: AccessLevel

    db_id: int
    full_name: str
