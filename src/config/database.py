from typing import Optional, Any
from urllib.parse import urlparse
import importlib

from src.config.settings import settings


class DatabaseClient:
    client: Optional[Any] = None


db = DatabaseClient()


async def get_db_client() -> Any:
    """Return a connected `databases.Database` instance (singleton).

    If `settings.POSTGRESSQL_URL` contains a JDBC-style URL (starts with 'jdbc:'),
    strip the prefix and use the hostname/port from it. The function composes
    a full URL including user/password and database name from settings.
    """
    if db.client is None:
        # Import lazily to avoid import-time errors when the package isn't installed
        databases_mod = importlib.import_module("databases")
        Database = getattr(databases_mod, "Database")

        raw = settings.POSTGRESSQL_URL or ""
        if raw.startswith("jdbc:"):
            raw = raw[len("jdbc:"):]

        parsed = urlparse(raw)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 5432
        # parsed.path may contain the database name; fall back to settings
        dbname = parsed.path.lstrip("/") or settings.POSTGRESSQL_DATABASE

        user = settings.POSTGRESSQL_USER
        password = settings.POSTGRESSQL_PASSWORD

        db_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

        db.client = Database(db_url)
        await db.client.connect()

    return db.client


async def close_db_client():
    if db.client:
        await db.client.disconnect()
        db.client = None
