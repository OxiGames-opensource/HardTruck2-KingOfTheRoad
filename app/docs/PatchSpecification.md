# Patch Format

This document defines the standard patch format used across OxiGames projects.

The goal is to ensure that every compatibility patch is:

- reproducible
- documented
- verifiable
- safe to apply
- safe to rollback whenever possible

---

# Patch Structure

Each compatibility patch should reside in its own directory.

Example:

```text
app/
└── patches/
    └── texture-memory/
        ├── README.md
        └── patch.json
```

---

# Patch Documentation

Each patch should include a `README.md` describing:

- problem
- symptoms
- root cause
- affected game versions
- technical explanation
- validation procedure
- rollback information

The documentation should be understandable without requiring external resources.

---

# Patch Definition

Each patch is described by a `patch.json` file.

Example:

```json
{
    "id": "texture-memory",
    "title": "Texture Memory Compatibility Fix",
    "status": "stable",
    "category": "compatibility",

    "targets": [
        {
            "platform": "windows",
            "game_version": "Steam",
            "file": "king.exe",
            "signature": "F7 D8 1B C0 F7 D8 85 C0",
            "replace":   "B8 01 00 00 00 85 C0 90"
        }
    ]
}
```

---

# Required Fields

## id

Stable unique identifier.

Example:

```json
"id": "texture-memory"
```

---

## title

Human-readable patch name.

Example:

```json
"title": "Texture Memory Compatibility Fix"
```

---

## status

Patch maturity.

Allowed values:

```text
stable
experimental
research
deprecated
```

---

## category

Patch category.

Recommended values:

```text
compatibility
startup
graphics
audio
input
filesystem
linux
windows
research
```

---

## targets

List of supported game executables or files.

A patch may support multiple game editions.

---

# Target Fields

## platform

Target platform.

Allowed values:

```text
windows
linux
proton
wine
all
```

---

## game_version

Known game edition.

Examples:

```text
Steam
GOG
Retail
Unknown
```

---

## file

Relative path inside the game installation.

Example:

```json
"file": "king.exe"
```

---

## signature

Original byte signature used to locate the patch.

The patcher should search for this signature before modifying the executable.

---

## replace

Replacement byte sequence.

Unless explicitly supported, replacement bytes must have the same length as the signature.

---

# Safety Rules

A patching tool should always:

- verify the executable version before patching
- verify that the signature exists
- refuse to patch if the signature is not found
- refuse to patch if the signature is found multiple times unless explicitly allowed
- create a backup before modifying any file
- support rollback whenever possible
- never distribute original game files

---

# Patch Status

## Stable

Fully tested and recommended for normal use.

---

## Experimental

Functionally works but requires additional testing.

---

## Research

Used for investigation purposes only.

Not intended for end users.

---

## Deprecated

Retained for documentation and historical reference.

Not recommended for new installations.

---

# Notes

Raw offsets may be included for documentation purposes.

Example:

```json
"offset": "0x1155BE"
```

However, compatibility patches should prefer **signature-based matching** over fixed offsets whenever possible.

Signature matching is significantly more reliable across different executable builds and distributions.