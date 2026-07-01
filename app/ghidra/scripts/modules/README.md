# Module Command Line Interface Standard

## Purpose

All research modules must expose a consistent command line interface.

A user who learns one module should immediately understand how to use every other module.

Consistency is preferred over module-specific conventions.

---

# General Syntax

Every module should follow the same command format:

```text
run.java [arguments] [options]
```

where:

- `arguments` represent the primary research target;
- `options` modify the module behavior.

---

# Arguments

Arguments should contain only the minimum information required to perform the research task.

Examples:

```text
FindStringRefs
```

```text
run.java "avi subsystem error"
```

```text
FindRefsToAddress
```

```text
run.java 005279e0
```

```text
DumpDataAroundAddress
```

```text
run.java 00676680 0x220
```

```text
DisasmAroundAddress
```

```text
run.java 00527c20 300
```

```text
DecompileFunctions
```

```text
run.java 005279e0 00528f50 00515ca0
```

Modules may support multiple primary arguments when appropriate.

---

# Common Options

Every module should support a common set of options whenever applicable.

## Help

```text
--help
```

Displays module documentation and exits.

---

## Verbose Mode

```text
--verbose
```

Produces additional diagnostic output.

---

## Quiet Mode

```text
--quiet
```

Produces only essential output.

---

# Module Specific Options

Modules may define additional options specific to their functionality.

Examples:

## FindStringRefs

```text
--ignore-case
```

---

## DecompileFunctions

```text
--output=c
```

```text
--output=signature
```

Future modes may include:

```text
--output=asm
```

```text
--output=all
```

---

# Output Philosophy

Modules should produce structured, human-readable output.

Typical layout:

```text
Header

Research results

Summary
```

The summary should always contain enough information to quickly determine whether the execution was successful.

---

# Logging

Every module must:

- write to the console;
- write to its own log file;
- store logs inside its local `result/` directory.

---

# Interactive Mode

If required arguments are missing, the module should request them interactively whenever possible.

This allows the same module to work both:

- from `analyzeHeadless`;
- from the Ghidra graphical interface.

---

# Exit Behavior

Every successful execution should finish with:

```text
[OK] Done.
```

Warnings and failures should use the common logger formatting.

---

# Future Compatibility

New options should be introduced without breaking existing command lines.

For example:

```text
run.java 005279e0
```

should remain valid after introducing:

```text
--output=...
```

or

```text
--verbose
```

The command line interface should remain backward compatible whenever practical.

---

# Design Goal

Every research module should feel like part of a single toolkit rather than an independent script.

The entire OxiGames Ghidra Toolkit should provide a predictable, consistent and reproducible user experience.