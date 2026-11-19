import logging
import os
import sys

from Utilities.logging_setup import setup_logging
from Utilities.config import load_config
from State import get_state_backend

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger("archive_scanner.main")


def main():
    setup_logging(SCRIPT_DIR)
    logger.info("Archive Scanner starting")

    config = load_config(os.path.join(SCRIPT_DIR, "config.json"))

    if config is None:
        logger.error("Failed to load configuration, exiting")
        sys.exit(1)

    logger.info("Configuration loaded successfully")
    logger.info("Storage mode: %s", config.storage.mode)
    logger.info("Relationships configured: %d", len(config.relationships))

    state = get_state_backend(config, SCRIPT_DIR)
    logger.info("State backend initialised: %s", type(state).__name__)

    # TODO: Phase 2 — Adapter initialisation and polling loop
    # TODO: Phase 3 — Email digest

    logger.info("Archive Scanner finished")


if __name__ == "__main__":
    main()
