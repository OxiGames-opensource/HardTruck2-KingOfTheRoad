# FindMultipleStrings

## Purpose

`FindMultipleStrings` performs broad reconnaissance by searching for multiple strings within the currently loaded Ghidra program.

Unlike `FindStringRefs`, which focuses on a single target, this module is designed to quickly scan a large set of candidate strings and identify which ones exist inside the executable.

For every matched string, the module reports:

- string address;
- string value;
- reference count;
- reference addresses.

The module intentionally stops at this level.

Once an interesting string has been identified, more specialized modules such as `FindStringRefs`, `TraceStringCallers`, `FindRefsToAddress`, `DisasmAroundAddress`, or `DecompileFunctions` can be used for deeper investigation.

This module serves as the initial reconnaissance stage of the OxiGames research workflow.

---

# Repository Location

```text
ghidra/scripts/modules/
└── FindMultipleStrings/
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

The module accepts one or more search strings.

Example:

```text
run.java "avi subsystem error"
```

Multiple search strings:

```text
run.java \
    "avi subsystem error" \
    "Not enough texture memory" \
    "Your computer does not have graphic accelerator"
```

If no search string is provided, the module requests one interactively.

---

# Options

## Case-insensitive Search

```text
--ignore-case
```

Enables case-insensitive matching.

---

## Search Strings From File

```text
--file=<path>
```

Loads search strings from a text file.

Each non-empty line is treated as an independent search string.

Empty lines are ignored.

Lines beginning with:

```text
#
```

are treated as comments.

Example:

```text
--file=ghidra/workspace/strings.txt
```

Example file:

```text
# Movies
KotrNewgame.avi
KotrDemo.avi

# Graphics
Not enough texture memory
Your computer does not have graphic accelerator
```

---

# Usage

The standard execution workflow is described in:

```text
ghidra/workspace/README.md
```

## Search Using Command Line Arguments

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/FindMultipleStrings/run.java \
    "Your computer does not have graphic accelerator" \
    "Not enough texture memory" \
    "KotrNewgame.avi"
```

---

## Case-insensitive Search

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/FindMultipleStrings/run.java \
    "your computer does not have graphic accelerator" \
    "not enough texture memory" \
    --ignore-case
```

---

## Search Using a File

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/FindMultipleStrings/run.java \
    --file=ghidra/workspace/strings.txt
```

---

# Output

For every search string the module reports:

- search text;
- matched string address;
- matched string value;
- reference count;
- reference addresses.

Example:

```text
=== Search ===

Text: Your computer does not have graphic accelerator

STRING: 00676d98 = Your computer does not have graphic accelerator

XREF count: 4

  XREF: 00515db1 type=DATA
  XREF: 00515dc4 type=DATA
  XREF: 00516502 type=DATA
  XREF: 00516516 type=DATA
```

If no match exists:

```text
=== Search ===

Text: Some Missing String

No matches.
```

---

# Summary

At the end of execution the module reports:

- search strings;
- matched strings;
- references found.

Example:

```text
=== Summary ===

Search strings: 3
Matched strings: 3
References found: 5

[OK] Done.
```

---

# Result Files

Every execution creates a log file inside:

```text
ghidra/scripts/modules/FindMultipleStrings/result/
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

1. Prepare a list of candidate strings.
2. Run `FindMultipleStrings` to perform broad reconnaissance.
3. Select interesting matches.
4. Use `FindStringRefs` to inspect references for a specific string.
5. Use `TraceStringCallers` to locate the calling functions.
6. Use `FindRefsToAddress` to inspect additional references.
7. Use `DisasmAroundAddress` to inspect assembly.
8. Use `DecompileFunctions` to inspect high-level logic.

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

This module performs research only and never modifies executable files.

---

# Legal Notice

This module is intended for use with legally obtained copies of supported games.

It performs reverse engineering research only and does not distribute, modify or replace original game files.