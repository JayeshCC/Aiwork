"""Module entry point for the AIWork API server."""

import sys

from .server import main


if __name__ == "__main__":
    main(sys.argv[1:])
