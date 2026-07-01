# FindRefsToAddress

## Purpose

`FindRefsToAddress` searches for all references to a specified address in the currently opened Ghidra program.

The script is intended to help identify:

- function callers;
- code paths;
- subsystem entry points;
- shared helper functions;
- binary dependencies;
- patch impact.

This is one of the core research utilities used during reverse engineering.

## Repository Location

```text
ghidra/scripts/modules/
└── FindRefsToAddress/
    ├── README.md
    ├── result/
    │   └── .gitkeep
    └── run.java
```

## Requirements

- Ghidra 12+
- A legally purchased copy of the target game.
- Target executable imported through the standard OxiGames workflow.

## Parameters

The script accepts a single address.

Supported formats:

```text
005279e0
```

```text
0x005279e0
```

```text
5279e0
```

If no argument is provided, the script asks for the address interactively.

## Usage

The standard execution workflow is described in:

```text
ghidra/workspace/README.md
```

Example:

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/FindRefsToAddress/run.java 005279e0
```

## Output

The script reports:

- target address;
- every reference to the address;
- reference type;
- containing function (when available);
- summary.

Example:

```text
=== Find References To Address ===

Target address: 005279e0

REF: 004d7fd1 -> 005279e0
Type: UNCONDITIONAL_CALL
Function: FUN_004d76b0

...

=== Summary ===

Target address: 005279e0
References found: 11

[OK] Done.
```

## Result Files

Every execution creates a log file inside:

```text
ghidra/scripts/modules/FindRefsToAddress/result/
```

Filename format:

```text
YYYY-MM-DD_HH-mm-ss.log
```

Example:

```text
2026-01-02_08-45-50.log
```

Result files are local artifacts and are intentionally excluded from version control.

## Typical Workflow

This script is commonly used after discovering an interesting address.

Typical investigation sequence:

1. Locate an interesting string using `FindStringRefs`.
2. Inspect the referencing code.
3. Identify an interesting function or address.
4. Execute `FindRefsToAddress`.
5. Discover every caller of that address.
6. Continue reverse engineering from the discovered call sites.

## Related Research

Typical usage includes:

```text
research/MovieSubsystem/
research/GpuDetection/
research/TextureMemory/
```

## Related Patch

None.

This script is a research helper and does not modify binaries.

## Legal Notice

This script is intended for use with legally obtained copies of supported games.

It performs analysis only and does not distribute or modify original game files.