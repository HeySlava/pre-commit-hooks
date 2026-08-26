from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path


OLD_FORMAT_RE = re.compile(
    r'(?<!%)%'
    r'(?:\([^)]+\))?'
    r'[-+0-9#*. ]*'
    r'[diouxXeEfFgGaAcrs]',
)


def check(source: str, path: str) -> list[str]:
    errors: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.BinOp):
            continue
        if not isinstance(node.op, ast.Mod):
            continue
        if not isinstance(node.left, ast.Constant):
            continue
        if not isinstance(node.left.value, str):
            continue
        if OLD_FORMAT_RE.search(node.left.value):
            errors.append(
                f'{path}:{node.lineno}: old-style string formatting with %',
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    ret = 0
    for filename in args.filenames:
        source = Path(filename).read_text(encoding='utf-8')
        try:
            errors = check(source, filename)
        except SyntaxError as exc:
            errors = [f'{filename}: cannot parse: {exc}']
        for error in errors:
            print(error)
        ret |= bool(errors)
    return ret


if __name__ == '__main__':
    sys.exit(main())
