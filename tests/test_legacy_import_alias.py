# SPDX-License-Identifier: Apache-2.0
"""The deprecated termux_playwright import name must keep resolving to amv_playwright."""
import importlib
import subprocess
import sys
import warnings


def test_old_import_name_aliases_new_package():
    for name in [m for m in list(sys.modules) if m == "termux_playwright" or m.startswith("termux_playwright.")]:
        del sys.modules[name]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        old = importlib.import_module("termux_playwright")
    new = importlib.import_module("amv_playwright")
    assert old is new
    assert any(issubclass(w.category, DeprecationWarning) and "amv_playwright" in str(w.message) for w in caught)


def test_old_submodule_is_same_object():
    new = importlib.import_module("amv_playwright.exceptions")
    old = importlib.import_module("termux_playwright.exceptions")
    assert old is new


def test_old_import_in_fresh_interpreter():
    code = "import warnings; warnings.simplefilter('error', DeprecationWarning)\n" \
           "try:\n    import termux_playwright\nexcept DeprecationWarning:\n    print('warned')\n"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert "warned" in out.stdout
