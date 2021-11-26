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

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="a",
        format="[%(name)s: %(levelname)s] %(asctime)s — %(message)s",
        datefmt="%a, %d %b %y %H:%M:%S"
    )

    # Parse arguments
    command = sys.argv[1]
    command_params = sys.argv[2:]

    command_func = COMMAND_MAP.get(command)
    if (command_func == None):
        retval = f"Command {command} not found"
        logging.warning(retval)
        print(retval)
        sys.exit(1)

    logging.info(f"Executing {command} with params {command_params}")
    result = command_func(*command_params)
    print(json.dumps(result))
