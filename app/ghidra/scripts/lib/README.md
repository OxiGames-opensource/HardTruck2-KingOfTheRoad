# Ghidra Script Library

This directory contains shared helper classes used by Ghidra scripts in this repository.

The library exists to keep individual scripts small, consistent, and reproducible.

## Purpose

Shared classes from this directory provide common functionality for:

- console output formatting;
- writing script results to log files;
- creating result directories;
- working with script arguments;
- collecting information about the currently opened Ghidra program;
- common string and file utilities.

## Directory Location

```text
ghidra/scripts/lib/
```

## Expected Structure

```text
ghidra/scripts/lib/
├── README.md
├── Console.java
├── FileUtils.java
├── Logger.java
├── ProgramInfo.java
├── ScriptOptions.java
└── StringUtils.java
```

## Classes

### `Logger.java`

Writes script messages both to the Ghidra console and to a result log file.

Expected log file format:

```text
YYYY-MM-DD_HH-mm-ss.log
```

Each script should write its runtime output to its own local `result/` directory.

### `ProgramInfo.java`

Collects and prints information about the currently opened Ghidra program.

Typical information:

- program name;
- executable path, if available;
- executable format;
- language;
- compiler specification;
- image base;
- minimum address;
- maximum address.

### `ScriptOptions.java`

Provides helper methods for reading script arguments and default values.

This class is intended to make scripts usable in both:

- Ghidra GUI mode;
- Ghidra Headless mode.

### `FileUtils.java`

Provides helper methods for local file and directory operations.

Typical use cases:

- creating directories;
- checking whether paths exist;
- resolving result paths;
- safely creating output files.

### `StringUtils.java`

Provides small string helper methods used across scripts.

Typical use cases:

- empty string checks;
- safe trimming;
- case-insensitive matching;
- formatting simple text values.

### `Console.java`

Provides helper methods for formatting console output.

Typical use cases:

- section headers;
- summary blocks;
- key-value output;
- visual separators.

## Usage Rules

- Shared classes should contain only reusable logic.
- Script-specific logic must remain inside the script directory.
- Do not place research notes in this directory.
- Do not place script results in this directory.
- Do not place game files in this directory.
- Do not place Ghidra project files in this directory.

## Script Integration

A script should use shared classes from this directory when it needs common behavior.

Example script structure:

```text
ghidra/scripts/modules/FindStringRefs/
├── README.md
├── result/
│   └── .gitkeep
└── run.java
```

The script should write generated output to:

```text
ghidra/scripts/modules/FindStringRefs/result/
```

Generated result files must not be committed to the repository.

## Result Files

Runtime results are local artifacts.

They must be written to the script-specific `result/` directory using this filename format:

```text
YYYY-MM-DD_HH-mm-ss.log
```

Example:

```text
2026-01-02_08-45-50.log
```

The repository contains tools and documentation, not generated analysis output.

## Git Rules

The contents of every script `result/` directory must be ignored by Git.

Expected `.gitignore` rule:

```gitignore
# Ghidra script runtime results
ghidra/scripts/modules/*/result/*
!ghidra/scripts/modules/*/result/.gitkeep
```

## Legal Notice

This library is intended only for compatibility research, documentation, and preservation work.

It does not include, generate, or distribute original game files.

All scripts using this library must be used only with legally purchased copies of **Hard Truck 2: King of the Road**.