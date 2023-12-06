import sys
import os
from pathlib import Path
from inspect import cleandoc

_, raw_day = sys.argv
day = int(raw_day)
new_day = f"day_{day:02}"
new_day_directory = Path(new_day)
new_day_file = new_day_directory / f"{new_day}.py"

if not new_day_directory.exists():
    os.mkdir(new_day_directory)

base_file_content = cleandoc(
    f"""
    from aocd.models import Puzzle

    puzzle = Puzzle(2023, {day})
    """
)
if not new_day_file.exists():
    with open(new_day_file, "w") as f:
        f.write(base_file_content)
