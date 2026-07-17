from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


def check(source: str, path: str) -> list[str]:
    errors: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.level > 0:
            errors.append(
                f'{path}:{node.lineno}: relative import is prohibited',
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
