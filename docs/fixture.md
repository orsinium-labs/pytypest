# Fixture

Fixtures are helper functions that are cached for the duration of a single test and may have teardown logic to be executed when the test finishes. For example, a fixture may start a database transaction for each test and then rollback that transaction when the test finishes, so that changes done by one test won't affect tests running after it.

## Defining fixtures

Fixture is a generator function decorated with `pytypest.fixture`. It has 3 parts:

1. **Setup** is everything that goes before `yield`. It prepares environment for the test, establishes connections, creates fake data.
1. **Result** is what goes on the right from `yield`. This is what the fixture returns into the test function to use.
1. **Teardown** is everything that goes after `yield`. It cleans up environment after the test, closes connections, removes data from the database.

It's similar to [@contextlib.contextmanager](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager) except that `yield` never raises an exception, even if the test fails (so you don't need to wrap it into `try-finally`).

```python
from typing import Iterator
from pytypest import fixture

cache = {}

@fixture
def get_cache() -> Iterator[dict]:
    # setup: prepare environment for the test
    old_cache = cache.copy()
    cache.clear()

    # yield fixture result for the test to use
    yield cache

    # teardown: clean up environment after the test
    cache.clear()
    cache.update(old_cache)
```

## Using fixtures

You can call fixtures from test functions and other fixtures as a regular function:

```python
cache = get_cache()
assert cache == {}
```

## Scope

You can specify `scope` for a fixture which controls when tear down will be executed. For example, `Scope.SESSION` indicates that the fixture must be executed only once for all tests. Setup will be executed when the fixture is first called and teardown will be executed when pytest finished running all the tests.

```python
from pytypest import fixture, Scope

@fixture(scope=Scope.SESSION)
def connect_to_db():
    ...
```

Be careful with the scope. If the fixture returns a mutable object, one test may change it affection all the tests running after it. Consider using [pytest-randomly](https://github.com/pytest-dev/pytest-randomly) to randomize the tests' order and catch side-effects early.

## Fixtures with arguments

Fixtures can accept arguments. It's especially useful for factories.

```python
def make_user(name: str = 'Guido') -> Iterator[User]:
    u = User(name=name)
    u.save()
    yield u
    u.delete()
```

## Caching

Fixtures **without arguments** are cached for the duration of their scope.

```python
cache1 = get_cache()
cache2 = get_cache()
assert cache1 is cache2
```

## Context manager

You can any fixture as a context manager. Then setup will be executed when entering the context and teardown when leaving it. The cached value, even if available, will not be used.

```python
with connect_to_db() as connection:
    ...
```

## Fixtures without teardown

If a fixture doesn't have teardown, you can use `return` instead of `yield`:

```python
@fixture
def make_user() -> User:
    return User()
```

You should use fixtures only if you need teardown, scoping, or caching. Otherwise, prefer plain old helper functions.

## Mixing with pytest

You can call fixtures from anywhere within running pytest tests, including other pytypest fixtures, pytest fixtures, and helper functions.

If you want to call a pytest fixture, use {py:func}`pytypest.fixtures.get_pytest_fixture`:

```python
from pytypest.fixtures import get_pytest_fixture
django_db_keepdb = get_pytest_fixture('django_db_keepdb')
```

You usually need to use it only for accessing fixtures defined in pytest plugins (like the example below fetching a fixture defined in [pytest-django](https://pytest-django.readthedocs.io/)) because [pytypest.fixtures](./fixtures.md) already defines wrappers for all built-in pytest fixtures.

## autouse

You can specify fixtures to be used automatically when entering their scope, regardless if they were explicitly called or not. It's especially useful for fixtures that ensure isolation for all tests, like the ones forbidding network interactions, unclosed files, or having unhandled warnings. Don't overuse it, though, and prefer explicitly called fixtures over implicit ones.

To register such fixtures, call `pytypest.autouse` and pass inside all fixtures that should be automatically used for all tests. The best place to do that is in `tests/conftest.py`.

```python
import os
from pytypest import autouse, fixture
from pytypest.fixtures import forbid_networking


@fixture
def ensure_environ_unchanged():
    old = os.environ.copy()
    yield
    assert os.environ == old

autouse(
    forbid_networking,
    ensure_environ_unchanged,
)
```

 The `autouse` function can be called only once, so that there is only one place in the whole project where all such fixtures are listed.
