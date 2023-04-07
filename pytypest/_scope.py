from enum import Enum


class Scope(Enum):
    """Scope for which the fixture.

    The scope defines when the fixture cache will be reset
    and the teardown executed.
    """

    FUNCTION = 'function'
    """
    Default. Teardown is called at the end of the test function.
    """

    CLASS = 'class'
    """
    Teardown is called after the last test in a test class.
    """

    MODULE = 'module'
    """
    Teardown is called after the last test in a file.
    """

    PACKAGE = 'package'
    """
    Experimental. Teardown is called after the last test in a directory.
    """

    SESSION = 'session'
    """
    Teardown is called after the last tests overall in the current session.
    """
