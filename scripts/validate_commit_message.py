#!/usr/bin/env python3
"""Valida mensagens de commit conforme Conventional Commits."""

import re
import sys
from pathlib import Path

CONVENTIONAL_COMMIT_PATTERN = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(\([^)]+\))?!?: .+"
)


def validate_commit_message(message_file: Path) -> int:
    """Valida a primeira linha de uma mensagem de commit.

    Args:
        message_file: Arquivo criado pelo Git com a mensagem do commit.

    Returns:
        0 quando a mensagem é válida; 1 caso contrário.
    """
    message = message_file.read_text(encoding="utf-8").splitlines()
    subject = message[0].strip() if message else ""

    if CONVENTIONAL_COMMIT_PATTERN.fullmatch(subject):
        return 0

    print(
        "Mensagem de commit inválida. Use Conventional Commits, por exemplo:",
        file=sys.stderr,
    )
    print("  feat: adicionar endpoint de tarefas", file=sys.stderr)
    print("  fix(api): corrigir validação de UUID", file=sys.stderr)
    return 1


def main() -> int:
    """Executa a validação usando o caminho fornecido pelo Git."""
    if len(sys.argv) != 2:
        print("Uso: validate_commit_message.py <arquivo-da-mensagem>", file=sys.stderr)
        return 2

    return validate_commit_message(Path(sys.argv[1]))


if __name__ == "__main__":
    raise SystemExit(main())
