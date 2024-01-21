#!/bin/bash

folder_path="tests/test_data"  # Replace with the actual folder path
pattern="test[0-9]*_source.py"      # Pattern to match source files

# Find the latest number
latest_number=$(ls "$folder_path" | grep -E "$pattern" | awk -F'[_]' '{print $1}' | grep -Eo '[0-9]+' | sort -n | tail -n 1)

# Check if latest_number is empty (no files found)
if [ -z "$latest_number" ]; then
  latest_number=0
fi

# Generate new file names with the latest number
new_source_file="test$((latest_number + 1))_source.py"
new_expected_file="test$((latest_number + 1))_expected.py"

# Create the new source and expected files
touch "$folder_path/$new_source_file"
touch "$folder_path/$new_expected_file"

echo "Created $new_source_file and $new_expected_file"
