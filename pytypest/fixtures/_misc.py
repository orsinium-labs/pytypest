from __future__ import annotations

import os
import socket
import unittest.mock
from pathlib import Path
from typing import (
    Callable, ContextManager, Iterator, MutableMapping, Sequence, TypeVar,
)

from .._fixture_factory import fixture
from .._hub import hub
from ._helpers import NetworkGuard


T = TypeVar('T')


@fixture
def defer(callback: Callable[[], object]) -> Iterator[None]:
    """Execute the given callback when leaving the test function.

    It's a nice way to clean up after a test function without
    creating a fixture or a context manager.

    Similar to :pytest:`pytest.FixtureRequest.addfinalizer`.

    ::

        stream = open('some-file.txt')
        defer(stream.close)

    """
    yield
    callback()


@fixture
def enter_context(manager: ContextManager[T]) -> Iterator[T]:
    """
    Enter the context manager, return its result,
    and exit the context when leaving the test function.

    It's a bit imilar to `contextlib.ExitStack` in a sense
    that it helps to keep code indentation low
    when entering multiple context managers.

    ::

        stream = enter_context(open('some_file'))

    """
    with manager as value:
        yield value


@fixture
def forbid_networking(
    *,
    allowed: Sequence[tuple[str, int]] = (),
) -> Iterator[None]:
    """Forbid network connections during the test.

    This fixture is a good candidate for :func:`pytypest.autouse`.

    The `allowed` argument accepts a sequence of `(host, port)` pairs
    to which connections should still be allowed.

    ::

        forbid_networking(allowed=[('example.com', 443)])

    """
    guard = NetworkGuard(
        allowed=frozenset(allowed),
        wrapped=socket.getaddrinfo,
    )
    socket.getaddrinfo = guard
    yield
    socket.getaddrinfo = guard.wrapped


@fixture
def chdir(path: Path | str) -> Iterator[None]:
    """Change the current working dir to the given path.

    Similar to :pytest:`pytest.MonkeyPatch.chdir`.

    ::

        chdir('/')

    """
    old_path = Path.cwd()
    os.chdir(path)
    yield
    os.chdir(old_path)


@fixture
def preserve_mapping(target: MutableMapping) -> Iterator[None]:
    """Restore the current state of the mapping after leaving the test.

    After calling the fixture, you can safely modify the given mapping,
    and these changes will be reverted before the next test starts.

    It's not a deep copy, though. If you modify a list inside of the mapping,
    that modification will escape the test.

    ::

        import sys
        preserve_mapping(sys.modules)
        sys.modules['requests'] = Mock()

    """
    with unittest.mock.patch.dict(target):
        yield


def get_project_root() -> Path:
    """Get the path to the root directory of the project.

    ::

        root = get_project_root()
        assert (root / 'pyproject.toml').exists()

    https://docs.pytest.org/en/7.1.x/reference/customize.html#finding-the-rootdir
    """
    if hub.request is None:
        raise RuntimeError('pytest plugin is not active')
    return hub.request.session.config.rootpath
