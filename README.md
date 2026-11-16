# pre-commit-hooks

Pre-commit hooks for enforcing Python code conventions.

## Hooks

| id | Check |
| --- | --- |
| `docstring-comment-check` | Module docstrings are prohibited; function and class docstrings may contain at most 2 lines; comments are prohibited except for `# TODO` (shebangs and encoding cookies are allowed) |
| `empty-init-check` | `__init__.py` must be empty |
| `old-string-format-check` | Old-style string formatting with `%` is prohibited; f-strings and `.format()` are allowed |
| `relative-import-check` | Relative imports are prohibited |

The Python version is not pinned: pre-commit runs the hooks using the interpreter
from its environment, and the code is compatible with any Python 3 version.

## Usage

Add the following to `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/HeySlava/pre-commit-hooks
  rev: v0.1.0
  hooks:
    - id: docstring-comment-check
    - id: empty-init-check
    - id: old-string-format-check
    - id: relative-import-check
```

## Development

```bash
tox -p
pre-commit run --all-files
```
