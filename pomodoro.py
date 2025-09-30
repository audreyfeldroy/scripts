# /// script
# dependencies = [
#   "rich",
#   "typer",
# ]
# ///

import time
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

def pomodoro_timer(task: str):
    console.print(f"Starting Pomodoro for: {task}")
    total_seconds = 25 * 60
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task_id = progress.add_task(f"Pomodoro: {task} - 25:00 remaining", total=total_seconds)
        for i in range(total_seconds, 0, -1):
            time.sleep(1)
            minutes = i // 60
            seconds = i % 60
            progress.update(task_id, advance=1, description=f"Pomodoro: {task} - {minutes:02d}:{seconds:02d} remaining")
    console.print("Pomodoro complete!")

if __name__ == "__main__":
    typer.run(pomodoro_timer)