#!/bin/bash
if ! command -v uv &> /dev/null
then
    echo "---" >&2
    echo "⚠️ 'uv' command not found." >&2
    echo "This tool requires 'uv' to be installed and in your PATH." >&2
    echo "Please install it from https://github.com/astral-sh/uv" >&2
    echo "---" >&2
    exit 1
fi