#!/usr/bin/env python3
from __future__ import annotations

"""
GUI placeholder for the next step.

The patching logic has been moved to core.py.
This file will become the Tkinter-based community-friendly interface.
"""

from core import default_patches_dir, load_all_patches


def main() -> int:
    patches = load_all_patches(default_patches_dir())

    print("OxiGames Patcher GUI placeholder")
    print("")
    print("Available patches:")

    for patch in patches:
        print(f"- {patch.patch_id}: {patch.title}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
