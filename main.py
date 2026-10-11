#!/usr/bin/env python3
# Copyright (c) 2026 Uno Kim / AMEVA Foundation. All rights reserved.
# SPDX-License-Identifier: Apache-2.0 OR Commercial-License
"""Main CLI router for termux-playwright."""

import sys
from termux_playwright.__main__ import main

if __name__ == "__main__":
    sys.exit(main())

