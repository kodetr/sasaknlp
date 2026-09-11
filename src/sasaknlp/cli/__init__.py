"""CLI package for SasakNLP."""

from typing import List, Optional


def main(argv: Optional[List[str]] = None) -> int:
    """Delegate to sasaknlp.cli.main."""
    from sasaknlp.cli.main import main as _cli_main
    return _cli_main(argv)


__all__ = ["main"]
