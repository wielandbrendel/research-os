#!/usr/bin/env python3
"""
Setup research-os standards for ML research.
Ensures ~/.research-os/standards/ contains required files.
"""

import os
import shutil
from pathlib import Path
import sys
import json
from typing import List, Tuple

REQUIRED_STANDARDS = {
    'global': [
        'coding-style.md',
        'commenting.md',
        'conventions.md',
        'error-handling.md',
        'tech-stack.md',
        'validation.md'
    ],
    'testing': [
        'coverage.md',
        'unit-tests.md'
    ]
}

def setup_standards() -> Tuple[bool, List[str], str]:
    """Setup standards and return (success, created_files, message)."""

    # Paths
    home = Path.home()
    user_standards_dir = home / '.research-os' / 'standards'

    # Get plugin root from environment or script location
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if not plugin_root:
        # Fallback: assume script is in plugin/scripts/
        plugin_root = Path(__file__).parent.parent
    else:
        plugin_root = Path(plugin_root)

    default_standards_dir = plugin_root / 'standards'

    created_files = []

    # Create user directory structure
    user_standards_dir.mkdir(parents=True, exist_ok=True)

    # Process each category
    for category, files in REQUIRED_STANDARDS.items():
        category_path = user_standards_dir / category
        category_path.mkdir(exist_ok=True)

        for filename in files:
            user_file = category_path / filename
            if not user_file.exists():
                default_file = default_standards_dir / category / filename

                if default_file.exists():
                    # Copy from defaults
                    shutil.copy2(default_file, user_file)
                    created_files.append(f"{category}/{filename}")
                else:
                    # Create placeholder for missing defaults
                    content = f"""# {filename[:-3].replace('-', ' ').title()}

## Overview
Custom ML research standards for {category}/{filename}

## Standards
[Add your research-specific standards here]

## Examples
[Add examples relevant to your research]
"""
                    user_file.write_text(content)
                    created_files.append(f"{category}/{filename} (template)")

    # Generate message
    if created_files:
        msg = f"✅ Research-OS standards successfully initialized\n"
        msg += f"📁 Created {len(created_files)} files in ~/.research-os/standards/\n"
        if len(created_files) <= 5:
            msg += "\n".join(f"  • {f}" for f in created_files)
        else:
            msg += "\n".join(f"  • {f}" for f in created_files[:3])
            msg += f"\n  ... and {len(created_files) - 3} more"
    else:
        msg = "✅ Research-OS standards successfully loaded.\n"
        msg += "All standards already present in ~/.research-os/standards/."

    print(msg, file=sys.stderr)
    return True, created_files, msg

if __name__ == "__main__":
    success, created, message = setup_standards()
    # print(json.dumps({
    #     "continue": True,
    #     "systemMessage": message
    # }))
    sys.exit(0)