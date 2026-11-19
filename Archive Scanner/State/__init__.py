import logging
from abc import ABC, abstractmethod

logger = logging.getLogger("archive_scanner.state")


class StateBackend(ABC):
    @abstractmethod
    def load(self, key: str) -> list[int]:
        """Load seen work IDs for a given site:tag key."""
        ...

    @abstractmethod
    def save(self, key: str, work_ids: list[int]) -> None:
        """Save seen work IDs for a given site:tag key."""
        ...

    @abstractmethod
    def add_works(self, key: str, new_ids: list[int]) -> None:
        """Add new work IDs to the existing set for a key."""
        ...

    @abstractmethod
    def get_all_keys(self) -> list[str]:
        """Return all site:tag keys that have stored state."""
        ...


def get_state_backend(config, state_dir: str) -> StateBackend:
    if config.storage.mode == "sqlite":
        from State.state_sqlite import SqliteStateBackend

        try:
            backend = SqliteStateBackend(config.storage.sqlite_path)
            logger.info("Using SQLite state backend: %s", config.storage.sqlite_path)
            return backend
        except Exception as e:
            logger.warning(
                "SQLite backend unavailable (%s), falling back to JSON", e
            )

    from State.state_json import JsonStateBackend

    backend = JsonStateBackend(state_dir)
    logger.info("Using JSON state backend")
    return backend
