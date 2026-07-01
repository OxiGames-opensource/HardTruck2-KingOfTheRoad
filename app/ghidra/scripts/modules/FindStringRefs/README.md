# FindStringRefs

## Purpose

`FindStringRefs` searches defined string data in the currently opened Ghidra program and prints references to strings that match a requested text fragment.

The script is intended to help locate code paths related to:

- error messages;
- subsystem initialization;
- diagnostics;
- UI text;
- configuration strings;
- compatibility research entry points.

This script was initially created during research of the movie subsystem error message:

```text
avi subsystem error
```

The search text is configurable and can be provided either interactively or through Ghidra script arguments.

## Repository Location

```text
ghidra/scripts/modules/FindStringRefs/
├── README.md
├── result/
│   └── .gitkeep
└── run.java
```

## Requirements

- Ghidra installed.
- A legally purchased copy of **Hard Truck 2: King of the Road**.
- The target executable imported into a local Ghidra project.
- Ghidra auto-analysis completed before running the script.

## What The Script Does

The script:

1. Gets a search string from script arguments or interactive input.
2. Iterates over defined data in the current Ghidra program.
3. Filters values recognized by Ghidra as strings.
4. Searches for strings matching the requested text.
5. Prints matched string addresses.
6. Prints all references pointing to matched strings.
7. Writes the same output to a local result log file.
8. Prints a short summary.

## Parameters

### Argument 1: Search Text

The first script argument is used as the search text.

Example:

```text
avi subsystem error
```

If no argument is provided, the script opens an interactive input dialog.

If the interactive input is empty, the default value is used:

```text
avi subsystem error
```

### Optional Argument: `--ignore-case`

Enables case-insensitive search.

### Optional Argument: `--exact`

Requires exact string match instead of substring match.

## Usage In Ghidra GUI

1. Open the target executable in Ghidra.
2. Wait until auto-analysis is complete.
3. Open Script Manager.
4. Add the repository script directory if needed:

```text
ghidra/scripts/
```

5. Run:

```text
modules/FindStringRefs/run.java
```

6. Enter the string fragment to search for.

Example:

```text
avi subsystem error
```

## Usage In Ghidra Headless Mode

Example:

```text
analyzeHeadless /path/to/ghidra/project ProjectName \
    -process king.exe \
    -postScript FindStringRefs/run.java "avi subsystem error"
```

Case-insensitive search:

```text
analyzeHeadless /path/to/ghidra/project ProjectName \
    -process king.exe \
    -postScript FindStringRefs/run.java "AVI SUBSYSTEM ERROR" --ignore-case
```

Exact match:

```text
analyzeHeadless /path/to/ghidra/project ProjectName \
    -process king.exe \
    -postScript FindStringRefs/run.java "avi subsystem error" --exact
```

## Output

The script prints output to:

- Ghidra console;
- script-local result log file.

Result files are written to:

```text
ghidra/scripts/modules/FindStringRefs/result/
```

Result filename format:

```text
YYYY-MM-DD_HH-mm-ss.log
```

Example:

```text
2026-01-02_08-45-50.log
```

The script prints:

- matched string address;
- matched string value;
- references to the matched string;
- reference type;
- total number of matched strings;
- total number of references.

## Result Files Policy

Result files are local artifacts.

They are intentionally not committed to the repository.

The repository contains the research tool, not generated analysis output.

Expected `.gitignore` rule:

```gitignore
ghidra/scripts/modules/*/result/*
!ghidra/scripts/modules/*/result/.gitkeep
```

## Limitations

The script searches only strings already recognized by Ghidra as defined data.

If the expected text is not found:

1. Run auto-analysis again.
2. Check that the target memory range is analyzed.
3. Manually define the string in Ghidra if needed.
4. Run the script again.

## Related Research

```text
research/MovieSubsystem/Notes.md
```

## Related Patch

Currently none.

This script is a research helper and does not apply binary patches.

## Legal Notice

This script is intended for use with a legally purchased copy of **Hard Truck 2: King of the Road**.

It does not include or distribute original game files.

It is intended only for compatibility research, documentation, and preservation work.