from pytypest import fixture


def test_setup_return():
    log = []

    @fixture
    def fixt():
        log.append(42)
        return 13

    assert fixt.setup() == 13
    assert log == [42]


def test_setup_yield():
    log = []

    @fixture
    def fixt():
        log.append(42)
        yield 13

    assert fixt.setup() == 13
    assert log == [42]


def test_teardown_return():
    @fixture
    def fixt():
        return 13

    fixt.teardown()
    assert fixt.setup() == 13
    fixt.teardown()


def test_teardown_yield():
    log = []

    @fixture
    def fixt():
        yield 13
        log.append(42)

    fixt.teardown()
    assert fixt.setup() == 13
    fixt.teardown()
    assert log == [42]
