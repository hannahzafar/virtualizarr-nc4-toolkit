#!/usr/bin/env python

import tempfile
from pathlib import Path
from virtualizarr_nc4_toolkit.utils import find_directory_files

print("Test 1: Non-existent directory")
result = find_directory_files("/fake/path")
print(f"Result: {result}\n")

print("Test 2: Is not a directory")
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Created temp directory: {tmpdir}")
    tmppath = Path(tmpdir)
    tmpfile = tmppath / "file1.txt"
    tmpfile.touch()
    result = find_directory_files(tmpfile)
    print(f"Result: {result}\n")


print("Test 3: Directory with no files")
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Created temp directory: {tmpdir}")
    result = find_directory_files(tmpdir)
    print(f"Result: {result}\n")

print("Test 4: Directory with files but no .nc4")
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Created temp directory: {tmpdir}")
    tmppath = Path(tmpdir)
    (tmppath / "file1.txt").touch()
    (tmppath / "file2.txt").touch()

    result = find_directory_files(tmppath)
    print(f"Result: {result}\n")

print("Test 5: Directory with one .nc4 file")
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Created temp directory: {tmpdir}")
    tmppath = Path(tmpdir)
    (tmppath / "file1.nc4").touch()

    result = find_directory_files(tmppath)
    print(f"Result: {result}\n")

print("Test 6: Directory with multiple .nc4 files")
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Created temp directory: {tmpdir}")
    tmppath = Path(tmpdir)
    (tmppath / "file1.nc4").touch()
    (tmppath / "file2.nc4").touch()

    result = find_directory_files(tmppath)
    print(f"Result: {result}")
    print(result[0], type(result[0]))
