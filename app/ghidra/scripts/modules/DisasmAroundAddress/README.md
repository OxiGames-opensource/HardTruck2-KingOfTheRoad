# DisasmAroundAddress

## Purpose

`DisasmAroundAddress` prints disassembled instructions starting from a specified address.

The script is intended to help inspect:

- nearby code flow;
- function bodies;
- branch targets;
- call sites;
- patch candidates;
- code surrounding interesting references.

This is one of the core research utilities used during reverse engineering.

## Repository Location

```text
ghidra/scripts/modules/
└── DisasmAroundAddress/
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

The script accepts two parameters.

### Parameter 1 — Start Address

Supported formats:

```text
00527c20
```

```text
0x00527c20
```

```text
527c20
```

If omitted, the script asks for the address interactively.

### Parameter 2 — Instruction Count

The number of instructions to print.

Supported formats:

```text
300
```

```text
0x12c
```

If omitted, the script asks for the count interactively.

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
    -postScript modules/DisasmAroundAddress/run.java 00527c20 300
```

Equivalent hexadecimal count example:

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/DisasmAroundAddress/run.java 00527c20 0x12c
```

## Output

The script prints:

- start address;
- instruction count;
- first resolved instruction address;
- disassembled instructions;
- summary.

Example:

```text
=== Disassemble Around Address ===

Start address: 00527c20
Instruction count: 300

00527c20  PUSH EBP
00527c21  MOV EBP,ESP
...
```

## Summary

At the end of execution the script reports:

- requested start address;
- first instruction address;
- requested instruction count;
- printed instructions.

Example:

```text
=== Summary ===

Requested start address: 00527c20
First instruction address: 00527c20
Requested instructions: 300
Printed instructions: 300

[OK] Done.
```

## Result Files

Every execution creates a log file inside:

```text
ghidra/scripts/modules/DisasmAroundAddress/result/
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

This utility is typically used after locating an interesting code address.

Common investigation sequence:

1. Locate a string with `FindStringRefs`.
2. Find references with `FindRefsToAddress`.
3. Trace callers with `TraceStringCallers`.
4. Inspect nearby instructions with `DisasmAroundAddress`.
5. Continue analysis from branches, calls, and patch candidates.

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
