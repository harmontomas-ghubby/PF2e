from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Solo PF2e Table"
    db_path: str = "sqlite:///solo_table.db"
    data_dir: Path = Path("data")
    templates_dir: Path = Path("app/templates")
    static_dir: Path = Path("app/static")


settings = Settings()
