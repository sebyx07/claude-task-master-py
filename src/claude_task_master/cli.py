"""CLI entry point for Claude Task Master."""

import typer
from rich.console import Console
from rich.markdown import Markdown

from .cli_commands.workflow import register_workflow_commands
from .core.state import StateManager
from .utils.doctor import SystemDoctor

app = typer.Typer(
    name="claude-task-master",
    help="""Autonomous task orchestration system using Claude Agent SDK.

Claude Task Master keeps Claude working until a goal is achieved by:
- Breaking down goals into actionable tasks
- Executing tasks with appropriate tools
- Creating and managing GitHub PRs
- Waiting for CI and addressing reviews

Quick start:
  claudetm start "Your goal here"
  claudetm status
  claudetm clean -f

For more info, see: https://github.com/sebyx07/claude-task-master-py
""",
    add_completion=False,
)
console = Console()

# Register workflow commands (start, resume) from submodule
register_workflow_commands(app)


@app.command()
def status() -> None:
    """Show current status of the task.

    Displays goal, current task, session count, and configuration options.

    Examples:
        claudetm status
    """
    state_manager = StateManager()

    if not state_manager.exists():
        console.print("[yellow]No active task found.[/yellow]")
        raise typer.Exit(1)

    try:
        state = state_manager.load_state()
        goal = state_manager.load_goal()

        console.print("\n[bold blue]Task Status[/bold blue]\n")
        console.print(f"[cyan]Goal:[/cyan] {goal}")
        console.print(f"[cyan]Status:[/cyan] {state.status}")
        console.print(f"[cyan]Model:[/cyan] {state.model}")
        console.print(f"[cyan]Current Task:[/cyan] {state.current_task_index + 1}")
        console.print(f"[cyan]Sessions:[/cyan] {state.session_count}")
        console.print(f"[cyan]Run ID:[/cyan] {state.run_id}")

        if state.current_pr:
            console.print(f"[cyan]Current PR:[/cyan] #{state.current_pr}")

        console.print("\n[cyan]Options:[/cyan]")
        console.print(f"  Auto-merge: {state.options.auto_merge}")
        console.print(f"  Max sessions: {state.options.max_sessions or 'unlimited'}")
        console.print(f"  Pause on PR: {state.options.pause_on_pr}")
        console.print(f"  Log level: {state.options.log_level}")
        console.print(f"  Log format: {state.options.log_format}")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


@app.command()
def plan() -> None:
    """Display the current task plan.

    Shows the markdown task list with checkboxes indicating completion status.

    Examples:
        claudetm plan
    """
    state_manager = StateManager()

    if not state_manager.exists():
        console.print("[yellow]No active task found.[/yellow]")
        raise typer.Exit(1)

    try:
        plan_content = state_manager.load_plan()

        if not plan_content:
            console.print("[yellow]No plan found.[/yellow]")
            raise typer.Exit(1)

        console.print("\n[bold blue]Task Plan[/bold blue]\n")
        console.print(Markdown(plan_content))

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


@app.command()
def logs(
    session: int | None = typer.Option(None, help="Show specific session number"),
    tail: int = typer.Option(100, "--tail", "-n", help="Number of lines to show"),
) -> None:
    """Display logs from the current run.

    Shows Claude's output, tool usage, and execution details.

    Examples:
        claudetm logs
        claudetm logs -n 50
    """
    state_manager = StateManager()

    if not state_manager.exists():
        console.print("[yellow]No active task found.[/yellow]")
        raise typer.Exit(1)

    try:
        state = state_manager.load_state()
        log_file = state_manager.get_log_file(state.run_id)

        if not log_file.exists():
            console.print("[yellow]No log file found.[/yellow]")
            raise typer.Exit(1)

        console.print(f"\n[bold blue]Logs[/bold blue] ({log_file})\n")

        with open(log_file) as f:
            lines = f.readlines()

        # Show last N lines
        for line in lines[-tail:]:
            print(line, end="")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


