# OxiGames Patcher

`OxiGames Patcher` applies and rolls back binary compatibility patches described by `patch.json` files.

The patcher is intended to be used only with legally obtained copies of supported games.

## Repository Location

```text
app/tools/patcher/
├── README.md
├── Build.md
├── core.py
├── gui.py
└── run.py
```

## Architecture

The patcher is split into three layers.

### `core.py`

Contains the patching logic:

- patch metadata loading;
- target file resolution;
- byte status detection;
- backup creation;
- patch application;
- byte-level rollback;
- full restore from backup.

`core.py` does not print CLI output and does not depend on GUI code.

### `run.py`

Command-line interface.

It parses arguments, calls `core.py`, and prints human-readable output.

### `gui.py`

GUI entry point.

At this stage it is a placeholder for the upcoming Tkinter interface.

The GUI will use the same `core.py` logic as the CLI.

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

## Rollback Model

`rollback` does not restore the whole file from backup.

Instead, it reverses selected patches byte-by-byte:

```text
newBytes -> oldBytes
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
python3 app/tools/patcher/run.py status \
    --game "/path/to/Hard Truck 2 King of the Road" \
    --all
```

### Apply Selected Patches

```bash
python3 app/tools/patcher/run.py apply \
    --game "/path/to/Hard Truck 2 King of the Road" \
    DisplayModeDetection TextureMemory
```

### Apply All Patches

```bash
python3 app/tools/patcher/run.py apply \
    --game "/path/to/Hard Truck 2 King of the Road" \
    --all
```

### Rollback Selected Patches

```bash
python3 app/tools/patcher/run.py rollback \
    --game "/path/to/Hard Truck 2 King of the Road" \
    DisplayModeDetection
```

### Rollback All Patches

```bash
python3 app/tools/patcher/run.py rollback \
    --game "/path/to/Hard Truck 2 King of the Road" \
    --all
```

### Restore Original File From Backup

```bash
python3 app/tools/patcher/run.py restore-original \
    --game "/path/to/Hard Truck 2 King of the Road"
```

## GUI Preview

For now:

```bash
python3 app/tools/patcher/gui.py
```

This only verifies that the future GUI entry point can load patch definitions through `core.py`.

## Legal Notice

This tool is intended only for compatibility and preservation work.

It does not bypass DRM, distribute copyrighted game files, or replace original game content.
