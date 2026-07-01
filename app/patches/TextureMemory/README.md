# TextureMemory

## Purpose

`TextureMemory` fixes an incorrect texture memory failure check on modern systems.

The original game may report insufficient texture memory even when the system has enough available video memory. This can happen on modern GPUs, Wine, Proton, or graphics compatibility layers where the original detection logic does not behave correctly.

This patch bypasses the failing conditional branch and allows the game to continue past the texture memory check.

## Target

```text
king.exe
```

## Patch Point

```text
Virtual address: 0x00513024
File offset:     0x00113024
Section:         .text
Size:            2 bytes
```

## Original Bytes

```text
7d 1e
```

## Patched Bytes

```text
eb 1e
```

## Technical Notes

The original instruction is a conditional jump.

The patched instruction changes it to an unconditional jump while preserving the jump distance.

Conceptually:

```text
JGE +0x1e
```

is replaced with:

```text
JMP +0x1e
```

This bypasses the failure path related to the texture memory check.

## Expected Result

The game should continue past the texture memory validation instead of failing with an insufficient texture memory condition.

## Compatibility Notes

This patch is intended for compatibility improvement only.

It does not replace game files and does not bypass licensing or DRM.

## Related Research

```text
app/research/TextureMemory/Notes.md
```

## Status

```text
Implemented
```
