# Ghidra Workspace

This directory contains local files used during reverse engineering.

The repository never contains original game files.

## Purpose

`ghidra/workspace/` is a local working directory containing executables or other binaries that will be analyzed by Ghidra.

Everything stored here is considered a local user artifact and is intentionally excluded from version control.

## Repository Policy

Do not commit files placed in this directory.

Typical local files include:

- game executables;
- dynamic libraries;
- extracted binaries;
- temporary research files.

The repository should contain only:

- documentation;
- research notes;
- Ghidra scripts;
- patch descriptions;
- tooling.

## Expected Layout

```text
ghidra/workspace/
├── README.md
├── .gitkeep
└── <target executable>
```

## Standard Workflow

All Ghidra scripts in this repository follow the same execution model.

1. Copy the executable to be researched into `ghidra/workspace/`.
2. Open a terminal inside the project container or local development environment.
3. Execute the standard `analyzeHeadless` command.
4. Monitor execution progress in the console.
5. Review the generated results inside the script's local `result/` directory.

## Standard Command

All repository scripts should be executed using the following command:

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/<target executable> \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/<ScriptFolder>/run.java [script arguments]
```

Example:

```bash
analyzeHeadless ghidra/project HardTruck2 \
    -import ghidra/workspace/king.exe \
    -overwrite \
    -scriptPath "ghidra/scripts" \
    -postScript modules/FindStringRefs/run.java "avi subsystem error"
```

## Why Always Use `-overwrite`?

Every execution intentionally imports the executable again.

Although this requires a small amount of additional processing time, it guarantees that every script starts from a clean and reproducible state.

Benefits include:

- no stale analysis data;
- no accidental use of an older executable;
- deterministic research results;
- identical workflow for every script;
- no need to remember whether the executable has already been imported.

Reproducibility is considered more important than saving a few seconds during execution.

## Script Output

Every script writes its output to:

- the Ghidra console;
- its own local `result/` directory.

Example:

```text
ghidra/scripts/modules/FindStringRefs/result/
```

Generated log files use the following format:

```text
YYYY-MM-DD_HH-mm-ss.log
```

Example:

```text
2026-01-02_08-45-50.log
```

Result files are local artifacts and are intentionally excluded from the repository.

## Script Architecture

Each script is executed from its own directory.

Shared functionality is provided by the common library located at:

```text
ghidra/scripts/lib/
```

The library contains reusable components such as:

- logging;
- file utilities;
- program information;
- console formatting;
- script option handling;
- common helper functions.

This keeps individual scripts focused on research logic while maintaining a consistent implementation across the repository.

## Notes

Scripts operate on Ghidra's `currentProgram`.

After importing the executable into the local project, scripts should not access the original file directly.

## Legal Notice

Use this workspace only with legally obtained copies of supported games.

Do not commit or distribute original game files.