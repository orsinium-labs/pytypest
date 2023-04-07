# Fixture

...

## Defining fixtures

...

## Using fixtures

...

## Scope

...

## Caching

...

## Context manager

...

## Fixtures without teardown

If a fixture doesn't have teardown, you can use `return` instead of `yield`:

```python
@fixture
def get_user() -> User:
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

...
