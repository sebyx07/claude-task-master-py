"""GitHub commands for Claude Task Master - CI and PR operations."""

import typer
from rich.console import Console

from ..github import GitHubClient

console = Console()


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


def pr_status_cmd(
    pr_number: int = typer.Argument(..., help="PR number"),
) -> None:
    """Show PR status including CI and review comments.

    Displays CI check results and count of unresolved review threads.

    Examples:
        claudetm pr-status 123
    """
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


def register_github_commands(app: typer.Typer) -> None:
    """Register GitHub commands with the Typer app."""
    app.command(name="ci-status")(ci_status)
    app.command(name="ci-logs")(ci_logs)
    app.command(name="pr-comments")(pr_comments)
    app.command(name="pr-status")(pr_status_cmd)
