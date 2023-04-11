# Recipes

## Skipping tests

Use {pytest}`pytest.skip` to skip a test:

```python
def test_something() -> None:
    if sys.version_info < (3, 10):
        pytest.skip('unsupported python version')
    ...
```

## Fixtures' parametrization

You can use in parametrization any objects, including helper functions, fixtures, and arguments for fixtures:

```python
@fixture
def make_user(anonymous: bool):
    return User(anonymous=anonymous)

def _test_user(anonymous: bool):
    u = make_user(anonymous=anonymous)

test_user = parametrize(
    _test_user,
    case(anonymous=False),
    case(anonymous=True),
)
```
