from enum import Enum


class Scope(Enum):
    FUNCTION = 'function'
    CLASS = 'class'
    MODULE = 'module'
    PACKAGE = 'package'
    SESSION = 'session'
