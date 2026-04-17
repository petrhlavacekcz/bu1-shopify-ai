#!/usr/bin/env python3
"""Read-only smoke test for iDoklad API v3."""

from __future__ import annotations

import sys

from idoklad_common import api_get, get_access_token


def summarize_collection(name: str, payload: dict) -> str:
    data = payload.get("Data", {})
    total_items = data.get("TotalItems")
    total_pages = data.get("TotalPages")
    items = data.get("Items", [])
    first_id = items[0].get("Id") if items else None
    return (
        f"{name}: ok"
        f", total_items={total_items}"
        f", total_pages={total_pages}"
        f", first_id={first_id}"
    )


def main() -> int:
    try:
        access_token, expires_in = get_access_token()
        contacts = api_get("/v3/Contacts", access_token, {"Page": 1, "PageSize": 1})
        invoices = api_get("/v3/IssuedInvoices", access_token, {"Page": 1, "PageSize": 1})

        print("iDoklad smoke test passed")
        print(f"Token: ok, expires_in={expires_in}")
        print(summarize_collection("Contacts", contacts))
        print(summarize_collection("IssuedInvoices", invoices))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"iDoklad smoke test failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
