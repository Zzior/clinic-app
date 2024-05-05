"""This file represents configurations from files and environment."""
from pathlib import Path
from dataclasses import dataclass

# Data access (With Save configs)
from src.services.database import ClinicDatabase
from src.services.data_classes import AccessLevel

app_dir: Path = Path(__file__).parent.parent.parent


@dataclass
class Configuration:
    """All in one configuration's class."""
    # Session {"page.session_id": {"name": "user_name", ...}}
    sessions: dict[str, AccessLevel]

    app_dir = app_dir
    configs_dir = app_dir / "storage"
    database_dir = configs_dir / "users.db"

    # Services
    database = ClinicDatabase(database_dir)


conf = Configuration(sessions={})

