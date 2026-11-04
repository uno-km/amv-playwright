# SPDX-License-Identifier: Apache-2.0
"""Deprecated alias of :mod:`amv_playwright`.

WHAT: ``import termux_playwright`` (and ``import termux_playwright.<sub>``) keeps working and returns the
      very same module objects as ``amv_playwright``.
WHY:  the package was renamed from termux-playwright to amv-playwright in 2.0.0; user code
      written against the old import name should not break on upgrade.
HOW:  a meta-path finder maps every ``termux_playwright.*`` name to ``amv_playwright.*`` and this
      package replaces itself in ``sys.modules`` with ``amv_playwright``.

This alias will be removed in a future major release. Import ``amv_playwright`` instead.
"""
import importlib
import importlib.abc
import importlib.util
import sys
import warnings

_OLD = "termux_playwright"
_NEW = "amv_playwright"

warnings.warn(
    f"'{_OLD}' was renamed to '{_NEW}'; import '{_NEW}' instead. "
    "The old name will be removed in a future major release.",
    DeprecationWarning,
    stacklevel=2,
)


class _AliasLoader(importlib.abc.Loader):
    def create_module(self, spec):
        return importlib.import_module(_NEW + spec.name[len(_OLD):])

    def exec_module(self, module):
        return None


class _AliasFinder(importlib.abc.MetaPathFinder):
    _loader = _AliasLoader()

    def find_spec(self, fullname, path=None, target=None):
        if not fullname.startswith(_OLD + "."):
            return None
        if fullname.endswith(".__main__"):
            # Let runpy load amv_playwright/__main__.py through the normal path finder.
            return None
        return importlib.util.spec_from_loader(fullname, self._loader)


if not any(getattr(f, "_amv_alias_of", None) == _OLD for f in sys.meta_path):
    _finder = _AliasFinder()
    _finder._amv_alias_of = _OLD
    sys.meta_path.insert(0, _finder)

sys.modules[_OLD] = importlib.import_module(_NEW)
