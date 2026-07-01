# DisplayModeDetection

## Purpose

`DisplayModeDetection` fixes display mode detection on modern systems.

The original game may fail during video mode probing even when a valid display mode is available. This can prevent the game from passing graphics initialization correctly on modern operating systems, Wine, Proton, or contemporary GPU drivers.

This patch forces the display mode detection check to report success at a specific compatibility point.

## Target

```text
king.exe
```

## Patch Point

```text
Virtual address: 0x005155be
File offset:     0x001155be
Section:         .text
Size:            8 bytes
```

## Original Bytes

```text
f7 d8 1b c0 f7 d8 85 c0
```

## Patched Bytes

```text
b8 01 00 00 00 85 c0 90
```

## Technical Notes

The original code computes a result value and then tests it.

The patched code forces the result register to a successful value before the test instruction.

Conceptually:

```text
EAX = 1
TEST EAX, EAX
```

The final byte is padded with `NOP` to preserve instruction alignment and patch size.

## Expected Result

The game should continue past display mode detection instead of failing due to an invalid or unsupported detection result.

## Compatibility Notes

This patch is intended for compatibility improvement only.

It does not replace game files and does not bypass licensing or DRM.

## Related Research

```text
app/research/GpuDetection/Notes.md
```

## Status

```text
Implemented
```
