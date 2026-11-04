# Copyright (c) 2026 Uno Kim / AMEVA Foundation. All rights reserved.
# SPDX-License-Identifier: Apache-2.0 OR Commercial-License
"""
amv_playwright.cli_protocol
AMEVA Component Protocol v1 — Playwright CLI 엔트리포인트

사용:
    amv-playwright component info --json
    amv-playwright component doctor-lite --json
    amv-playwright instance list --json
    amv-playwright instance start --json
    amv-playwright instance stop INSTANCE_ID --json
"""
from __future__ import annotations

import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="amv-playwright",
        description="Termux Playwright — [AMEVA Protocol v1] component/instance CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── AMEVA Component Protocol v1 ─────────────────────────────────────────
    try:
        from ameva_component.cli_support import build_protocol_subcommands, dispatch_protocol
        build_protocol_subcommands(subparsers)
        _protocol_available = True
    except ImportError:
        _protocol_available = False
    # ────────────────────────────────────────────────────────────────────────

    # 기존 별도 엔드포인트 안내 명령
    subparsers.add_parser("install", help="Install Playwright + Chromium (use amv-playwright-install)")
    subparsers.add_parser("doctor",  help="Run diagnostics (use amv-playwright-doctor)")

    args = parser.parse_args(argv)

    if args.command in ("install",):
        print("[INFO] Run 'amv-playwright-install' directly.", file=sys.stderr)
        sys.exit(0)
    elif args.command == "doctor":
        print("[INFO] Run 'amv-playwright-doctor' directly.", file=sys.stderr)
        sys.exit(0)
    elif args.command in ("component", "model", "instance") and _protocol_available:
        from ameva_component.cli_support import dispatch_protocol
        from amv_playwright.control import PlaywrightControl
        dispatch_protocol(args, PlaywrightControl())
    elif args.command in ("component", "model", "instance"):
        print("[ERROR] ameva-component-sdk not installed.", file=sys.stderr)
        sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
