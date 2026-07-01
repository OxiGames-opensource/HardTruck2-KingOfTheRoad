# Build Guide

This document describes how to build release binaries for `OxiGames Patcher`.

The source of truth is:

```text
app/tools/patcher/run.py
```

## Requirements

- Python 3.10+
- PyInstaller

Install PyInstaller:

```bash
python3 -m pip install pyinstaller
```

## Linux Build

From repository root:

```bash
pyinstaller     --onefile     --name OxiGames-HardTruck2-Patcher-linux-x64     app/tools/patcher/run.py
```

Output:

```text
dist/OxiGames-HardTruck2-Patcher-linux-x64
```

## Windows Build

On Windows:

```powershell
pyinstaller `
    --onefile `
    --name OxiGames-HardTruck2-Patcher-windows-x64 `
    app/tools/patcher/run.py
```

Output:

```text
dist/OxiGames-HardTruck2-Patcher-windows-x64.exe
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
