#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core import (
    PatcherError,
    apply_patches,
    default_patches_dir,
    get_status,
    load_all_patches,
    restore_original,
    rollback_patches,
    select_patches,
)


def info(message: str) -> None:
    print(f"[INFO] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def warn(message: str) -> None:
    print(f"[WARN] {message}")


def fail(message: str) -> None:
    print(f"[ERROR] {message}")


def command_list(args: argparse.Namespace) -> int:
    patches = load_all_patches(args.patches_dir)

    if not patches:
        warn("No patches found.")
        return 0

    for patch in patches:
        print(f"{patch.patch_id}: {patch.title}")
        if patch.description:
            print(f"  {patch.description}")

    return 0


def command_status(args: argparse.Namespace) -> int:
    patches = select_patches(load_all_patches(args.patches_dir), args.patch_ids, args.all)

    for status in get_status(args.game, patches):
        print("")
        print(f"=== {status.patch_id} ===")
        print(f"Target: {status.target}")
        print(f"VA: {status.virtual_address}")
        print(f"Offset: 0x{status.file_offset:x}")
        print(f"Status: {status.status}")

    return 0


def command_apply(args: argparse.Namespace) -> int:
    patches = select_patches(load_all_patches(args.patches_dir), args.patch_ids, args.all)
    current_patch_id = None

    for result in apply_patches(args.game, patches):
        if result.patch_id != current_patch_id:
            current_patch_id = result.patch_id
            print("")
            print(f"=== Applying {result.patch_id} ===")

        info(f"Target: {result.target}")
        info(f"Offset: 0x{result.file_offset:x}")
        info(f"Status: {result.previous_status}")
        ok(result.message)

    ok("Done.")
    return 0


def command_rollback(args: argparse.Namespace) -> int:
    patches = select_patches(load_all_patches(args.patches_dir), args.patch_ids, args.all)
    current_patch_id = None

    for result in rollback_patches(args.game, patches):
        if result.patch_id != current_patch_id:
            current_patch_id = result.patch_id
            print("")
            print(f"=== Rolling back {result.patch_id} ===")

        info(f"Target: {result.target}")
        info(f"Offset: 0x{result.file_offset:x}")
        info(f"Status: {result.previous_status}")
        ok(result.message)

    ok("Done.")
    return 0


def command_restore_original(args: argparse.Namespace) -> int:
    patches = load_all_patches(args.patches_dir)
    restored = 0

    for result in restore_original(args.game, patches):
        print("")
        print(f"=== Restoring {result.target.name} ===")
        info(f"Target: {result.target}")
        info(f"Backup: {result.backup}")

        if result.restored:
            restored += 1
            ok(result.message)
        else:
            warn(result.message)

    print("")
    ok(f"Done. Restored files: {restored}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oxigames-patcher",
        description="Apply OxiGames binary compatibility patches.",
    )

    parser.add_argument(
        "--patches-dir",
        type=Path,
        default=default_patches_dir(),
        help="Directory containing patch definitions. Default: app/patches",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List available patches.")
    list_parser.set_defaults(func=command_list)

    status_parser = subparsers.add_parser("status", help="Show patch status.")
    add_game_argument(status_parser)
    add_patch_selection_arguments(status_parser)
    status_parser.set_defaults(func=command_status)

    apply_parser = subparsers.add_parser("apply", help="Apply patches.")
    add_game_argument(apply_parser)
    add_patch_selection_arguments(apply_parser)
    apply_parser.set_defaults(func=command_apply)

    rollback_parser = subparsers.add_parser("rollback", help="Rollback patches byte-by-byte.")
    add_game_argument(rollback_parser)
    add_patch_selection_arguments(rollback_parser)
    rollback_parser.set_defaults(func=command_rollback)

    restore_parser = subparsers.add_parser(
        "restore-original",
        help="Restore original target files from backup.",
    )
    add_game_argument(restore_parser)
    restore_parser.set_defaults(func=command_restore_original)

    return parser


def add_game_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--game",
        type=Path,
        required=True,
        help="Path to the game directory or target executable.",
    )


def add_patch_selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("patch_ids", nargs="*", help="Patch ids to process.")
    parser.add_argument("--all", action="store_true", help="Process all available patches.")


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    args.patches_dir = args.patches_dir.resolve()

    if hasattr(args, "game"):
        args.game = args.game.resolve()

    try:
        return args.func(args)
    except PatcherError as exc:
        fail(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
