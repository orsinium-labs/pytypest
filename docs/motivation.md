# Motivation

The framework was created to solve very specific problems with pytest inherit in its design.

## pytest.fixture

1. **Fixtures aren't type annotated**. To have an autocomplete for a fixture inside of test function, I have to explicitly annotate the fixture each time I use it.
1. **Fixtures aren't namespaced**. Big projects end up with fixtures like `client_with_basket_and_items_in_it`.
1. **Tests cannot pass parameters into fixtures**. People end up making awful workarounds like overriding fixtures, or parametrizing the test for just the fixture, and it's all very implicit and hard to maintain.
1. **Fixtures can be overriden in submodules**. When there is a test function that uses `parcel` fixture, and the project defines 6 different fixtures with the same name, you need to check each one of them, and find the one that shares the most of the path with the test.
1. **Go-to-definition on fixtures doesn't work**. Again, each time you want to see the fixture implementation, it turns into a treasure hunt.
1. **Fixtures aren't namespaced**. When you have a global fixture `order` that uses a global fixture `user` and then the `user` fixture is overriden for a particular test file or by a test parameter, the `order` fiture will start using that new version. This violates [open-closed principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle) (particular test can modify a global behavior) and that's the reason why the modern practice is to prefer [composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance).
1. **The order of fixtures run is implicit**. In theory, the order of fixtures shouldn't matter because they shouldn't have implicit dependencies on each other. On practice, you often will have global side-effects in fixtures that may affect other fixtures. For example, if you add a fixture for [freezegun](https://github.com/spulec/freezegun), the time will be frozen for some fixtures but not others. And when using it as a decorator, the time won't be frozen for any fixtures at all.
1. **There is no distinction between setup and data fixtures**. When tests gets changed or copy-pasted, you often will have tests that require fixtures that it actually doesn't need. Each such fixture increases coupling and slowes down each test run.
1. **There is no lazy execution of fixtures**. If a function requires a fixture, it will be executed before the function is even called.

## pytest.mark.parametrize

1. **Arguments are positional-only**. It's ok when you have only 1-2 arguments, but when the parametrization includes multiple parameters, it gets impossible to read. You can use a dict for each parameter, but that makes sense only for relevant items, and you won't get autocomplete.
1. **Arguments can't have default values**. If you have a parameter that differs in 90% of cases, you still have to repeat it for each case.
1. **Arguments aren't type-safe**. Type-checking tests helps to ensure that type annotations for your code reflect how you use it. Without it, type annotations may lie. And documentation that lies is worse than no documentation.
1. **Test cases go before test function**. When you open a file with a test with many test cases, the first thing you see is a bunch of obscure values that don't make any sense for you yet. The test name, description, and implementation must go first, and only then specific test values, when you already know what they mean. Humans read from top to bottom.
