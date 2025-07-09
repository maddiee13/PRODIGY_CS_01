#!/bin/bash

TEST_PASS=0
TEST_FAIL=0

run_test() {
    local description=$1
    local command=$2
    local expected=$3
    
    echo "Running test: $description"
    result=$(eval $command 2>/dev/null)
    
    if [ "$result" == "$expected" ]; then
        echo "  PASS: $command"
        ((TEST_PASS++))
    else
        echo "  FAIL: $command"
        echo "    Expected: $expected"
        echo "    Got: $result"
        ((TEST_FAIL++))
    fi
}

# Basic encryption
run_test "Basic encryption" "python src/Shiftlock.py encrypt -t 'HELLO' -s 3" "KHOOR"

# Basic decryption
run_test "Basic decryption" "python src/Shiftlock.py decrypt -t 'KHOOR' -s 3" "HELLO"

# Extended character set
run_test "Extended charset" "python src/Shiftlock.py encrypt -t 'ABC123' -s 3 --charset=extended" "DEF456"

# Alphanumeric
run_test "Alphanumeric" "python src/Shiftlock.py encrypt -t 'TEST123' -s 5 --charset=alphanumeric" "YJXY678"

# File handling
echo "Secret text" > test_input.txt
python src/Shiftlock.py encrypt -f test_input.txt -s 7 -o test_encrypted.txt
run_test "File encryption" "cat test_encrypted.txt" "Zlzjyl aoha"

# Cleanup
rm test_input.txt test_encrypted.txt

# Results
echo ""
echo "Test results:"
echo "PASS: $TEST_PASS"
echo "FAIL: $TEST_FAIL"

if [ "$TEST_FAIL" -gt 0 ]; then
    exit 1
fi