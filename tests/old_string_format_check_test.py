from __future__ import annotations

from agent_hooks.old_string_format_check import check
from agent_hooks.old_string_format_check import main


def test_fstring_ok():
    assert check('x = f"hello {name}"\n', 'a.py') == []


def test_format_ok():
    assert check('x = "hello {}".format(name)\n', 'a.py') == []


def test_named_format_ok():
    assert check('x = "hello {name}".format(name=name)\n', 'a.py') == []


def test_percent_s_fails():
    errors = check('x = "hello %s" % name\n', 'a.py')
    assert len(errors) == 1
    assert 'a.py:1' in errors[0]
    assert 'old-style string formatting' in errors[0]


def test_percent_d_fails():
    errors = check('x = "count %d" % n\n', 'a.py')
    assert len(errors) == 1


def test_percent_named_fails():
    errors = check('x = "%(name)s" % values\n', 'a.py')
    assert len(errors) == 1


def test_percent_escaped_ok():
    assert check('x = "100%%" % ()\n', 'a.py') == []


def test_modulo_number_ok():
    assert check('x = 5 % 2\n', 'a.py') == []


def test_percent_in_plain_string_no_op_ok():
    assert check('x = "100%"\n', 'a.py') == []


def test_main_returns_nonzero(tmp_path):
    bad = tmp_path / 'bad.py'
    bad.write_text('x = "%s" % 1\n')
    assert main([str(bad)]) == 1


def test_main_ok(tmp_path):
    good = tmp_path / 'good.py'
    good.write_text('x = f"{1}"\n')
    assert main([str(good)]) == 0
