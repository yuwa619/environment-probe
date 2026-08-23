import json
import os
import sys
from typing import Dict, Any
from environment_probe import __version__

def get_probe_data() -> Dict[str, Any]:
    """Gathers runtime information and validates required configuration."""
    env_name = os.environ.get("APE_ENVIRONMENT")
    if not env_name:
        raise ValueError("Required environment variable 'APE_ENVIRONMENT' is not set.")

    return {
        "package_version": __version__,
        "python_version": sys.version.split()[0],
        "environment_name": env_name,
    }

def run_probe() -> None:
    """Executes the probe command, printing JSON or cleanly reporting errors."""
    try:
        data = get_probe_data()
        print(json.dumps(data, indent=2))
        sys.exit(0)
    except ValueError as err:
        # Clean error message without printing a raw stack trace or secrets
        print(f"Configuration Error: {err}", file=sys.stderr)
        sys.exit(1)
