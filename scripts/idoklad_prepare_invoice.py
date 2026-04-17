#!/usr/bin/env python3
"""Prepare-only helper for iDoklad invoice workflows.

This script never writes to iDoklad. It resolves a partner context, inspects
recent invoices, and outputs a draft payload skeleton plus missing fields.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

from idoklad_common import api_get, get_access_token


def build_contact_filter(args: argparse.Namespace) -> tuple[str, str] | None:
    if args.partner_id:
        return None
    if args.identification_number:
        return "IdentificationNumber", args.identification_number
    if args.vat_identification_number:
        return "VatIdentificationNumber", args.vat_identification_number
    if args.email:
        return "Email", args.email
    if args.company_name:
        return "CompanyName", args.company_name
    return None


def lookup_partner(token: str, args: argparse.Namespace) -> tuple[dict | None, list[dict], str | None]:
    if args.partner_id:
        detail = api_get(f"/v3/Contacts/{args.partner_id}", token)
        return detail.get("Data"), [], f"partner id {args.partner_id}"

    filter_spec = build_contact_filter(args)
    if not filter_spec:
        return None, [], None

    field, value = filter_spec
    payload = api_get(
        "/v3/Contacts",
        token,
        {
            "filter": f"({field}~eq~{value})",
            "page": 1,
            "pagesize": 5,
            "sort": "CompanyName~Asc",
        },
    )
    items = payload.get("Data", {}).get("Items", [])
    if len(items) == 1:
        detail = api_get(f"/v3/Contacts/{items[0]['Id']}", token)
        return detail.get("Data"), items, f"{field}={value}"
    return None, items, f"{field}={value}"


def recent_invoices(token: str, partner_id: int) -> list[dict]:
    payload = api_get(
        "/v3/IssuedInvoices",
        token,
        {
            "filter": f"(PartnerId~eq~{partner_id})",
            "page": 1,
            "pagesize": 5,
            "sort": "DateOfIssue~Desc",
        },
    )
    return payload.get("Data", {}).get("Items", [])


def best_effort_invoice_defaults(token: str) -> tuple[dict, list[str]]:
    notes: list[str] = []
    defaults: dict = {}

    try:
        payload = api_get("/v3/IssuedInvoices/Default", token)
        defaults = payload.get("Data", {}) or {}
        if defaults:
            notes.append("Loaded agenda defaults from IssuedInvoices/Default.")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"IssuedInvoices/Default was not usable without extra input: {exc}")

    if not defaults.get("PaymentOptionId"):
        payment_options = api_get(
            "/v3/PaymentOptions",
            token,
            {"page": 1, "pagesize": 50, "sort": "Id~Asc"},
        ).get("Data", {}).get("Items", [])
        default_payment = next((item for item in payment_options if item.get("IsDefault")), None)
        if default_payment:
            defaults["PaymentOptionId"] = default_payment.get("Id")
            notes.append("Filled PaymentOptionId from default payment option list entry.")

    if not defaults.get("NumericSequenceId"):
        sequences = api_get(
            "/v3/NumericSequences",
            token,
            {
                "filter": "(DocumentType~eq~0)",
                "page": 1,
                "pagesize": 50,
                "sort": "Id~Asc",
            },
        ).get("Data", {}).get("Items", [])
        default_sequence = next((item for item in sequences if item.get("IsDefault")), None)
        if default_sequence:
            defaults["NumericSequenceId"] = default_sequence.get("Id")
            notes.append("Filled NumericSequenceId from default issued-invoice sequence.")

    if not defaults.get("CurrencyId"):
        currencies = api_get(
            "/v3/Currencies",
            token,
            {"page": 1, "pagesize": 50, "sort": "Priority~Desc"},
        ).get("Data", {}).get("Items", [])
        if currencies:
            defaults["CurrencyId"] = currencies[0].get("Id")
            notes.append("Filled CurrencyId from highest-priority currency list entry.")

    return defaults, notes


def build_items(args: argparse.Namespace) -> list[dict]:
    if not args.item_name:
        return []

    return [
        {
            "Name": args.item_name,
            "Amount": args.item_amount,
            "UnitPrice": args.item_unit_price,
            "Unit": args.item_unit,
            "PriceType": args.item_price_type,
            "VatRateType": args.item_vat_rate_type,
            "IsTaxMovement": args.item_is_tax_movement,
            "ItemType": 0,
        }
    ]


def build_draft(
    args: argparse.Namespace,
    partner: dict | None,
    invoices: list[dict],
    invoice_defaults: dict,
) -> dict:
    today = dt.date.today()
    due_date = today + dt.timedelta(days=args.days_until_due)
    latest = invoices[0] if invoices else {}
    items = build_items(args)

    draft = {
        "Description": args.description,
        "DateOfIssue": today.isoformat(),
        "DateOfTaxing": today.isoformat(),
        "DateOfMaturity": due_date.isoformat(),
        "PartnerId": partner.get("Id") if partner else None,
        "CurrencyId": args.currency_id or latest.get("CurrencyId") or invoice_defaults.get("CurrencyId"),
        "PaymentOptionId": args.payment_option_id or latest.get("PaymentOptionId") or invoice_defaults.get("PaymentOptionId"),
        "NumericSequenceId": args.numeric_sequence_id or latest.get("NumericSequenceId") or invoice_defaults.get("NumericSequenceId"),
        "OrderNumber": args.order_number,
        "VariableSymbol": args.variable_symbol,
        "Items": items,
    }
    missing = [
        field
        for field in ["PartnerId", "CurrencyId", "PaymentOptionId", "NumericSequenceId"]
        if not draft.get(field)
    ]
    if not args.description:
        missing.append("Description")
    if not args.order_number:
        missing.append("OrderNumber")
    if not args.variable_symbol:
        missing.append("VariableSymbol")
    if not draft["Items"]:
        missing.append("Items")

    return {"draft": draft, "missing_required_or_recommended_fields": missing}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partner-id", type=int)
    parser.add_argument("--company-name")
    parser.add_argument("--identification-number")
    parser.add_argument("--vat-identification-number")
    parser.add_argument("--email")
    parser.add_argument("--description", default="BU1 draft invoice")
    parser.add_argument("--order-number")
    parser.add_argument("--variable-symbol")
    parser.add_argument("--days-until-due", type=int, default=14)
    parser.add_argument("--currency-id", type=int)
    parser.add_argument("--payment-option-id", type=int)
    parser.add_argument("--numeric-sequence-id", type=int)
    parser.add_argument("--item-name")
    parser.add_argument("--item-amount", type=float, default=1.0)
    parser.add_argument("--item-unit-price", type=float, default=0.0)
    parser.add_argument("--item-unit", default="ks")
    parser.add_argument("--item-price-type", type=int, default=0)
    parser.add_argument("--item-vat-rate-type", type=int, default=1)
    parser.add_argument("--item-is-tax-movement", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    try:
        token, expires_in = get_access_token()
        partner, matches, lookup_key = lookup_partner(token, args)
        invoice_defaults, default_notes = best_effort_invoice_defaults(token)

        output: dict[str, object] = {
            "mode": "prepare_only",
            "writes_performed": False,
            "token_expires_in": expires_in,
            "lookup_key": lookup_key,
            "notes": [
                "This script does not create or update anything in iDoklad.",
                "IssuedInvoices list filtering does not expose OrderNumber, so duplicate checks by order number need a broader strategy than a simple list filter.",
            ]
            + default_notes,
        }

        if lookup_key and partner is None:
            output["partner_lookup_status"] = "ambiguous" if matches else "not_found"
            output["partner_matches"] = [
                {
                    "Id": item.get("Id"),
                    "CompanyName": item.get("CompanyName"),
                    "IdentificationNumber": item.get("IdentificationNumber"),
                    "Email": item.get("Email"),
                }
                for item in matches
            ]
            print(json.dumps(output, ensure_ascii=True, indent=2))
            return 0

        if partner is None:
            output["partner_lookup_status"] = "missing_input"
            output["partner_matches"] = []
            print(json.dumps(output, ensure_ascii=True, indent=2))
            return 0

        invoices = recent_invoices(token, int(partner["Id"]))
        output["partner_lookup_status"] = "resolved"
        output["partner"] = {
            "Id": partner.get("Id"),
            "CompanyName": partner.get("CompanyName"),
            "IdentificationNumber": partner.get("IdentificationNumber"),
            "Email": partner.get("Email"),
            "DefaultInvoiceMaturity": partner.get("DefaultInvoiceMaturity"),
        }
        output["recent_invoices"] = [
            {
                "Id": item.get("Id"),
                "DocumentNumber": item.get("DocumentNumber"),
                "DateOfIssue": item.get("DateOfIssue"),
                "DateOfMaturity": item.get("DateOfMaturity"),
                "PartnerId": item.get("PartnerId"),
                "CurrencyId": item.get("CurrencyId"),
                "PaymentStatus": item.get("PaymentStatus"),
            }
            for item in invoices
        ]
        output["invoice_defaults"] = {
            "CurrencyId": invoice_defaults.get("CurrencyId"),
            "PaymentOptionId": invoice_defaults.get("PaymentOptionId"),
            "NumericSequenceId": invoice_defaults.get("NumericSequenceId"),
        }
        output.update(build_draft(args, partner, invoices, invoice_defaults))

        print(json.dumps(output, ensure_ascii=True, indent=2))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"idoklad prepare-only failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
