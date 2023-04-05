# Parametrize

## Intro into table-driven tests

If you already familiar with table-driven tests and `pytest.mark.parametrize`, got to the next section.

Let's say you have a function `concat` that concatenates the two given strings. For example, `concat('ohhi', 'mark')` should return `'ohhimark'`. Now, it's time to test it:

```python
def test_concat__simple():
    assert concat('ohhi', 'mark') == 'ohhimark'

def test_concat__empty():
    assert concat('', '') == ''

def test_concat__unicode():
    assert concat('привет', 'марк') == 'приветмарк'
```

Each time you want to test a new set of parameters, you have to copy-paste the whole test function body, and it doesn't scale well. Especially if the test has fixtures, setup, multiple assertions, and all that stuff. So, instead you try using a loop:

```python
def test_concat():
    cases = [
        ('ohhi', 'mark', 'ohhimark'),
        ('', '', ''),
        ('привет', 'марк', 'приветмарк'),
    ]
    for case in cases:
        a, b, exp = case
        assert concat(a, b) == exp
```

It's much easier to read and extend, but when one case fails, you don't know if other cases will fail or pass (the test function exits on the first failure) and there is no way run only this specific failing case.

Enter pytypest.

## Parametrization

The `pytypest.parametrize` function provides a nice way to parametrize tests. You pass in it a test function that accepts parameters as arguments, specify test cases as a set of function arguments, and pytypest will generate a separate test function for each case:

```python
from pytypest import case, parametrize

def _test_concat(a: str, b: str, exp: str):
    assert concat(a, b) == exp

test_concat = parametrize(
    _test_concat,
    case('ohhi', 'mark', exp='ohhimark'),
    case('', '', exp=''),
    case('привет', 'марк', exp='приветмарк'),
)
```

It is much better than the loop we had earlier:

1. You can use keyword arguments, which is great for readability when you have multiple parameters.
1. Test cases go after the test function implementation. Most humans read from top to bottom, so it helps the readability to show first the test logic and how test parameters are used (and hence what they mean) and only after that specific values for parameters.
1. For each test case, a new test will be generated. Hence you can run only specific test cases, and failures in one test case won't affect others.

## Naming test cases

By default, pytest will do its best to generate a unique name for each test case. It works well if there are just a few parameters and each is a short primitive type, but doesn't work so well for more ocmplex cases. A good test name is helpful for more descriptive failure messages. So, if you want to explicitly specify a good meaningful name for a test case, pass it as a keyword argument:

```python
test_concat = parametrize(
    _test_concat,
    case('ohhi', 'mark', exp='ohhimark'),
    empty_strings=case('', '', exp=''),
    unicode=case('привет', 'марк', exp='приветмарк'),
)
```

That's the preferred way to do that because then your IDE automatically ensures each name is unique. However, if you want to use as a name a string that isn't a valid python identifier, use `case.id` method:

```python
test_concat = parametrize(
    _test_concat,
    case('ohhi', 'mark', exp='ohhimark'),
    case.id('empty strings')('', '', exp=''),
    case.id('unicode')('привет', 'марк', exp='приветмарк'),
)
```
