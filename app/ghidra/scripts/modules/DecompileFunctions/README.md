# DecompileFunctions

## Purpose

`DecompileFunctions` decompiles one or more functions that contain the specified addresses.

The module is intended to quickly inspect function logic after discovering an interesting address during reverse engineering.

Typical use cases include:

- understanding subsystem behavior;
- identifying patch locations;
- inspecting control flow;
- validating research results;
- studying functions referenced by strings or call chains.

This is one of the core research modules of the OxiGames Ghidra Toolkit.

---

# Repository Location

```text
ghidra/scripts/modules/
└── DecompileFunctions/
    ├── README.md
    ├── result/
    │   └── .gitkeep
    └── run.java
```

---

# Requirements

- Ghidra 12+
- A legally obtained copy of the target game.
- Target executable imported using the standard OxiGames workflow.

---

# Parameters

The module accepts one or more addresses.

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

Example:

```text
run.java 005279e0
```

Multiple addresses:

```text
run.java 005279e0 00528f50 00515ca0
```

If no address is specified, the module requests one interactively.

---

# Options

## Full Decompiled C Output

```text
--output=c
```

Prints the complete decompiled function.

This is the default mode.

---

## Function Signature

```text
--output=signature
```

Prints only the function signature.

Example:

```text
undefined4 FUN_005279e0(char *param_1,int param_2)
```

---

# Usage

The standard execution workflow is described in:

```text
ghidra/workspace/README.md
```

## Full Decompiled Output

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/DecompileFunctions/run.java \
    005279e0 \
    --output=c
```

---

## Function Signature Only

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/DecompileFunctions/run.java \
    005279e0 \
    --output=signature
```

---

## Multiple Functions

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/DecompileFunctions/run.java \
    005279e0 \
    00528f50 \
    00515ca0 \
    --output=c
```

---

# Output

For every requested address the module reports:

- requested address;
- containing function;
- function entry point;
- selected output mode;
- decompiled source code or function signature.

Example:

```text
=== Function ===

Requested address: 005279e0
Function: FUN_005279e0
Function entry: 005279e0
Output mode: c
```

---

# Summary

At the end of execution the module reports:

- requested addresses;
- functions found;
- successfully decompiled functions;
- failed items.

Example:

```text
=== Summary ===

Requested addresses: 3
Functions found: 3
Functions decompiled: 3
Failed: 0

[OK] Done.
```

---

# Result Files

Every execution generates a log file inside:

```text
ghidra/scripts/modules/DecompileFunctions/result/
```

Filename format:

```text
YYYY-MM-DD_HH-mm-ss.log
```

Example:

```text
2026-01-02_08-45-50.log
```

Result files are considered local research artifacts and are intentionally excluded from version control.

---

# Typical Workflow

A common reverse engineering workflow is:

1. Locate an interesting string using `FindStringRefs`.
2. Find references using `FindRefsToAddress`.
3. Discover callers using `TraceStringCallers`.
4. Inspect machine code using `DisasmAroundAddress`.
5. Decompile the discovered functions using `DecompileFunctions`.

---

# Related Research

Typical usage includes:

```text
research/MovieSubsystem/
research/GpuDetection/
research/TextureMemory/
```

---

# Related Patch

None.

This module performs analysis only and never modifies executable files.

---

# Legal Notice

This module is intended for use with legally obtained copies of supported games.

It performs reverse engineering research only and does not distribute, modify or replace original game files.