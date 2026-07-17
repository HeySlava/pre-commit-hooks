# agent-hooks

Pre-commit хуки для правил Python из AGENTS.md.

## Хуки

| id | Проверка |
| --- | --- |
| `docstring-comment-check` | docstring модуля запрещён; docstring функции/класса — максимум 2 строки; комментарии запрещены, кроме `# TODO` (shebang и encoding-cookie разрешены) |
| `empty-init-check` | `__init__.py` должен быть пустым |
| `relative-import-check` | относительные импорты запрещены |

Версия Python не фиксируется: pre-commit запускает хуки на интерпретаторе
из своего окружения, код совместим с любым Python 3.

## Подключение в проекте

`.pre-commit-config.yaml`:

```yaml
- repo: <url-этого-репозитория>
  rev: v0.1.0
  hooks:
    - id: docstring-comment-check
    - id: empty-init-check
    - id: relative-import-check
```

## Разработка

```bash
tox -p
pre-commit run --all-files
```