@app.command()
def context() -> None:
    """Display accumulated context and learnings.

    Shows insights gathered during execution that help inform future sessions.

    Examples:
        claudetm context
    """
    state_manager = StateManager()

    if not state_manager.exists():
        console.print("[yellow]No active task found.[/yellow]")
        raise typer.Exit(1)

    try:
        context_content = state_manager.load_context()

        if not context_content:
            console.print("[yellow]No context accumulated yet.[/yellow]")
            return

        console.print("\n[bold blue]Accumulated Context[/bold blue]\n")
        console.print(Markdown(context_content))

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


@app.command()
def progress() -> None:
    """Display human-readable progress summary.

    Shows what has been accomplished and what remains to be done.

    Examples:
        claudetm progress
    """
    state_manager = StateManager()

    if not state_manager.exists():
        console.print("[yellow]No active task found.[/yellow]")
        raise typer.Exit(1)

    try:
        progress_content = state_manager.load_progress()

        if not progress_content:
            console.print("[yellow]No progress recorded yet.[/yellow]")
            return

        console.print("\n[bold blue]Progress Summary[/bold blue]\n")
        console.print(Markdown(progress_content))

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


@app.command()
def comments(
    pr: int | None = typer.Option(None, "--pr", "-p", help="PR number to show comments for"),
) -> None:
    """Display PR review comments.

    Shows review comments for the current task's PR or a specified PR.

    Examples:
        claudetm comments
        claudetm comments -p 123
    """
    console.print("[bold blue]PR Comments[/bold blue]")
    # TODO: Implement comments logic
    raise typer.Exit(1)


@app.command()
def pr() -> None:
    """Display current PR status and CI checks.

    Shows the status of the PR associated with the current task.

    Examples:
        claudetm pr
    """
    console.print("[bold blue]PR Status[/bold blue]")
    # TODO: Implement pr logic
    raise typer.Exit(1)


