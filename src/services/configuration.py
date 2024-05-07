"""This file represents configurations from files and environment."""
from pathlib import Path
from dataclasses import dataclass

# Data access (With Save configs)
from src.services.authentication import AuthenticationService
from src.services.database import ClinicDatabase
from src.services.data_classes import SessionInfo

app_dir: Path = Path(__file__).parent.parent.parent


@dataclass
class Configuration:
    """All in one configuration's class."""

    app_dir = app_dir
    configs_dir = app_dir / "storage"
    configs_dir.mkdir(exist_ok=True, parents=True)

    # Data access (With Save configs)
    # Session {"page.session_id": SessionInfo}
    sessions: dict[str, SessionInfo]

    database = ClinicDatabase(configs_dir / "users.db")
    authentication: AuthenticationService = AuthenticationService(configs_dir / "authentication.json")


conf = Configuration(sessions={})

