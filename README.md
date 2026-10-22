# PCK Reverse engineer
**Reverse engineering of .pck files from the "In The Groove" PC Demo**

.pck files are packages that StepMania mounts as VFS (Virtual File System) instead of unpacking their content to disk.

## How the structure maps to a VFS

The directory is the pack’s file index. The engine reads it when it mounts the pack and builds a table from each path to a position in the file.
The paths are virtual paths, not locations on disk. Entries like "Cache/Banners/..." and "Cache/Songs/..." look like paths relative to the game’s root. Once the pack is mounted, they would appear as if those folders and files existed there.
Each record gives the offset, stored size and compression flag, so the engine can open one file without touching the rest. A read seeks to the offset and, for a flagged entry, decompresses on the fly with zlib.

## Bit by bit walkthrough

This is the structure of a sample .pck file.

```offset      bytes / value                      meaning
0x0000      50 43 4b 46                        "PCKF" magic
0x0004      "default base song" + zeros        pack name, fills up to 0x80
0x0080      00 00 00 00                        reserved (0)
0x0084      a8 00 00 00                        file count = 168
0x0088      ── directory starts ──
            record 0 (20 bytes of numbers + name)
            record 1
            ...
            record 167
0x2D36      ── file data starts (offset 11574) ──
            file 0's bytes, file 1's bytes, ...
```

Here is one record of a directory:

```
20 80 00 00   stored size   = 32,800
20 80 00 00   real size     = 32,800   (same, so not compressed)
36 2d 00 00   data offset   = 11,574
3f 00 00 00   name length   = 63
00 00 00 00   compressed?   = 0
"Cache/Banners/_Songs_In The Groove_Euphoria_Euphoria-banner.png"   (63 characters)
```
