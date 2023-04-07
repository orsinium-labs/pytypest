from docutils import nodes
from sphinx.application import Sphinx


project = 'pytypest'
copyright = '2023, @orsinium'
author = '@orsinium'
templates_path = ['_templates']
html_theme = 'alabaster'
autodoc_typehints_format = 'short'
autodoc_preserve_defaults = True
autodoc_member_order = 'bysource'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'myst_parser',
]


def pytest_role(
    name: str,
    rawtext: str,
    text: str,
    lineno,
    inliner,
) -> tuple[list[nodes.Node], list[nodes.system_message]]:
    """A custom RST role to interpret `:pytest:...` in docstrings.

    https://docutils.sourceforge.io/docs/howto/rst-roles.html
    """
    ref = f'https://docs.pytest.org/en/latest/reference/reference.html#{text}'
    node = nodes.reference(rawtext, text, refuri=ref)
    return [node], []


def setup(app: Sphinx) -> None:
    app.add_role('pytest', pytest_role)
