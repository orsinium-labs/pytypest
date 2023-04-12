# pytypest

Type-safe and maintainable fixtures and parametrization for [pytest](https://github.com/pytest-dev/pytest).

Features:

+ 100% type safe.
+ Great IDE integration, go-to-definition always takes you in the right place.
+ Test parametrization that is readable even with many arguments.
+ Plug-and-play integration with pytest.
+ No vendor-lock, you can use only the features you need and don't touch the rest.
+ Fixtures can be cached, and you are in control of for how long.
+ Fixtures can accept arguments.

Check out [motivation](https://pytypest.orsinium.dev/motivation.html) if you want to know more about why this project was born.

## Installation

```bash
python3 -m pip install pytypest
```

## Usage

Fixtures are regular helper functions that `yield` their result and do teardown afterwards:

```python
from typing import Iterator
from pytypest import fixture

@fixture
def get_user(anonymous: bool) -> Iterator[User]:
    u = User(anonymous=anonymous)
    u.save()
    yield u
    u.delete()

def test_user() -> None:
    u = get_user(anonymous=False)
    assert u.anonymous is False
```

Compared to built-in pytest fixtures, these are explicit, type-safe, can accept arguments, support go-to-definition in IDE, and can be used as context managers. And like pytest fixtures, they are cached and can be scoped to the module or the whole session.

Read more in the **documentation**: [pytypest.orsinium.dev](https://pytypest.orsinium.dev/).
