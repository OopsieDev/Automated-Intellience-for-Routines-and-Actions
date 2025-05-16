from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
import inquirer
import sys

console = Console()

tasks = []

def show_menu():
    console.print("[bold cyan]\nTask Manager CLI[/bold cyan]", justify="center")
    console.print("[green]1.[/green] Add Task")
    console.print("[green]2.[/green] List Tasks")
    console.print("[green]3.[/green] Mark Task as Done")
    console.print("[green]4.[/green] Delete Task")
    console.print("[green]5.[/green] Exit")

def add_task():
    task = Prompt.ask("Enter task description")
    tasks.append({"desc": task, "done": False})
    console.print(f"[bold green]Task added:[/bold green] {task}")

def list_tasks():
    table = Table(title="Tasks", show_lines=True)
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Status", style="green")
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return
    for i, t in enumerate(tasks, 1):
        status = "[bold green]Done[/bold green]" if t["done"] else "[red]Pending[/red]"
        table.add_row(str(i), t["desc"], status)
    console.print(table)

def mark_done():
    list_tasks()
    if not tasks:
        return
    idx = Prompt.ask("Enter task ID to mark as done", default="1")
    if idx.isdigit() and 1 <= int(idx) <= len(tasks):
        tasks[int(idx)-1]["done"] = True
        console.print(f"[green]Task {idx} marked as done![/green]")
    else:
        console.print("[red]Invalid task ID.[/red]")

def delete_task():
    list_tasks()
    if not tasks:
        return
    idx = Prompt.ask("Enter task ID to delete", default="1")
    if idx.isdigit() and 1 <= int(idx) <= len(tasks):
        removed = tasks.pop(int(idx)-1)
        console.print(f"[red]Task deleted:[/red] {removed['desc']}")
    else:
        console.print("[red]Invalid task ID.[/red]")

def main():
    while True:
        questions = [
            inquirer.List(
                "choice",
                message="Choose an option",
                choices=[
                    ("Add Task", "1"),
                    ("List Tasks", "2"),
                    ("Mark Task as Done", "3"),
                    ("Delete Task", "4"),
                    ("Exit", "5"),
                ],
                default="2",
            )
        ]
        answer = inquirer.prompt(questions)
        choice = answer["choice"] if answer else "5"
        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            if Confirm.ask("Are you sure you want to exit?"):
                console.print("[bold cyan]Goodbye![/bold cyan]")
                sys.exit(0)

if __name__ == "__main__":
    main()