@app.command()
def clean(force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation")) -> None:
    """Clean up task state directory.

    Removes all state files (.claude-task-master/) to start fresh.
    Use this after completing a task or to abandon a stuck task.

    Examples:
        claudetm clean       # Prompts for confirmation
        claudetm clean -f    # Force without confirmation
    """
    state_manager = StateManager()

    if not state_manager.exists():
        console.print("[yellow]No task state found.[/yellow]")
        raise typer.Exit(0)

    # Check if another session is active
    if state_manager.is_session_active():
        console.print("[bold red]Warning: Another claudetm session is active![/bold red]")
        if not force:
            confirm = typer.confirm("Force cleanup anyway? This may crash the running session")
            if not confirm:
                console.print("[yellow]Cancelled[/yellow]")
                raise typer.Exit(1)
        console.print("[yellow]Forcing cleanup of active session...[/yellow]")

    if not force:
        confirm = typer.confirm("Are you sure you want to clean all task state?")
        if not confirm:
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit(0)

    console.print("[bold red]Cleaning task state...[/bold red]")

    import shutil

    # Release any session lock before deletion
    state_manager.release_session_lock()

    if state_manager.state_dir.exists():
        shutil.rmtree(state_manager.state_dir)
        console.print("[green]✓ Task state cleaned[/green]")

    raise typer.Exit(0)


@app.command()
def doctor() -> None:
    """Check system requirements and authentication.

    Verifies:
    - Claude CLI is installed and accessible
    - OAuth credentials exist and are valid
    - Git is configured properly
    - GitHub CLI (gh) is available

    Examples:
        claudetm doctor
    """
    sys_doctor = SystemDoctor()
    success = sys_doctor.run_checks()
    raise typer.Exit(0 if success else 1)


@app.command(name="ci-status")
def ci_status(
    run_id: int | None = typer.Option(None, "--run-id", "-r", help="Specific workflow run ID"),
    limit: int = typer.Option(5, "--limit", "-l", help="Number of recent runs to show"),
) -> None:
    """Show GitHub Actions workflow run status.

    Lists recent CI runs with their status (success/failure/pending).

    Examples:
        claudetm ci-status
        claudetm ci-status -l 10
        claudetm ci-status -r 12345678
    """
    from .github.client import GitHubClient

    try:
        gh = GitHubClient()

        if run_id:
            # Show specific run status
            status = gh.get_workflow_run_status(run_id)
            console.print(status)
        else:
            # Show recent runs
            runs = gh.get_workflow_runs(limit=limit)
            if not runs:
                console.print("[yellow]No workflow runs found.[/yellow]")
                raise typer.Exit(0)

            console.print("[bold]Recent Workflow Runs:[/bold]\n")
            for run in runs:
                emoji = (
                    "✓"
                    if run.conclusion == "success"
                    else "✗"
                    if run.conclusion == "failure"
                    else "⏳"
                )
                console.print(
                    f"{emoji} [bold]#{run.id}[/bold] {run.name} "
                    f"({run.status}/{run.conclusion or 'pending'}) - {run.head_branch}"
                )

    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


@app.command(name="ci-logs")
def ci_logs(
    run_id: int | None = typer.Option(None, "--run-id", "-r", help="Specific workflow run ID"),
    lines: int = typer.Option(100, "--lines", "-n", help="Maximum lines to show"),
) -> None:
    """Show logs from failed CI runs.

    Useful for debugging CI failures without leaving the terminal.

    Examples:
        claudetm ci-logs
        claudetm ci-logs -r 12345678
        claudetm ci-logs -n 200
    """
    from .github.client import GitHubClient

    try:
        gh = GitHubClient()
        logs = gh.get_failed_run_logs(run_id, max_lines=lines)
        if logs:
            console.print(logs)
        else:
            console.print("[green]No failed runs found.[/green]")

    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


@app.command(name="pr-comments")
def pr_comments(
    pr_number: int = typer.Argument(..., help="PR number"),
    all_comments: bool = typer.Option(False, "--all", "-a", help="Include resolved comments"),
) -> None:
    """Show PR review comments formatted for addressing.

    Displays reviewer feedback grouped by file for easy reference.

    Examples:
        claudetm pr-comments 123
        claudetm pr-comments 123 --all
    """
    from .github.client import GitHubClient

    try:
        gh = GitHubClient()
        comments = gh.get_pr_comments(pr_number, only_unresolved=not all_comments)

        if comments:
            console.print(f"[bold]Review Comments for PR #{pr_number}:[/bold]\n")
            console.print(comments)
        else:
            console.print(
                f"[green]No {'unresolved ' if not all_comments else ''}comments on PR #{pr_number}.[/green]"
            )

    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


@app.command(name="pr-status")
def pr_status_cmd(
    pr_number: int = typer.Argument(..., help="PR number"),
) -> None:
    """Show PR status including CI and review comments.

    Displays CI check results and count of unresolved review threads.

    Examples:
        claudetm pr-status 123
    """
    from .github.client import GitHubClient

    try:
        gh = GitHubClient()
        status = gh.get_pr_status(pr_number)

        ci_emoji = (
            "✓"
            if status.ci_state == "SUCCESS"
            else "✗"
            if status.ci_state in ("FAILURE", "ERROR")
            else "⏳"
        )

        console.print(f"[bold]PR #{pr_number} Status:[/bold]")
        console.print(f"  {ci_emoji} CI: {status.ci_state}")
        console.print(f"  💬 Unresolved comments: {status.unresolved_threads}")

        if status.check_details:
            console.print("\n[bold]Checks:[/bold]")
            for check in status.check_details:
                check_emoji = (
                    "✓"
                    if check.get("conclusion") == "success"
                    else "✗"
                    if check.get("conclusion") == "failure"
                    else "⏳"
                )
                console.print(
                    f"  {check_emoji} {check['name']}: {check.get('conclusion') or check.get('status', 'pending')}"
                )

    except RuntimeError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from None


if __name__ == "__main__":
    app()
