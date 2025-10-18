#!/usr/bin/env python3
"""
PostToolUse hook for checking Python files after editing.
This hook runs after Edit, Write, or MultiEdit operations and applies ruff checking.
"""

import json
import subprocess
import sys


def main():
    """Main function to run ruff check hook."""
    try:
        # Read hook input data
        hook_data = json.load(sys.stdin)
        tool_input = hook_data.get("tool_input", {})

        # Get the file path from tool input
        file_path = tool_input.get("file_path", "")

        # Only process Python files and only for file editing tools
        if not file_path or not file_path.endswith((".py", ".pyi")):
            # Not a Python file, exit successfully
            print("Ruff check: Not a python file, skipping.")
            sys.exit(0)

        # Run ruff check with import sorting and comprehensive linting
        try:
            check_result = subprocess.run(
                [
                    "ruff",
                    "check",
                    "--fix",
                    "--select",
                    "F,E,W,I",
                    "--line-length",
                    "120",
                    file_path,
                ],
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            print("Ruff not found. Please install ruff.", file=sys.stderr)
            sys.exit(0)

        # Exit code mapping:
        # ruff exit 0 (success) -> hook exit 0
        # ruff exit 1 (violations found) -> hook exit 2 (block Claude)
        # ruff exit 2 (error) -> hook exit 0 (don't block on config errors)
        if check_result.returncode == 0:
            # Success - print stdout normally
            if check_result.stdout:
                print(check_result.stdout, end="")
            if check_result.stderr:
                print(check_result.stderr, file=sys.stderr, end="")
            sys.exit(0)
        elif check_result.returncode == 1:
            # Violations found - redirect stdout to stderr so Claude sees it
            if check_result.stdout:
                print(check_result.stdout, file=sys.stderr, end="")
            if check_result.stderr:
                print(check_result.stderr, file=sys.stderr, end="")
            sys.exit(2)  # Block and feed stderr to Claude
        else:  # check_result.returncode == 2
            # Config errors - don't block, print normally
            if check_result.stdout:
                print(check_result.stdout, end="")
            if check_result.stderr:
                print(check_result.stderr, file=sys.stderr, end="")
            sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on hook errors


if __name__ == "__main__":
    main()