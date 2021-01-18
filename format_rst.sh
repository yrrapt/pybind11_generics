#!/usr/bin/env bash


# check input arguments
if [ $# -ne 1 ]; then 
    echo "Usage: ${0} <file>"
    exit 1
fi

RST_FILE="${1}"
PANDOC_DEFAULTS=".pandoc_rst.yaml"

# check argument file exists
if ! [ -f "${RST_FILE}" ]; then
    echo "[ERROR] Cannot find file: ${RST_FILE}" >&2
    exit 1
fi

# check pandoc defaults file exists
if ! [ -f "${PANDOC_DEFAULTS}" ]; then
    echo "[ERROR] Cannot find pandoc defaults file: ${PANDOC_DEFAULTS}" >&2
    exit 1
fi

# check pandoc is installed
if ! [ -x $(command -v pandoc) ]; then
    echo "[ERROR] Cannot find pandoc in PATH" >&2
    exit 1
fi

# exit if any command fails
set -e

# use pandoc to re-format file
pandoc --defaults=.pandoc_rst.yaml -o "${RST_FILE}" "${RST_FILE}"
# replace code directives with code-block for better sphinx integration
sed -i 's/.. code::/.. code-block::/g' "${RST_FILE}"
