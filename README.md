# ShiftLock

ShiftLock is a robust, cross-platform Caesar cipher CLI tool supporting multiple character sets and advanced error handling. It works on both Windows and Linux.

## Key Features
- Cross-platform: Linux and Windows support
- Five character sets: basic, extended, alphanumeric, keyboard, unicode
- Correct Caesar cipher logic (A-Z and a-z shifted separately in basic mode)
- Unicode support
- Robust error handling and input validation
- Comprehensive test script
- **NEW: Graphical User Interface (GUI)**

## Installation

### Linux
```sh
./install.sh
```

### Windows
No installation required. Run with Python:
```sh
python src/Shiftlock.py [operation] [options]
```

## Usage

### GUI Version (Recommended for beginners)
```sh
python src/ShiftlockGUI.py
```

The GUI provides:
- Easy-to-use interface with radio buttons and dropdowns
- Text input area for direct text entry
- File browser for file input
- Real-time output display
- Save to file option
- All character sets and operations available

### CLI Version (Advanced users)

#### Encrypt text
```sh
python src/Shiftlock.py encrypt -t "Secret Message" -s 7
```

#### Decrypt file
```sh
python src/Shiftlock.py decrypt -f encrypted.txt -s 7 -o decrypted.txt
```

#### Brute-force decryption
```sh
python src/Shiftlock.py bruteforce -f ciphertext.txt
```

### Options
- `-t`, `--text` TEXT: Input text
- `-f`, `--file` FILE: Input file
- `-s`, `--shift` N: Shift value (default: 3, range: -25 to 25)
- `--charset` SET: Character set (basic, extended, alphanumeric, keyboard, unicode)
- `-o`, `--output` FILE: Output file
- `-v`, `--version`: Show version
- `-h`, `--help`: Show help message

## Testing
Run the test script:
```sh
bash tests/test_shiftlock.sh
```

## License
MIT 