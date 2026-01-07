#!/usr/bin/env python3
"""
Command-line entry point for AIWork TUI.

Usage:
    aiwork-tui                  # Run in demo mode
    aiwork-tui --mode demo      # Run in demo mode (auto-cycle)
    aiwork-tui --mode interactive  # Run in interactive mode (future)
"""

import sys
from aiwork.tui.app import main

if __name__ == "__main__":
    sys.exit(main())
