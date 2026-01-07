#!/usr/bin/env python3
"""
Demo script to showcase the AIWork TUI.

This script runs the TUI for a longer duration to demonstrate
the different views and features.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from aiwork.tui.app import AIWorkTUI

if __name__ == "__main__":
    print("🚀 Starting AIWork TUI Demo...")
    print("📺 The TUI will auto-cycle through different views")
    print("💡 Press Ctrl+C to stop\n")
    
    tui = AIWorkTUI()
    tui.run(mode="demo")
