# API

```{eval-rst}
.. currentmodule:: pytypest
.. autosummary::
    :nosignatures:

    autouse
    case
    fixture
    parametrize
    Scope
```

## Modules

+ [pytypest.fixtures](./fixtures.md)
+ [pytypest.experimental](./experimental.md)

## Public

```{eval-rst}
.. autofunction:: autouse
.. autofunction:: case
.. autofunction:: fixture
.. autofunction:: parametrize
.. autoclass:: Scope()
    :members:
```

## Private

```{eval-rst}
.. autoclass:: pytypest._fixture.Fixture()
    :members: __call__, __enter__, setup, teardown
.. autoclass:: pytypest._case.CaseMaker()
    :members:
.. autoclass:: pytypest._case.Case()
    :members:
```
