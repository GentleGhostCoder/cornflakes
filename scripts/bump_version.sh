#!/bin/bash

# Get the version number from the first command-line argument
version=$1

# Iterate over all files in the current directory
for file in */**; do
    # Check if the file is a regular file
    if [[ -f $file ]]; then
        # file is the current file skip
        if [[ $file == *"bump_version.sh"* ]]; then
            continue
        fi
        # Check if the file contains the string "# <<FORCE_BUMP>>"
        if grep -q "# <<FORCE_BUMP>>" "$file"; then
            # Increment the version number in the file
            sed -i "s/\(.*version.*=.*\|.*release.*=.*\)\(\".*\"\)\(.*\)/\1\"$version\"\3/" "$file"
        fi
    fi
done

echo "Version bumped to $version"
