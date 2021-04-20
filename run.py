import sys
from traceback import format_exc
import argparse

from dockerfile_source.app import Application
from dockerfile_source.utils import (
    parse_config,
    logger
)

logger = logger(__name__, 'logs')

def main():
    app = Application(logger, parse_config('config.json'))
    parser = argparse.ArgumentParser(
        prog="dockerfile_source",
        description="Python tool for analyzing docker files inside github repos. ",
    )
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument(
        'url',
        nargs = "?",
        help = "URL to remote txt file."
    )
    group.add_argument(
        "--file", "-f",
        help="URI to local txt file.",
    )
    app.parse_repo_file(parser.parse_args())
    app.execute_session()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info('\n[user exit](exiting)')
    except SystemExit:
        pass
    except:
        logger.info(
            '\n[cirtical error](exiting)\n'
            f'traceback => ({format_exc()})'
        )
