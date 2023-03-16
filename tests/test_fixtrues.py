from pathlib import Path

import pytest
from pytypest import fixtures
import os


def test_get_request(isolated, scoped) -> None:
    with scoped('function'):
        req = fixtures.get_request()
        assert req.function is test_get_request
        assert req.scope == 'function'


def test_make_temp_dir(isolated, scoped) -> None:
    with scoped('function'):
        path = fixtures.make_temp_dir()
        assert path.is_dir()


def test_chdir(isolated, scoped) -> None:
    dir1 = Path(os.getcwd())
    with scoped('function'):
        fixtures.chdir(dir1.parent)
        dir2 = Path(os.getcwd())
        assert dir2 == dir1.parent


def test_get_pytest_fixture(isolated, scoped, tmp_path) -> None:
    with scoped('function'):
        path = fixtures.get_pytest_fixture('tmp_path')
        assert path is tmp_path


@pytest.mark.parametrize('given, expected', [
    (fixtures.capture_std, 'capsys'),
    (lambda: fixtures.capture_std(binary=True), 'capsysbinary'),
    (lambda: fixtures.capture_std(fd=True), 'capfd'),
    (lambda: fixtures.capture_std(binary=True, fd=True), 'capfdbinary'),
    (fixtures.capture_logs, 'caplog'),
    (fixtures.update_doctest_namespace, 'doctest_namespace'),
    (fixtures.monkeypatch, 'monkeypatch'),
    (fixtures.record_warnings, 'recwarn'),
])
def test_proxying(isolated, scoped, given, expected, request) -> None:
    with scoped('function'):
        fixt1 = request.getfixturevalue(expected)
        fixt2 = fixtures.get_pytest_fixture(expected)
        fixt3 = given()
        assert fixt1 is fixt2
        assert fixt2 is fixt3
