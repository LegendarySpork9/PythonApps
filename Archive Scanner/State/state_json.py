import json
import logging
import os

from State import StateBackend

logger = logging.getLogger("archive_scanner.state_json")

ID_CAP_PER_TAG = 500
STATE_FILENAME = "seen_works.json"


class JsonStateBackend(StateBackend):
    def __init__(self, state_dir: str):
        self._path = os.path.join(state_dir, STATE_FILENAME)
        self._state: dict[str, list[int]] = self._load_file()

    def _load_file(self) -> dict[str, list[int]]:
        if not os.path.exists(self._path):
            logger.info("No %s found, starting with empty state", STATE_FILENAME)
            return {}

        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            logger.warning("%s is corrupted, resetting to empty state", STATE_FILENAME)
            return {}

        if not isinstance(data, dict):
            logger.warning("%s has unexpected format, resetting to empty state", STATE_FILENAME)
            return {}

        return data

    def _save_file(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def load(self, key: str) -> list[int]:
        return list(self._state.get(key, []))

    def save(self, key: str, work_ids: list[int]) -> None:
        self._state[key] = work_ids[-ID_CAP_PER_TAG:]
        self._save_file()

    def add_works(self, key: str, new_ids: list[int]) -> None:
        existing = self._state.get(key, [])
        existing.extend(new_ids)
        self._state[key] = existing[-ID_CAP_PER_TAG:]
        self._save_file()

    def get_all_keys(self) -> list[str]:
        return list(self._state.keys())
