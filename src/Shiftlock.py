#!/usr/bin/env python3
import sys
import json
import argparse
import os
from pathlib import Path

# Load character sets
def load_charsets():
    # Cross-platform way to check if running as root/admin
    try:
        is_admin = os.getuid() == 0 if hasattr(os, 'getuid') else False
    except:
        is_admin = False
    
    if is_admin:
        data_dir = Path('/usr/share/shiftlock')
    else:
        data_dir = Path(__file__).parent.parent / 'data'
    
    # Try both possible filenames
    charset_file = data_dir / 'charsets.json'
    if not charset_file.exists():
        charset_file = data_dir / 'character.json'
    
    try:
        with open(charset_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Character set file not found at {charset_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in character set file: {e}", file=sys.stderr)
        sys.exit(1)

# Caesar cipher implementation
def shift_text(text: str, shift: int, charset: str = "basic") -> str:
    charsets = load_charsets()
    charset_data = charsets.get(charset, charsets['basic'])
    chars = charset_data['chars']
    
    if charset == 'basic':
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lower = 'abcdefghijklmnopqrstuvwxyz'
        result = []
        for char in text:
            if char in upper:
                idx = upper.index(char)
                new_idx = (idx + shift) % 26
                result.append(upper[new_idx])
            elif char in lower:
                idx = lower.index(char)
                new_idx = (idx + shift) % 26
                result.append(lower[new_idx])
            else:
                result.append(char)
        return ''.join(result)
    else:
        wrap = len(chars)
        result = []
        for char in text:
            if char in chars:
                idx = chars.index(char)
                new_idx = (idx + shift) % wrap
                result.append(chars[new_idx])
            else:
                result.append(char)
        return ''.join(result)

# Main CLI function
def main():
    parser = argparse.ArgumentParser(
        description='ShiftLock - Robust Caesar Cipher Tool',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('operation', choices=['encrypt', 'decrypt', 'bruteforce'], 
                        help='Operation to perform')
    parser.add_argument('-t', '--text', help='Text to process')
    parser.add_argument('-f', '--file', help='Input file path')
    parser.add_argument('-s', '--shift', type=int, default=3, 
                        help='Shift value (default: 3, range: -25 to 25)')
    parser.add_argument('--charset', default='basic', 
                        choices=['basic', 'extended', 'alphanumeric', 'keyboard', 'unicode'],
                        help='''Character set:
  basic: A-Z only (default)
  extended: A-Z + numbers + punctuation
  alphanumeric: A-Z + 0-9
  keyboard: All standard keyboard characters
  unicode: Full Unicode support''')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-v', '--version', action='version', version='ShiftLock 1.0')

    args = parser.parse_args()

    # Validate shift range
    if not (-25 <= args.shift <= 25):
        print("Error: Shift must be between -25 and 25", file=sys.stderr)
        sys.exit(1)
    
    # Get input content
    content = ""
    if args.text:
        content = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: No input provided. Use --text or --file", file=sys.stderr)
        sys.exit(1)
    
    # Process content
    if args.operation == 'encrypt':
        result = shift_text(content, args.shift, args.charset)
    elif args.operation == 'decrypt':
        result = shift_text(content, -args.shift, args.charset)
    else:  # bruteforce
        print("Brute-force results:")
        for i in range(1, 26):
            print(f"Shift {i:2d}: {shift_text(content, -i, args.charset)}")
        sys.exit(0)
    
    # Output result
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Output saved to {args.output}")
        except Exception as e:
            print(f"Error writing file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(result)

if __name__ == "__main__":
    main()