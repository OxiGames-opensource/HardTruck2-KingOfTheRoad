# Build Guide

This document describes how to build release binaries for `OxiGames Patcher`.

## Source Files

```text
app/tools/patcher/core.py
app/tools/patcher/run.py
app/tools/patcher/gui.py
```

## Requirements

- Python 3.10+
- PyInstaller

Install PyInstaller:

```bash
python3 -m pip install pyinstaller
```

## CLI Linux Build

From repository root:

```bash
pyinstaller \
    --onefile \
    --name OxiGames-HardTruck2-Patcher-cli-linux-x64 \
    app/tools/patcher/run.py
```

## CLI Windows Build

On Windows:

```powershell
pyinstaller `
    --onefile `
    --name OxiGames-HardTruck2-Patcher-cli-windows-x64 `
    app/tools/patcher/run.py
```

## Future GUI Linux Build

```bash
pyinstaller \
    --onefile \
    --windowed \
    --name OxiGames-HardTruck2-Patcher-linux-x64 \
    app/tools/patcher/gui.py
```

## Future GUI Windows Build

```powershell
pyinstaller `
    --onefile `
    --windowed `
    --name OxiGames-HardTruck2-Patcher-windows-x64 `
    app/tools/patcher/gui.py
```

## Release Assets

Recommended release artifacts:

```text
OxiGames-HardTruck2-Patcher-linux-x64.zip
OxiGames-HardTruck2-Patcher-windows-x64.zip
checksums.txt
```

Each platform archive should include:

```text
patcher binary
app/patches/
README.md
```

## Notes

Do not include original game files in release assets.
