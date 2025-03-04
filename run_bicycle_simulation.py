#!/usr/bin/env python3
"""
Run script for the Bicycle Simulation game.
Simply execute this file to start the game.
"""

import os
import sys

# Check if matplotlib is installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Warning: matplotlib is not installed. Performance graphs will not be available.")
    print("You can install it with: pip install matplotlib")
    print("Continuing without graphing capability...\n")

# Import the simulation game
try:
    from bicycle_simulation_game import main

    # Run the game
    if __name__ == "__main__":
        main()
except ImportError:
    print("Error: Could not import bicycle_simulation_game module.")
    print("Make sure both files are in the same directory and named correctly:")
    print("  - bicycle_simulation_game.py")
    print("  - run_bicycle_simulation.py (this file)")
    sys.exit(1)