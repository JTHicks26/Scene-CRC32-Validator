# Scene CRC32 Validator
This program verifies crc32 checksums of .rXX and .rar files in the current directory.

# Requirements
- Python 3
- Directory with .rXX files, .rar file, and .sfv file.
  - .rXX files must have a standard length of integers in the extension.
    - eg: .r0-.r9 or .r00-.r99
  - .sfv file must contain filenames and crc32 checksums seperated by a space.

# Usage
1) Place crc32.py in the directory with the files to be validated
2) Run crc32.py
