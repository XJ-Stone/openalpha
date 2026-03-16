"""CLI entry point for openalpha."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()
error_console = Console(stderr=True, style="bold red")

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _check_env() -> bool:
    """Verify that required environment / API keys are available.

    Returns True when the environment looks usable; prints a helpful
    message and returns False otherwise.
    """
    try:
        from src.config import get_settings
        settings = get_settings()
    except Exception as exc:
        error_console.print(
            Panel(
                f"[bold]Configuration error:[/bold] {exc}\n\n"
                "Make sure a [cyan].env[/cyan] file exists in the backend/ directory.\n"
                "Copy [cyan].env.example[/cyan] and fill in your API keys.",
                title="Missing configuration",
                border_style="red",
            )
        )
        return False

    provider: str = settings.llm_provider
    if provider == "anthropic" and not settings.anthropic_api_key:
        error_console.print(
            Panel(
                "[bold]ANTHROPIC_API_KEY[/bold] is not set.\n\n"
                "1. Copy [cyan].env.example[/cyan] → [cyan].env[/cyan]\n"
                "2. Add your Anthropic API key\n"
                "3. Re-run the command",
                title="Missing API key",
                border_style="red",
            )
        )
        return False

    if provider == "openai" and not settings.openai_api_key:
        error_console.print(
            Panel(
                "[bold]OPENAI_API_KEY[/bold] is not set.\n\n"
                "1. Copy [cyan].env.example[/cyan] → [cyan].env[/cyan]\n"
                "2. Add your OpenAI API key\n"
                "3. Re-run the command",
                title="Missing API key",
                border_style="red",
            )
        )
        return False

    return True


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_analyze(question: str, *, stream: bool = True, verbose: bool = False) -> None:
    """Run an investor-research analysis for *question* and display the result."""
    if not _check_env():
        raise SystemExit(1)

    from src.agent import Agent

    console.print()
    console.print(
        Panel(
            f"[bold cyan]{question}[/bold cyan]",
            title="openalpha — research query",
            border_style="blue",
        )
    )
    console.print()

    agent = Agent()

    if stream:
        _stream_analysis(agent, question, verbose=verbose)
    else:
        _batch_analysis(agent, question, verbose=verbose)


def _stream_analysis(agent: object, question: str, *, verbose: bool = False) -> None:
    """Stream LLM tokens into a Rich Live display."""
    from src.agent import Agent

    assert isinstance(agent, Agent)
    collected: list[str] = []
    gen = agent.query(question, stream=True)

    with Live(console=console, refresh_per_second=8, vertical_overflow="visible") as live:
        for chunk in gen:
            collected.append(chunk)
            live.update(Markdown("".join(collected)))

    if verbose:
        console.print()
        console.print(f"[dim]Tokens received: {len(collected)}[/dim]")


def _batch_analysis(agent: object, question: str, *, verbose: bool = False) -> None:
    """Run analysis without streaming — collect and display at once."""
    from src.agent import Agent

    assert isinstance(agent, Agent)

    with console.status("[bold green]Thinking…[/bold green]"):
        result = agent.query(question, stream=False)

    console.print()
    console.print(Panel(Markdown(result), title="Analysis", border_style="green"))


def cmd_investors(*, verbose: bool = False) -> None:
    """List all tracked investors in a rich table."""
    # Reuse the same scanning logic from the API
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from api import _scan_profiles

    profiles = _scan_profiles()

    if not profiles:
        console.print("[yellow]No investor profiles found.[/yellow]")
        console.print(
            "Add profiles under [cyan]investors/<slug>/profile.md[/cyan]."
        )
        return

    table = Table(
        title="Tracked Investors",
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
    )
    table.add_column("Name", style="bold")
    table.add_column("Slug", style="dim")
    table.add_column("Fund")
    table.add_column("Role")
    table.add_column("Sectors")
    table.add_column("Companies")
    table.add_column("Updated", style="dim")

    for p in profiles:
        sectors = ", ".join(p.get("sectors", []) or [])
        companies = ", ".join(p.get("companies", []) or [])
        table.add_row(
            p.get("name", ""),
            p.get("slug", ""),
            p.get("fund", ""),
            p.get("role", ""),
            sectors,
            companies,
            str(p.get("last_updated", "")),
        )

    console.print()
    console.print(table)
    console.print()
    console.print(f"[dim]{len(profiles)} investor(s) tracked[/dim]")


def cmd_investor(slug: str, *, verbose: bool = False) -> None:
    """Show details for a specific investor."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from api import _find_appearances, _find_profile

    meta = _find_profile(slug)

    if meta is None:
        error_console.print(f"Investor [bold]'{slug}'[/bold] not found.")
        console.print("[dim]Run [cyan]openalpha investors[/cyan] to see available slugs.[/dim]")
        raise SystemExit(1)

    # Header panel
    name: str = meta.get("name", slug)
    fund: str = meta.get("fund", "")
    role: str = meta.get("role", "")
    sectors = ", ".join(meta.get("sectors", []) or [])
    companies = ", ".join(meta.get("companies", []) or [])
    updated: str = str(meta.get("last_updated", ""))

    header_lines = [
        f"[bold]{name}[/bold]",
        f"Fund: {fund}" if fund else "",
        f"Role: {role}" if role else "",
        f"Sectors: {sectors}" if sectors else "",
        f"Companies: {companies}" if companies else "",
        f"Last updated: {updated}" if updated else "",
    ]
    header = "\n".join(line for line in header_lines if line)
    console.print()
    console.print(Panel(header, title=f"Investor — {slug}", border_style="cyan"))

    # Profile content
    content: str = meta.get("_content", "")
    if content.strip():
        console.print()
        console.print(Panel(Markdown(content), title="Profile", border_style="green"))

    # Appearances
    appearances = _find_appearances(slug)
    if appearances:
        table = Table(
            title="Appearances",
            show_header=True,
            header_style="bold cyan",
            border_style="blue",
        )
        table.add_column("Title", style="bold")
        table.add_column("Source")
        table.add_column("Date")
        table.add_column("File", style="dim")

        for a in appearances:
            table.add_row(a.title, a.source, a.date, a.file)

        console.print()
        console.print(table)
        console.print(f"\n[dim]{len(appearances)} appearance(s)[/dim]")
    else:
        console.print("\n[yellow]No appearances recorded yet.[/yellow]")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="openalpha",
        description="openalpha — AI-powered investor research from the terminal",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", default=False, help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # analyze -----------------------------------------------------------
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a research question using investor data + LLM",
    )
    analyze_parser.add_argument(
        "question",
        type=str,
        help='Research question, e.g. "What do experts say about SNOW?"',
    )
    analyze_parser.add_argument(
        "--no-stream",
        action="store_true",
        default=False,
        help="Disable streaming — collect the full response before displaying",
    )

    # investors ---------------------------------------------------------
    subparsers.add_parser("investors", help="List all tracked investors")

    # investor <slug> ---------------------------------------------------
    investor_parser = subparsers.add_parser(
        "investor",
        help="Show details for a specific investor",
    )
    investor_parser.add_argument("slug", type=str, help="Investor slug (e.g. brad-gerstner)")

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse arguments and dispatch to the appropriate command handler."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        raise SystemExit(0)

    verbose: bool = args.verbose

    if args.command == "analyze":
        cmd_analyze(args.question, stream=not args.no_stream, verbose=verbose)
    elif args.command == "investors":
        cmd_investors(verbose=verbose)
    elif args.command == "investor":
        cmd_investor(args.slug, verbose=verbose)
    else:
        parser.print_help()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
