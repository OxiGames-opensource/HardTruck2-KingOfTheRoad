# DumpDataAroundAddress

## Purpose

`DumpDataAroundAddress` produces a hexadecimal and ASCII dump of memory starting at a specified address.

The script is intended to help inspect:

- binary data;
- string tables;
- resource tables;
- structures;
- arrays;
- memory layouts;
- unknown data regions.

This is one of the core research utilities used during reverse engineering.

## Repository Location

```text
ghidra/scripts/modules/
└── DumpDataAroundAddress/
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

The script accepts two parameters.

### Parameter 1 — Start Address

Supported formats:

```text
00676680
```

```text
0x00676680
```

```text
676680
```

If omitted, the script asks for the address interactively.

### Parameter 2 — Dump Length

The dump size may be specified in hexadecimal or decimal form.

Examples:

```text
0x220
```

```text
544
```

If omitted, the script asks for the size interactively.

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
    -postScript modules/DumpDataAroundAddress/run.java 00676680 0x220
```

Equivalent decimal example:

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/DumpDataAroundAddress/run.java 00676680 544
```

## Output

The script prints a classic hexadecimal dump.

Each line contains:

- address;
- hexadecimal bytes;
- printable ASCII representation.

Example:

```text
=== Dump Data Around Address ===

Start address : 00676680
Length        : 0x220 (544 bytes)

00676680  6c 6f 61 64 70 69 78 2e 74 78 72 00 32 2e 72 65  loadpix.txr.2.re
00676690  73 00 00 00 33 2e 72 65 73 00 00 00 31 2e 72 65  s...3.res...1.re
...
```

## Summary

At the end of execution the script reports:

- start address;
- dumped bytes;
- dumped lines.

Example:

```text
=== Summary ===

Start address: 00676680
Bytes dumped: 544
Lines dumped: 34

[OK] Done.
```

## Result Files

Every execution creates a log file inside:

```text
ghidra/scripts/modules/DumpDataAroundAddress/result/
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

This utility is typically used after locating an interesting address.

Common investigation sequence:

1. Locate a string with `FindStringRefs`.
2. Find callers using `FindRefsToAddress`.
3. Inspect nearby memory with `DumpDataAroundAddress`.
4. Continue reverse engineering using the discovered data.

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