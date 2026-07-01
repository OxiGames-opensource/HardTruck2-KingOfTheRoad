#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BACKUP_SUFFIX = ".oxigames-backup"


class PatcherError(RuntimeError):
    pass


@dataclass(frozen=True)
class BytePatch:
    patch_id: str
    title: str
    target_file: str
    virtual_address: str
    file_offset: int
    section: str
    old_bytes: bytes
    new_bytes: bytes
    size: int


@dataclass(frozen=True)
class PatchDefinition:
    patch_id: str
    title: str
    description: str
    path: Path
    byte_patches: list[BytePatch]


def info(message: str) -> None:
    print(f"[INFO] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def warn(message: str) -> None:
    print(f"[WARN] {message}")


def fail(message: str) -> None:
    print(f"[ERROR] {message}")


def parse_hex_bytes(value: str) -> bytes:
    try:
        return bytes.fromhex(value)
    except ValueError as exc:
        raise PatcherError(f"Invalid hex byte string: {value}") from exc


def parse_int(value: str | int) -> int:
    if isinstance(value, int):
        return value

    text = value.strip()

    if text.lower().startswith("0x"):
        return int(text, 16)

    return int(text, 10)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_patches_dir() -> Path:
    return repository_root() / "app" / "patches"


def require_string(data: dict, key: str, source: Path) -> str:
    value = data.get(key)

    if not isinstance(value, str) or not value.strip():
        raise PatcherError(f"Missing string key '{key}' in {source}")

    return value.strip()


def load_patch_definition(path: Path) -> PatchDefinition:
    patch_json_path = path / "patch.json"

    if not patch_json_path.exists():
        raise PatcherError(f"Missing patch.json: {patch_json_path}")

    data = json.loads(patch_json_path.read_text(encoding="utf-8"))

    patch_id = require_string(data, "id", patch_json_path)
    title = require_string(data, "title", patch_json_path)
    description = str(data.get("description", ""))

    target = data.get("target")

    if not isinstance(target, dict):
        raise PatcherError(f"Missing target object in {patch_json_path}")

    target_file = require_string(target, "file", patch_json_path)

    raw_patches = data.get("patches")

    if not isinstance(raw_patches, list) or not raw_patches:
        raise PatcherError(f"Missing patches list in {patch_json_path}")

    byte_patches: list[BytePatch] = []

    for index, raw_patch in enumerate(raw_patches):
        if not isinstance(raw_patch, dict):
            raise PatcherError(f"Invalid patch entry #{index} in {patch_json_path}")

        patch_type = raw_patch.get("type")

        if patch_type != "bytes":
            raise PatcherError(f"Unsupported patch type in {patch_json_path}: {patch_type}")

        old_bytes = parse_hex_bytes(require_string(raw_patch, "oldBytes", patch_json_path))
        new_bytes = parse_hex_bytes(require_string(raw_patch, "newBytes", patch_json_path))
        size = parse_int(raw_patch.get("size", len(old_bytes)))

        if len(old_bytes) != size:
            raise PatcherError(
                f"oldBytes size mismatch in {patch_json_path}: expected {size}, got {len(old_bytes)}"
            )

        if len(new_bytes) != size:
            raise PatcherError(
                f"newBytes size mismatch in {patch_json_path}: expected {size}, got {len(new_bytes)}"
            )

        if "fileOffset" not in raw_patch:
            raise PatcherError(f"Missing fileOffset in {patch_json_path}")

        byte_patches.append(
            BytePatch(
                patch_id=patch_id,
                title=title,
                target_file=target_file,
                virtual_address=str(raw_patch.get("virtualAddress", "")),
                file_offset=parse_int(raw_patch["fileOffset"]),
                section=str(raw_patch.get("section", "")),
                old_bytes=old_bytes,
                new_bytes=new_bytes,
                size=size,
            )
        )

    return PatchDefinition(
        patch_id=patch_id,
        title=title,
        description=description,
        path=path,
        byte_patches=byte_patches,
    )


def load_all_patches(patches_dir: Path) -> list[PatchDefinition]:
    if not patches_dir.exists():
        raise PatcherError(f"Patches directory does not exist: {patches_dir}")

    patches: list[PatchDefinition] = []

    for child in sorted(patches_dir.iterdir()):
        if not child.is_dir():
            continue

        patch_json = child / "patch.json"

        if not patch_json.exists():
            continue

        patches.append(load_patch_definition(child))

    return patches


def select_patches(
    patches: list[PatchDefinition],
    selected_ids: Iterable[str],
    select_all: bool,
) -> list[PatchDefinition]:
    if select_all:
        return patches

    selected = list(selected_ids)

    if not selected:
        raise PatcherError("No patches selected. Pass patch ids or use --all.")

    by_id = {patch.patch_id: patch for patch in patches}
    result: list[PatchDefinition] = []

    for patch_id in selected:
        if patch_id not in by_id:
            available = ", ".join(sorted(by_id))
            raise PatcherError(f"Unknown patch id: {patch_id}. Available patches: {available}")

        result.append(by_id[patch_id])

    return result


def unique_target_files(patches: list[PatchDefinition]) -> list[str]:
    seen: set[str] = set()
    files: list[str] = []

    for patch in patches:
        for byte_patch in patch.byte_patches:
            if byte_patch.target_file in seen:
                continue

            seen.add(byte_patch.target_file)
            files.append(byte_patch.target_file)

    return files


def resolve_target_file(game_path: Path, target_file: str) -> Path:
    if game_path.is_file():
        if game_path.name.lower() != target_file.lower():
            raise PatcherError(
                f"Game path points to a file, but expected {target_file}: {game_path}"
            )

        return game_path

    if game_path.is_dir():
        candidate = game_path / target_file

        if candidate.exists():
            return candidate

        raise PatcherError(f"Target file not found: {candidate}")

    raise PatcherError(f"Game path does not exist: {game_path}")


def read_bytes(path: Path, offset: int, size: int) -> bytes:
    with path.open("rb") as handle:
        handle.seek(offset)
        data = handle.read(size)

    if len(data) != size:
        raise PatcherError(
            f"Unable to read {size} bytes at offset 0x{offset:x} from {path}"
        )

    return data


def write_bytes(path: Path, offset: int, data: bytes) -> None:
    with path.open("r+b") as handle:
        handle.seek(offset)
        handle.write(data)


def backup_path(path: Path) -> Path:
    return path.with_name(path.name + BACKUP_SUFFIX)


def ensure_backup(path: Path) -> Path:
    backup = backup_path(path)

    if backup.exists():
        info(f"Backup already exists: {backup}")
        return backup

    shutil.copy2(path, backup)
    info(f"Backup created: {backup}")

    return backup


def patch_status(path: Path, byte_patch: BytePatch) -> str:
    current = read_bytes(path, byte_patch.file_offset, byte_patch.size)

    if current == byte_patch.old_bytes:
        return "original"

    if current == byte_patch.new_bytes:
        return "patched"

    return "unknown"


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
    patches = select_patches(
        load_all_patches(args.patches_dir),
        args.patch_ids,
        args.all,
    )

    for patch in patches:
        print("")
        print(f"=== {patch.patch_id} ===")

        for byte_patch in patch.byte_patches:
            target = resolve_target_file(args.game, byte_patch.target_file)
            status = patch_status(target, byte_patch)

            print(f"Target: {target}")
            print(f"VA: {byte_patch.virtual_address}")
            print(f"Offset: 0x{byte_patch.file_offset:x}")
            print(f"Status: {status}")

    return 0


def command_apply(args: argparse.Namespace) -> int:
    patches = select_patches(
        load_all_patches(args.patches_dir),
        args.patch_ids,
        args.all,
    )

    for patch in patches:
        print("")
        print(f"=== Applying {patch.patch_id} ===")

        for byte_patch in patch.byte_patches:
            target = resolve_target_file(args.game, byte_patch.target_file)
            status = patch_status(target, byte_patch)

            info(f"Target: {target}")
            info(f"Offset: 0x{byte_patch.file_offset:x}")
            info(f"Status: {status}")

            if status == "patched":
                ok("Already patched.")
                continue

            if status != "original":
                raise PatcherError(
                    f"Unexpected bytes at offset 0x{byte_patch.file_offset:x}. "
                    "Refusing to patch unknown file state."
                )

            ensure_backup(target)
            write_bytes(target, byte_patch.file_offset, byte_patch.new_bytes)

            new_status = patch_status(target, byte_patch)

            if new_status != "patched":
                raise PatcherError(f"Patch verification failed: {patch.patch_id}")

            ok("Patch applied.")

    ok("Done.")
    return 0


def command_rollback(args: argparse.Namespace) -> int:
    patches = select_patches(
        load_all_patches(args.patches_dir),
        args.patch_ids,
        args.all,
    )

    for patch in patches:
        print("")
        print(f"=== Rolling back {patch.patch_id} ===")

        for byte_patch in patch.byte_patches:
            target = resolve_target_file(args.game, byte_patch.target_file)
            status = patch_status(target, byte_patch)

            info(f"Target: {target}")
            info(f"Offset: 0x{byte_patch.file_offset:x}")
            info(f"Status: {status}")

            if status == "original":
                ok("Already original.")
                continue

            if status != "patched":
                raise PatcherError(
                    f"Unexpected bytes at offset 0x{byte_patch.file_offset:x}. "
                    "Refusing to rollback unknown file state."
                )

            write_bytes(target, byte_patch.file_offset, byte_patch.old_bytes)

            new_status = patch_status(target, byte_patch)

            if new_status != "original":
                raise PatcherError(f"Rollback verification failed: {patch.patch_id}")

            ok("Patch rolled back.")

    ok("Done.")
    return 0


def command_restore_original(args: argparse.Namespace) -> int:
    patches = load_all_patches(args.patches_dir)
    target_files = unique_target_files(patches)

    if not target_files:
        warn("No target files found in patch definitions.")
        return 0

    restored = 0

    for target_file in target_files:
        target = resolve_target_file(args.game, target_file)
        backup = backup_path(target)

        print("")
        print(f"=== Restoring {target_file} ===")
        info(f"Target: {target}")
        info(f"Backup: {backup}")

        if not backup.exists():
            warn("Backup not found.")
            continue

        shutil.copy2(backup, target)
        restored += 1
        ok("Original file restored from backup.")

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
    parser.add_argument(
        "patch_ids",
        nargs="*",
        help="Patch ids to process.",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all available patches.",
    )


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
