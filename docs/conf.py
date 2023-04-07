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
    'sphinx.ext.extlinks',
    'myst_parser',
]

extlinks = {
    'pytest': ('https://docs.pytest.org/en/latest/reference/reference.html#%s', '%s'),
}
