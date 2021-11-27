import json
import logging
import sys

from commands import cmd_login, cmd_register, cmd_check, cmd_disable

COMMAND_MAP = {
    "login": cmd_login,
    "register": cmd_register,
    "check": cmd_check,
    "disable": cmd_disable,
}

def main(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Parse arguments
    command = event["command"]
    command_params = event["args"]

    command_func = COMMAND_MAP.get(command)
    if (command_func == None):
        retval = f"Command {command} not found"
        logger.warning(retval)
        print(retval)
        sys.exit(1)

    logger.info(f"Executing {command} with params {command_params}")
    return command_func(*command_params)

if __name__ == "__main__":
    event = {
        "command": sys.argv[1],
        "args": sys.argv[2:],
    }
    context = {}
    result = main(event, context)
    print(json.dumps(result))
