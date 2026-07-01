from __future__ import annotations

import json
import shutil
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

@dataclass(frozen=True)
class PatchPointStatus:
    patch_id: str
    title: str
    target: Path
    virtual_address: str
    file_offset: int
    status: str

@dataclass(frozen=True)
class PatchOperationResult:
    patch_id: str
    title: str
    target: Path
    file_offset: int
    previous_status: str
    current_status: str
    message: str

@dataclass(frozen=True)
class RestoreResult:
    target: Path
    backup: Path
    restored: bool
    message: str

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
            raise PatcherError(f"oldBytes size mismatch in {patch_json_path}: expected {size}, got {len(old_bytes)}")
        if len(new_bytes) != size:
            raise PatcherError(f"newBytes size mismatch in {patch_json_path}: expected {size}, got {len(new_bytes)}")
        if "fileOffset" not in raw_patch:
            raise PatcherError(f"Missing fileOffset in {patch_json_path}")
        byte_patches.append(BytePatch(
            patch_id=patch_id,
            title=title,
            target_file=target_file,
            virtual_address=str(raw_patch.get("virtualAddress", "")),
            file_offset=parse_int(raw_patch["fileOffset"]),
            section=str(raw_patch.get("section", "")),
            old_bytes=old_bytes,
            new_bytes=new_bytes,
            size=size,
        ))
    return PatchDefinition(patch_id=patch_id, title=title, description=description, path=path, byte_patches=byte_patches)

def load_all_patches(patches_dir: Path) -> list[PatchDefinition]:
    if not patches_dir.exists():
        raise PatcherError(f"Patches directory does not exist: {patches_dir}")
    patches: list[PatchDefinition] = []
    for child in sorted(patches_dir.iterdir()):
        if not child.is_dir():
            continue
        if not (child / "patch.json").exists():
            continue
        patches.append(load_patch_definition(child))
    return patches

def select_patches(patches: list[PatchDefinition], selected_ids: Iterable[str], select_all: bool) -> list[PatchDefinition]:
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
            raise PatcherError(f"Game path points to a file, but expected {target_file}: {game_path}")
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
        raise PatcherError(f"Unable to read {size} bytes at offset 0x{offset:x} from {path}")
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
        return backup
    shutil.copy2(path, backup)
    return backup

def patch_status(path: Path, byte_patch: BytePatch) -> str:
    current = read_bytes(path, byte_patch.file_offset, byte_patch.size)
    if current == byte_patch.old_bytes:
        return "original"
    if current == byte_patch.new_bytes:
        return "patched"
    return "unknown"

def get_status(game_path: Path, patches: list[PatchDefinition]) -> list[PatchPointStatus]:
    statuses: list[PatchPointStatus] = []
    for patch in patches:
        for byte_patch in patch.byte_patches:
            target = resolve_target_file(game_path, byte_patch.target_file)
            statuses.append(PatchPointStatus(
                patch_id=patch.patch_id,
                title=patch.title,
                target=target,
                virtual_address=byte_patch.virtual_address,
                file_offset=byte_patch.file_offset,
                status=patch_status(target, byte_patch),
            ))
    return statuses

def apply_patches(game_path: Path, patches: list[PatchDefinition]) -> list[PatchOperationResult]:
    results: list[PatchOperationResult] = []
    for patch in patches:
        for byte_patch in patch.byte_patches:
            target = resolve_target_file(game_path, byte_patch.target_file)
            previous_status = patch_status(target, byte_patch)
            if previous_status == "patched":
                results.append(PatchOperationResult(patch.patch_id, patch.title, target, byte_patch.file_offset, previous_status, previous_status, "Already patched."))
                continue
            if previous_status != "original":
                raise PatcherError(f"Unexpected bytes at offset 0x{byte_patch.file_offset:x}. Refusing to patch unknown file state.")
            ensure_backup(target)
            write_bytes(target, byte_patch.file_offset, byte_patch.new_bytes)
            current_status = patch_status(target, byte_patch)
            if current_status != "patched":
                raise PatcherError(f"Patch verification failed: {patch.patch_id}")
            results.append(PatchOperationResult(patch.patch_id, patch.title, target, byte_patch.file_offset, previous_status, current_status, "Patch applied."))
    return results

def rollback_patches(game_path: Path, patches: list[PatchDefinition]) -> list[PatchOperationResult]:
    results: list[PatchOperationResult] = []
    for patch in patches:
        for byte_patch in patch.byte_patches:
            target = resolve_target_file(game_path, byte_patch.target_file)
            previous_status = patch_status(target, byte_patch)
            if previous_status == "original":
                results.append(PatchOperationResult(patch.patch_id, patch.title, target, byte_patch.file_offset, previous_status, previous_status, "Already original."))
                continue
            if previous_status != "patched":
                raise PatcherError(f"Unexpected bytes at offset 0x{byte_patch.file_offset:x}. Refusing to rollback unknown file state.")
            write_bytes(target, byte_patch.file_offset, byte_patch.old_bytes)
            current_status = patch_status(target, byte_patch)
            if current_status != "original":
                raise PatcherError(f"Rollback verification failed: {patch.patch_id}")
            results.append(PatchOperationResult(patch.patch_id, patch.title, target, byte_patch.file_offset, previous_status, current_status, "Patch rolled back."))
    return results

def restore_original(game_path: Path, patches: list[PatchDefinition]) -> list[RestoreResult]:
    results: list[RestoreResult] = []
    for target_file in unique_target_files(patches):
        target = resolve_target_file(game_path, target_file)
        backup = backup_path(target)
        if not backup.exists():
            results.append(RestoreResult(target, backup, False, "Backup not found."))
            continue
        shutil.copy2(backup, target)
        results.append(RestoreResult(target, backup, True, "Original file restored from backup."))
    return results
