from dataclasses import dataclass
from enum import Enum


class AccessLevel(Enum):
    ADMIN = 1
    DOCTOR = 2
    USER = 3


@dataclass
class SessionInfo:
    access_level: AccessLevel
    login: str

    db_id: int = None
    name: str = None

