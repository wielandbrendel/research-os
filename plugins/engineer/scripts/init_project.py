#!/usr/bin/env python3
"""
UserPromptSubmit hook for initializing research-os directory structure.
Triggers on /engineer:new-artifact command.
"""
import json
import sys
import os
import shutil
from pathlib import Path


def get_all_files(base_dir):
    """Get all relative file paths in directory, excluding .DS_Store."""
    files = set()
    for root, dirs, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename != '.DS_Store':
                rel_path = Path(root).relative_to(base_dir) / filename
                files.add(str(rel_path))
    return files


def sync_missing_files(source_dir, target_dir):
    """Sync missing files from source to target."""
    source_files = get_all_files(source_dir)
    target_files = get_all_files(target_dir)

    missing_files = source_files - target_files

    for rel_path in missing_files:
        src_file = source_dir / rel_path
        dst_file = target_dir / rel_path

        # Create parent directories if needed
        dst_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        shutil.copy2(src_file, dst_file)

    return sorted(list(missing_files))


def main():
    """Main hook function."""
    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)
        prompt = input_data.get("prompt", "")

        # Check if prompt contains our trigger command
        if "/engineer:new-artifact" not in prompt:
            # Not our concern, continue without modification
            sys.exit(0)

        # Get paths from environment
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
        if not project_dir:
            # Fallback to cwd from hook input
            project_dir = input_data.get("cwd", os.getcwd())

        project_dir = Path(project_dir)
        target_dir = project_dir / "research-os"
        source_dir = Path.home() / ".research-os"

        # Check if target already exists
        if target_dir.exists():
            # Check for missing files and sync if needed
            try:
                missing_files = sync_missing_files(source_dir, target_dir)
                if missing_files:
                    msg = f"📋 Synchronized {len(missing_files)} missing file(s) from ~/.research-os:\n"
                    for file in missing_files[:5]:  # Show first 5
                        msg += f"  ✓ {file}\n"
                    if len(missing_files) > 5:
                        msg += f"  ... and {len(missing_files) - 5} more\n"
                    print(msg, file=sys.stderr)
            except Exception as e:
                print(f"⚠️  Error syncing files: {e}", file=sys.stderr)
            # Continue silently if everything is in sync or after syncing
            sys.exit(0)

        # Check if source exists
        if not source_dir.exists():
            msg = "⚠️  Source directory ~/.research-os does not exist.\n"
            msg += "Please create ~/.research-os/standards/ with your research standards first."
            print(msg, file=sys.stderr)
            sys.exit(0)

        # Copy directory
        try:
            shutil.copytree(source_dir, target_dir)
            msg = f"✅ Successfully initialized research-os from ~/.research-os\n"
            msg += f"📁 Created: {target_dir}\n"
            msg += f"📄 Standards ready for customization in research-os/standards/"
            print(msg, file=sys.stderr)
        except Exception as e:
            print(f"❌ Error copying research-os: {e}", file=sys.stderr)

        # Always exit 0 to not block the command
        sys.exit(0)

    except Exception as e:
        # Log error but don't block
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()