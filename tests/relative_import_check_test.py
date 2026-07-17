from __future__ import annotations

from agent_hooks.relative_import_check import check
from agent_hooks.relative_import_check import main


def test_absolute_import_ok():
    assert check('import os\nfrom os import path\n', 'a.py') == []


def test_relative_import_fails():
    errors = check('from . import x\n', 'a.py')
    assert len(errors) == 1
    assert 'a.py:1' in errors[0]


def test_relative_parent_import_fails():
    errors = check('from ..pkg import x\n', 'a.py')
    assert len(errors) == 1


def test_main_returns_nonzero(tmp_path):
    bad = tmp_path / 'bad.py'
    bad.write_text('from . import x\n')
    assert main([str(bad)]) == 1
