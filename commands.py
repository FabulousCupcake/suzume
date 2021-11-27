import boto3
from botocore.exceptions import ClientError
import logging
import os
import time
from random import randint

from priconne.ugly.accounts import new_account
from priconne.ugly.client import Client

S3_BUCKET_NAME = "priconne-vanilla-statefiles"

logger = logging.getLogger("command")

def cmd_register(discord_user_id: str, viewer_id: int, password: str):
    viewer_id = int(viewer_id)

    logger.debug(f"Creating new device profile for discord user {discord_user_id}…")
    c = new_account()

    logger.debug(f"Linking with {viewer_id}:{password}…")
    c.link_account(viewer_id, password)

    logger.debug("Logging in…")
    c.login()

    state_file_path = f"/tmp/{discord_user_id}.json"
    logger.debug(f"Saving to state file {state_file_path}")
    c.set_state_file(state_file_path)
    c.flush_state()
    upload_to_s3(discord_user_id)

    return c.misc["user_data"]

def cmd_login(discord_user_id: str):
    state_file_path = f"state/{discord_user_id}.json"
    logger.debug(f"Loading from state file {state_file_path}")
    c = Client.from_state_file(state_file_path)

    logger.debug("Logging in…")
    c.login()
    upload_to_s3(discord_user_id)

    return c.misc["user_data"]

def cmd_check(discord_user_id: str):
    download_from_s3(discord_user_id)
    state_file_path = f"state/{discord_user_id}.json"
    return os.path.exists(state_file_path)

def cmd_disable(discord_user_id: str):
    download_from_s3(discord_user_id)
    state_file_path = f"state/{discord_user_id}.json"
    file_exists = os.path.exists(state_file_path)

    if (file_exists):
        disable_in_s3(discord_user_id)
        return True

    return False

# ------------------------------------------------------------------------------

def upload_to_s3(discord_user_id: str):
    filename = f"{discord_user_id}.json"
    filepath = f"/tmp/{filename}"

    s3 = boto3.resource('s3')
    s3.Object(S3_BUCKET_NAME, filename).upload_file(filepath)

def download_from_s3(discord_user_id: str):
    filename = f"{discord_user_id}.json"
    filepath = f"/tmp/{filename}"

    s3 = boto3.resource('s3')

    try:
        s3.Object(S3_BUCKET_NAME, filename).download_file(filepath)
    except ClientError as e:
        if e.response["Error"]["Message"] == "Not Found":
            logger.info(f"{filename} not found in s3")
            return false


def disable_in_s3(discord_user_id: str):
    unix_timestamp = int(time.time())
    filename_disabled = f"{discord_user_id}-disabled-{unix_timestamp}.json"
    filename_original = f"{discord_user_id}.json"

    s3 = boto3.resource('s3')
    s3.Object(S3_BUCKET_NAME, filename_disabled).copy_from(CopySource={
        "Bucket": S3_BUCKET_NAME,
        "Key": filename_original,
    })
    s3.Object(S3_BUCKET_NAME, filename_original).delete()
