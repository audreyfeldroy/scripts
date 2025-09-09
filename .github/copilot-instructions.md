# AGENTS.md
 
## Setup

No setup needed because uv scripts are self-contained!

## uv Scripts

A uv script 2025-08-29-example.py:

```python
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich.pretty import pprint

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])
```

To run it: `uv run 2025-08-29-example.py`

## Instructions

* In the current directory, create a uv script for the task the user requested.
* Script name should start with the current date in YYYY-MM-DD-task-name.py format.
* Don't put `uv` in the script name. All scripts in here are uv scripts.
* Never create a virtualenv to run it. `uv run 2025-08-29-example.py` creates a temporary environment for the script with its dependencies.

## References

https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script
