import logging
import os
import time
from random import randint

from priconne.ugly.accounts import new_account
from priconne.ugly.client import Client

logger = logging.getLogger("command")

def cmd_register(discord_user_id: str, viewer_id: int, password: str):
    viewer_id = int(viewer_id)

    logger.debug(f"Creating new device profile for discord user {discord_user_id}…")
    c = new_account()
    delay()

    logger.debug(f"Linking with {viewer_id}:{password}…")
    c.link_account(viewer_id, password)
    delay()

    logger.debug("Logging in…")
    c.login()
    delay()

    state_file_path = f"state/{discord_user_id}.json"
    logger.debug(f"Saving to state file {state_file_path}")
    os.makedirs("state", exist_ok=True)
    c.set_state_file(state_file_path)
    c.flush_state()

    return c.misc["user_data"]

def cmd_login(discord_user_id: str):
    state_file_path = f"state/{discord_user_id}.json"
    logger.debug(f"Loading from state file {state_file_path}")
    c = Client.from_state_file(state_file_path)

    logger.debug("Logging in…")
    c.login()

    return c.misc["user_data"]

def cmd_check(discord_user_id: str):
    state_file_path = f"state/{discord_user_id}.json"
    return os.path.exists(state_file_path)

def cmd_disable(discord_user_id: str):
    state_file_path = f"state/{discord_user_id}.json"
    file_exists = os.path.exists(state_file_path)

    if (file_exists):
        unix_timestamp = int(time.time())
        new_file_path = f"state/{discord_user_id}-disabled-{unix_timestamp}.json"
        os.rename(state_file_path, new_file_path)
        return True

    return False

# ------------------------------------------------------------------------------

def delay():
    time.sleep(randint(500,1000) / 1000)
