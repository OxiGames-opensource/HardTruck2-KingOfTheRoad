# TraceStringCallers

## Purpose

`TraceStringCallers` traces the execution path from a string to the functions that ultimately call the code using that string.

The script performs the following steps:

1. Finds a string matching the requested text.
2. Finds every reference to that string.
3. Determines the function containing each reference.
4. Finds every caller of those functions.

This utility is intended to quickly discover how a particular resource, message or subsystem is reached during program execution.

Typical targets include:

- error messages;
- warning messages;
- resource names;
- configuration strings;
- menu text;
- subsystem identifiers.

## Repository Location

```text
ghidra/scripts/modules/
└── TraceStringCallers/
    ├── README.md
    ├── result/
    │   └── .gitkeep
    └── run.java
```

## Requirements

- Ghidra 12+
- A legally purchased copy of the target game.
- Target executable imported using the standard OxiGames workflow.

## Parameters

### Parameter 1 — Search Text

The string or substring to search for.

Example:

```text
Your computer does not have graphic accelerator
```

If omitted, the script requests the value interactively.

### Optional Parameter — `--ignore-case`

Enables case-insensitive matching.

Example:

```text
--ignore-case
```

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
    -postScript modules/TraceStringCallers/run.java \
    "Your computer does not have graphic accelerator"
```

Case-insensitive example:

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/TraceStringCallers/run.java \
    "your computer does not have graphic accelerator" \
    --ignore-case
```

## Output

The script reports:

- matched string;
- every reference to the string;
- reference type;
- containing function;
- function entry point;
- callers of that function;
- caller function information.

Example:

```text
=== Trace String Callers ===

STRING: 00676d98 = Your computer does not have graphic accelerator

XREF FROM: 00515db1
Reference type: DATA
Function: FUN_00515ca0
Function entry: 00515ca0

  CALLER XREF: 005284a3
    Type: UNCONDITIONAL_CALL
    Function: FUN_00527f30
    Function entry: 00527f30
```

## Summary

At the end of execution the script reports:

- matched strings;
- string references;
- containing functions;
- callers found.

Example:

```text
=== Summary ===

Matched strings: 1
String references: 4
Containing functions: 2
Callers found: 2

[OK] Done.
```

## Result Files

Every execution creates a log file inside:

```text
ghidra/scripts/modules/TraceStringCallers/result/
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

This utility bridges the gap between string discovery and function analysis.

Typical investigation sequence:

1. Locate an interesting string.
2. Execute `TraceStringCallers`.
3. Identify the function using the string.
4. Discover every caller of that function.
5. Continue reverse engineering from the discovered call sites.
6. Use `FindRefsToAddress` or `DumpDataAroundAddress` for deeper analysis if needed.

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