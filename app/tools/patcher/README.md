# OxiGames Patcher

`OxiGames Patcher` applies and rolls back binary compatibility patches described by `patch.json` files.

The patcher is intended to be used only with legally obtained copies of supported games.

## Purpose

The patcher provides a reproducible way to:

- list available patches;
- inspect patch status;
- apply selected patches;
- apply all available patches;
- rollback selected patches byte-by-byte;
- rollback all patches byte-by-byte;
- create a backup before the first modification;
- restore the original executable from backup;
- verify bytes before patching or rolling back;
- avoid distributing original game files.

## Repository Location

```text
app/tools/patcher/
├── README.md
├── Build.md
└── run.py
```

## Patch Location

The patcher expects patch directories in:

```text
app/patches/
```

Each patch directory must contain:

```text
README.md
patch.json
```

## Backup Model

Before applying the first patch to a target file, the patcher creates a backup next to it.

Backup filename format:

```text
<file>.oxigames-backup
```

Example:

```text
king.exe.oxigames-backup
```

The backup is created only if it does not already exist.

This means:

- the first patching operation preserves the pre-OxiGames state;
- later apply/rollback operations do not overwrite the backup;
- `restore-original` restores the entire file from the backup.

## Rollback Model

`rollback` does not restore the whole file from backup.

Instead, it reverses selected patches byte-by-byte:

```text
newBytes -> oldBytes
```

This allows independent patch management.

Example:

```text
Apply A
Apply B
Rollback A
Result: B remains applied
```

To restore the whole original executable, use:

```text
restore-original
```

## Basic Usage

Run from the repository root.

### List Patches

```bash
python3 app/tools/patcher/run.py list
```

### Show Patch Status

```bash
python3 app/tools/patcher/run.py status     --game "/path/to/Hard Truck 2 King of the Road"     --all
```

### Apply Selected Patches

```bash
python3 app/tools/patcher/run.py apply     --game "/path/to/Hard Truck 2 King of the Road"     DisplayModeDetection TextureMemory
```

### Apply All Patches

```bash
python3 app/tools/patcher/run.py apply     --game "/path/to/Hard Truck 2 King of the Road"     --all
```

### Rollback Selected Patches

```bash
python3 app/tools/patcher/run.py rollback     --game "/path/to/Hard Truck 2 King of the Road"     DisplayModeDetection
```

### Rollback All Patches

```bash
python3 app/tools/patcher/run.py rollback     --game "/path/to/Hard Truck 2 King of the Road"     --all
```

### Restore Original File From Backup

```bash
python3 app/tools/patcher/run.py restore-original     --game "/path/to/Hard Truck 2 King of the Road"
```

## Game Path

`--game` can point either to:

- the game directory;
- the target executable itself.

Examples:

```bash
--game "/path/to/Hard Truck 2 King of the Road"
```

```bash
--game "/path/to/Hard Truck 2 King of the Road/king.exe"
```

## Status Values

The patcher can report:

```text
original
```

The current bytes match `oldBytes`.

```text
patched
```

The current bytes match `newBytes`.

```text
unknown
```

The bytes are neither original nor patched.

This usually means the executable is from a different version or was modified by another tool.

## Safety Rules

The patcher:

- never includes original game files;
- checks `oldBytes` before applying a patch;
- checks `newBytes` before rolling back a patch;
- refuses to patch unknown bytes by default;
- refuses to rollback unknown bytes by default;
- creates a backup before the first modification;
- never overwrites an existing backup;
- can restore the full file from backup;
- applies only patch data described in repository metadata.

## Legal Notice

This tool is intended only for compatibility and preservation work.

It does not bypass DRM, distribute copyrighted game files, or replace original game content.
