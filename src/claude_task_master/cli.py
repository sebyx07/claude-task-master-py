"""CLI entry point for Claude Task Master."""

import typer
from rich.console import Console
from rich.markdown import Markdown
from typing import Optional
from pathlib import Path
import sys

from .core.credentials import CredentialManager
from .core.state import StateManager, TaskOptions
from .core.agent import AgentWrapper, ModelType
from .core.planner import Planner
from .core.orchestrator import WorkLoopOrchestrator
from .core.logger import TaskLogger
from .core.context_accumulator import ContextAccumulator
from .utils.doctor import SystemDoctor

app = typer.Typer(
    name="claude-task-master",
    help="Autonomous task orchestration system using Claude Agent SDK",
    add_completion=False,
)
console = Console()


@app.command()
def start(
    goal: str = typer.Argument(..., help="The goal to achieve"),
    model: str = typer.Option("sonnet", help="Model to use: sonnet, opus, haiku"),
    auto_merge: bool = typer.Option(True, help="Automatically merge PRs when ready"),
    max_sessions: Optional[int] = typer.Option(None, help="Maximum number of sessions"),
    pause_on_pr: bool = typer.Option(False, help="Pause after creating PR for review"),
) -> None:
    """Start a new task with the given goal."""
    console.print(f"[bold green]Starting new task:[/bold green] {goal}")
    console.print(f"Model: {model}, Auto-merge: {auto_merge}")

    try:
        # Check if state already exists
        state_manager = StateManager()
        if state_manager.exists():
            console.print("[red]Error: Task already exists. Use 'resume' to continue or 'clean' to start fresh.[/red]")
            raise typer.Exit(1)

        # Load credentials
        console.print("Loading credentials...")
        cred_manager = CredentialManager()
        access_token = cred_manager.get_valid_token()

        # Parse model type
        model_type = ModelType(model)

        # Initialize state
        console.print("Initializing task state...")
        options = TaskOptions(
            auto_merge=auto_merge,
            max_sessions=max_sessions,
            pause_on_pr=pause_on_pr,
        )
        state = state_manager.initialize(goal=goal, model=model, options=options)

        # Initialize components
        working_dir = Path.cwd()
        agent = AgentWrapper(access_token, model_type, str(working_dir))
        planner = Planner(agent, state_manager)
        context_accumulator = ContextAccumulator(state_manager)

        # Initialize logger
        log_file = state_manager.get_log_file(state.run_id)
        logger = TaskLogger(log_file)

        # Run planning phase
        console.print("\n[bold cyan]Phase 1: Planning[/bold cyan]")
        logger.start_session(0, "planning")

        try:
            plan_result = planner.create_plan(goal)
            logger.log_response(plan_result.get("raw_output", ""))
            logger.end_session("completed")

            # Display plan
            console.print("\n[bold green]Plan created:[/bold green]")
            plan = state_manager.load_plan()
            if plan:
                console.print(Markdown(plan))

            # Update state to working
            state.status = "working"
            state_manager.save_state(state)

        except Exception as e:
            logger.log_error(str(e))
            logger.end_session("failed")
            console.print(f"\n[red]Planning failed: {e}[/red]")
            raise typer.Exit(1)

        # Run work loop
        console.print("\n[bold cyan]Phase 2: Execution[/bold cyan]")
        orchestrator = WorkLoopOrchestrator(agent, state_manager, planner)

        exit_code = orchestrator.run()

        if exit_code == 0:
            console.print("\n[bold green]✓ Task completed successfully![/bold green]")
        elif exit_code == 2:
            console.print("\n[yellow]Task paused. Use 'resume' to continue.[/yellow]")
        else:
            console.print("\n[red]Task blocked or failed.[/red]")

        raise typer.Exit(exit_code)

    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("Run 'claude-task-master doctor' to check your setup.")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def resume() -> None:
    """Resume a paused or interrupted task."""
    console.print("[bold blue]Resuming task...[/bold blue]")
    # TODO: Implement resume logic
    raise typer.Exit(1)


@app.command()
def status() -> None:
    """Show current status of the task."""
    console.print("[bold blue]Task Status[/bold blue]")
    # TODO: Implement status logic
    raise typer.Exit(1)


@app.command()
def plan() -> None:
    """Display the current task plan."""
    console.print("[bold blue]Task Plan[/bold blue]")
    # TODO: Implement plan logic
    raise typer.Exit(1)


@app.command()
def logs(
    session: Optional[int] = typer.Option(None, help="Show specific session number")
) -> None:
    """Display logs from the current run."""
    console.print("[bold blue]Logs[/bold blue]")
    # TODO: Implement logs logic
    raise typer.Exit(1)


@app.command()
def context() -> None:
    """Display accumulated context and learnings."""
    console.print("[bold blue]Context[/bold blue]")
    # TODO: Implement context logic
    raise typer.Exit(1)


@app.command()
def progress() -> None:
    """Display human-readable progress summary."""
    console.print("[bold blue]Progress[/bold blue]")
    # TODO: Implement progress logic
    raise typer.Exit(1)


@app.command()
def comments(
    pr: Optional[int] = typer.Option(None, help="PR number to show comments for")
) -> None:
    """Display PR review comments."""
    console.print("[bold blue]PR Comments[/bold blue]")
    # TODO: Implement comments logic
    raise typer.Exit(1)


@app.command()
def pr() -> None:
    """Display current PR status and CI checks."""
    console.print("[bold blue]PR Status[/bold blue]")
    # TODO: Implement pr logic
    raise typer.Exit(1)


@app.command()
def clean(
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation")
) -> None:
    """Clean up task state directory."""
    if not force:
        confirm = typer.confirm("Are you sure you want to clean all task state?")
        if not confirm:
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit(0)

    console.print("[bold red]Cleaning task state...[/bold red]")
    # TODO: Implement clean logic
    raise typer.Exit(0)


@app.command()
def doctor() -> None:
    """Check system requirements and authentication."""
    doctor = SystemDoctor()
    success = doctor.run_checks()
    raise typer.Exit(0 if success else 1)


if __name__ == "__main__":
    app()
