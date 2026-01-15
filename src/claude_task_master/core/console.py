"""Console output utilities with colored [claudetm] prefix."""

# ANSI color codes
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

PREFIX = f"{CYAN}{BOLD}[claudetm]{RESET}"


def info(message: str, *, end: str = "\n", flush: bool = False) -> None:
    """Print info message with prefix."""
    print(f"{PREFIX} {message}", end=end, flush=flush)


def success(message: str, *, end: str = "\n", flush: bool = False) -> None:
    """Print success message with prefix (green)."""
    print(f"{PREFIX} {GREEN}{message}{RESET}", end=end, flush=flush)


def warning(message: str, *, end: str = "\n", flush: bool = False) -> None:
    """Print warning message with prefix (yellow)."""
    print(f"{PREFIX} {YELLOW}{message}{RESET}", end=end, flush=flush)


def error(message: str, *, end: str = "\n", flush: bool = False) -> None:
    """Print error message with prefix (red)."""
    print(f"{PREFIX} {RED}{message}{RESET}", end=end, flush=flush)


def detail(message: str, *, end: str = "\n", flush: bool = False) -> None:
    """Print detail/secondary message with prefix (dim)."""
    print(f"{PREFIX} {DIM}   {message}{RESET}", end=end, flush=flush)


def tool(message: str, *, end: str = "\n", flush: bool = False) -> None:
    """Print tool-related message with prefix (magenta)."""
    print(f"{PREFIX} {MAGENTA}{message}{RESET}", end=end, flush=flush)


def stream(text: str, *, end: str = "", flush: bool = True) -> None:
    """Print streaming text (no prefix, for Claude's output)."""
    print(text, end=end, flush=flush)


def newline() -> None:
    """Print a newline."""
    print()
