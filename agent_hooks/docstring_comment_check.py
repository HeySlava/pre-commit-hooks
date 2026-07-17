from __future__ import annotations

import argparse
import ast
import io
import re
import sys
import tokenize
from pathlib import Path

MAX_DOCSTRING_LINES = 2
DOCSTRING_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
ENCODING_RE = re.compile(r'coding[:=]\s*[-\w.]+')


def check_docstrings(source: str, path: str) -> list[str]:
    errors: list[str] = []
    tree = ast.parse(source)
    if ast.get_docstring(tree, clean=False) is not None:
        errors.append(f'{path}:1: module docstring is prohibited')
    for node in ast.walk(tree):
        if not isinstance(node, DOCSTRING_NODES):
            continue
        doc = ast.get_docstring(node, clean=False)
        if doc is None:
            continue
        text = doc.strip('\n')
        lines = text.splitlines() if text.strip() else []
        if len(lines) > MAX_DOCSTRING_LINES:
            errors.append(
                f'{path}:{node.lineno}: docstring of {node.name!r} has '
                f'{len(lines)} lines (max {MAX_DOCSTRING_LINES})',
            )
    return errors


def _is_allowed_comment(tok: tokenize.TokenInfo) -> bool:
    if tok.start[0] == 1 and tok.string.startswith('#!'):
        return True
    if tok.start[0] <= 2 and ENCODING_RE.search(tok.string):
        return True
    return tok.string.lstrip('#').strip().upper().startswith('TODO')


def check_comments(source: str, path: str) -> list[str]:
    errors: list[str] = []
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type != tokenize.COMMENT or _is_allowed_comment(tok):
            continue
        msg = 'comment not allowed (only # TODO): '
        errors.append(f'{path}:{tok.start[0]}: {msg}{tok.string}')
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    ret = 0
    for filename in args.filenames:
        source = Path(filename).read_text(encoding='utf-8')
        try:
            errors = check_docstrings(source, filename)
            errors += check_comments(source, filename)
        except (SyntaxError, tokenize.TokenError) as exc:
            errors = [f'{filename}: cannot parse: {exc}']
        for error in errors:
            print(error)
        ret |= bool(errors)
    return ret


if __name__ == '__main__':
    sys.exit(main())
