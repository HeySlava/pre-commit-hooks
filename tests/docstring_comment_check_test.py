from __future__ import annotations

from agent_hooks.docstring_comment_check import check_comments
from agent_hooks.docstring_comment_check import check_docstrings
from agent_hooks.docstring_comment_check import main


def test_module_docstring_prohibited():
    errors = check_docstrings('"""Short."""\n', 'a.py')
    assert len(errors) == 1
    assert 'prohibited' in errors[0]


def test_no_docstring_ok():
    assert check_docstrings('x = 1\n', 'a.py') == []


def test_one_line_function_docstring_ok():
    source = 'def f():\n    """Short."""\n'
    assert check_docstrings(source, 'a.py') == []


def test_two_line_function_docstring_ok():
    source = 'def f():\n    """First.\n    Second."""\n'
    assert check_docstrings(source, 'a.py') == []


def test_three_line_docstring_fails():
    source = 'def f():\n    """One.\n    Two.\n    Three."""\n'
    errors = check_docstrings(source, 'a.py')
    assert len(errors) == 1
    assert 'a.py:1' in errors[0]


def test_class_docstring_fails():
    source = 'class A:\n    """a\n    b\n    c\n    """\n'
    assert len(check_docstrings(source, 'a.py')) == 1


def test_todo_comment_ok():
    assert check_comments('x = 1  # TODO: fix\n', 'a.py') == []


def test_plain_comment_fails():
    errors = check_comments('x = 1  # comment\n', 'a.py')
    assert len(errors) == 1
    assert 'a.py:1' in errors[0]


def test_shebang_ok():
    assert check_comments('#!/usr/bin/env python3\nx = 1\n', 'a.py') == []


def test_encoding_cookie_ok():
    source = '# -*- coding: utf-8 -*-\nx = 1\n'
    assert check_comments(source, 'a.py') == []


def test_main_returns_nonzero(tmp_path):
    bad = tmp_path / 'bad.py'
    bad.write_text('# nope\n')
    assert main([str(bad)]) == 1


def test_main_module_docstring_nonzero(tmp_path):
    bad = tmp_path / 'bad.py'
    bad.write_text('"""Doc."""\n')
    assert main([str(bad)]) == 1


def test_main_ok(tmp_path):
    good = tmp_path / 'good.py'
    good.write_text('def f():\n    """Ok."""\n')
    assert main([str(good)]) == 0
