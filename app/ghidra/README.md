# Ghidra Scripts

This directory contains helper scripts used during reverse engineering research for **Hard Truck 2: King of the Road** compatibility patches.

Scripts are provided for analysis, documentation, and reproducibility purposes only.

## Purpose

Ghidra scripts are used to:

- locate patch points;
- inspect strings and references;
- verify addresses and instructions;
- export technical information for research notes;
- support documentation of binary patches.

They are not part of the game and do not include original game files.

## Directory Structure

Each script must be placed in its own directory:

```text
ghidra/scripts/modules/
└── ScriptName/
    ├── README.md
    └── run.java
```

or:

```text
ghidra/scripts/modules/
└── ScriptName/
    ├── README.md
    └── run.py
```

## Naming Rules

- Script directory names must use **PascalCase**.
- Each script directory must contain a `README.md`.
- The main script entrypoint must be named `run.java` or `run.py`.
- Do not use spaces in script directory names.
- Do not use underscores (`_`).
- Do not use kebab-case (`-`).

Examples:

```text
FindStringRefs/
FindPatchPoint/
ExportPatchBytes/
DumpFunctionInfo/
```

## Repository Rules

Do not commit:

- original game files;
- `king.exe`;
- imported Ghidra projects;
- Ghidra project databases;
- generated analysis caches;
- temporary reverse engineering dumps.

Allowed files:

- Ghidra scripts;
- script documentation;
- short byte patterns required to identify patch points;
- labels, notes, and metadata created for research;
- references to related research notes and patches.

## Script README Requirements

Each script `README.md` should describe:

- what the script does;
- how to run it;
- expected input;
- expected output;
- related research notes;
- related patch, if applicable;
- limitations or assumptions.

Recommended format:

````md
# ScriptName

## Purpose

Describe what this script does.

## Usage

Describe how to run it in Ghidra.

## Output

Describe what the script prints or exports.

## Related Research

- `research/SomeTopic/Notes.md`

## Related Patch

- `patches/SomePatch/patch.json`