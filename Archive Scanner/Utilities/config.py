import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("archive_scanner.config")


@dataclass
class AO3Config:
    username: str
    password: str


@dataclass
class SmtpConfig:
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True


@dataclass
class EmailConfig:
    from_address: str
    to_address: str
    subject_prefix: str = "[Archive Scanner]"


@dataclass
class Relationship:
    site: str
    tag: str
    track_from: datetime


@dataclass
class StorageConfig:
    mode: str = "json"
    sqlite_path: str = ""


@dataclass
class SearchConfig:
    max_pages: int = 2
    delay_between_requests_seconds: int = 3


@dataclass
class AppConfig:
    ao3: AO3Config
    smtp: SmtpConfig
    email: EmailConfig
    relationships: list[Relationship]
    storage: StorageConfig = field(default_factory=StorageConfig)
    search: SearchConfig = field(default_factory=SearchConfig)


def load_config(config_path: str) -> AppConfig | None:
    if not os.path.exists(config_path):
        logger.error("config.json not found at %s", config_path)
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError as e:
        logger.error("config.json contains invalid JSON: %s", e)
        return None

    required_sections = ["ao3", "smtp", "email", "relationships"]
    missing = [s for s in required_sections if s not in raw]

    if missing:
        for section in missing:
            logger.error("config.json missing required section: '%s'", section)
        return None

    ao3 = _parse_ao3(raw["ao3"])
    if ao3 is None:
        return None

    smtp = _parse_smtp(raw["smtp"])
    if smtp is None:
        return None

    email_config = _parse_email(raw["email"])
    if email_config is None:
        return None

    relationships = _parse_relationships(raw["relationships"])
    if not relationships:
        logger.error("No valid relationships found in config")
        return None

    storage = _parse_storage(raw.get("storage", {}))
    search = _parse_search(raw.get("search", {}))

    return AppConfig(
        ao3=ao3,
        smtp=smtp,
        email=email_config,
        relationships=relationships,
        storage=storage,
        search=search,
    )


def _parse_ao3(data: dict) -> AO3Config | None:
    for field_name in ("username", "password"):
        if field_name not in data or not data[field_name]:
            logger.error("ao3 section missing required field: '%s'", field_name)
            return None

    return AO3Config(username=data["username"], password=data["password"])


def _parse_smtp(data: dict) -> SmtpConfig | None:
    for field_name in ("host", "port", "username", "password"):
        if field_name not in data:
            logger.error("smtp section missing required field: '%s'", field_name)
            return None

    if not isinstance(data["port"], int):
        logger.error("smtp.port must be an integer, got: %s", type(data["port"]).__name__)
        return None

    return SmtpConfig(
        host=data["host"],
        port=data["port"],
        username=data["username"],
        password=data["password"],
        use_tls=data.get("use_tls", True),
    )


def _parse_email(data: dict) -> EmailConfig | None:
    for field_name in ("from_address", "to_address"):
        if field_name not in data or not data[field_name]:
            logger.error("email section missing required field: '%s'", field_name)
            return None

    return EmailConfig(
        from_address=data["from_address"],
        to_address=data["to_address"],
        subject_prefix=data.get("subject_prefix", "[Archive Scanner]"),
    )


def _parse_relationships(data: list) -> list[Relationship]:
    if not isinstance(data, list) or not data:
        logger.error("relationships must be a non-empty list")
        return []

    valid = []

    for i, rel in enumerate(data):
        if not isinstance(rel, dict):
            logger.error("relationships[%d] is not an object", i)
            continue

        site = rel.get("site")
        tag = rel.get("tag")

        if not site or not tag:
            logger.error("relationships[%d] missing 'site' or 'tag'", i)
            continue

        track_from_raw = rel.get("track_from")

        if not track_from_raw:
            logger.error(
                "Relationship '%s:%s' missing track_from — "
                "this field is required to prevent flooding on first run",
                site, tag,
            )
            continue

        try:
            track_from = datetime.fromisoformat(track_from_raw)
        except (ValueError, TypeError) as e:
            logger.error(
                "Relationship '%s:%s' has invalid track_from '%s': %s",
                site, tag, track_from_raw, e,
            )
            continue

        valid.append(Relationship(site=site, tag=tag, track_from=track_from))

    return valid


def _parse_storage(data: dict) -> StorageConfig:
    mode = data.get("mode", "json")

    if mode not in ("json", "sqlite"):
        logger.warning(
            "Unrecognised storage mode '%s', defaulting to 'json'", mode
        )
        mode = "json"

    sqlite_path = data.get("sqlite_path", "")

    if mode == "sqlite" and not sqlite_path:
        logger.warning(
            "storage.mode is 'sqlite' but sqlite_path is empty, defaulting to 'json'"
        )
        mode = "json"

    return StorageConfig(mode=mode, sqlite_path=sqlite_path)


def _parse_search(data: dict) -> SearchConfig:
    max_pages = data.get("max_pages", 2)
    delay = data.get("delay_between_requests_seconds", 3)

    if not isinstance(max_pages, int) or max_pages < 1:
        logger.warning("search.max_pages must be a positive integer, defaulting to 2")
        max_pages = 2

    if not isinstance(delay, int) or delay < 0:
        logger.warning(
            "search.delay_between_requests_seconds must be a non-negative integer, "
            "defaulting to 3"
        )
        delay = 3

    return SearchConfig(max_pages=max_pages, delay_between_requests_seconds=delay)
