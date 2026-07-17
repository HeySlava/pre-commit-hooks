from __future__ import annotations

from agent_hooks.empty_init_check import main


def test_empty_init_ok(tmp_path):
    init = tmp_path / '__init__.py'
    init.write_text('')
    assert main([str(init)]) == 0


def test_whitespace_only_ok(tmp_path):
    init = tmp_path / '__init__.py'
    init.write_text('\n')
    assert main([str(init)]) == 0


def test_non_empty_init_fails(tmp_path):
    init = tmp_path / '__init__.py'
    init.write_text('x = 1\n')
    assert main([str(init)]) == 1


def test_non_init_files_ignored(tmp_path):
    other = tmp_path / 'module.py'
    other.write_text('x = 1\n')
    assert main([str(other)]) == 0
