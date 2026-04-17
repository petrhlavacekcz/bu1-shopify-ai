#!/usr/bin/env python3
"""Read-only iDoklad invoice reader.

Supports:
- invoice detail by id
- invoice list by partner and date range
- optional item expansion
- client-side filtering by country

This script never writes to iDoklad.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

from idoklad_common import api_get, get_access_token


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--invoice-id", type=int)
    parser.add_argument("--partner-id", type=int)
    parser.add_argument("--date-from")
    parser.add_argument("--date-to")
    parser.add_argument("--country-id", type=int)
    parser.add_argument("--country-name")
    parser.add_argument("--with-items", action="store_true")
    parser.add_argument("--with-detail", action="store_true")
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--max-pages", type=int, default=5)
    parser.add_argument("--max-results", type=int, default=100)
    parser.add_argument("--sort", default="DateOfIssue~Desc")
    parser.add_argument("--output-format", choices=["json", "csv"], default="json")
    parser.add_argument("--output-file")
    return parser.parse_args()


def normalize_country_name(value: str | None) -> str | None:
    if not value:
        return None
    return value.strip().casefold()


def invoice_matches_filters(invoice: dict, args: argparse.Namespace) -> bool:
    date_of_issue = invoice.get("DateOfIssue")
    if args.date_from and date_of_issue and date_of_issue < args.date_from:
        return False
    if args.date_to and date_of_issue and date_of_issue > args.date_to:
        return False

    if args.country_id is not None:
        country_id = (
            invoice.get("PartnerAddress", {}) or {}
        ).get("CountryId")
        if country_id != args.country_id:
            return False

    if args.country_name:
        country_name = normalize_country_name(
            (invoice.get("PartnerAddress", {}) or {}).get("CountryName")
        )
        if country_name != normalize_country_name(args.country_name):
            return False

    return True


def summarize_item(item: dict) -> dict:
    prices = item.get("Prices", {}) or {}
    return {
        "Id": item.get("Id"),
        "Name": item.get("Name"),
        "Amount": item.get("Amount"),
        "Unit": item.get("Unit"),
        "UnitPrice": prices.get("UnitPrice"),
        "TotalWithoutVat": prices.get("TotalWithoutVat"),
        "TotalWithVat": prices.get("TotalWithVat"),
        "VatRate": item.get("VatRate"),
        "VatRateType": item.get("VatRateType"),
    }


def summarize_invoice(invoice: dict, include_items: bool) -> dict:
    prices = invoice.get("Prices", {}) or {}
    partner_address = invoice.get("PartnerAddress", {}) or {}
    result = {
        "Id": invoice.get("Id"),
        "DocumentNumber": invoice.get("DocumentNumber"),
        "DateOfIssue": invoice.get("DateOfIssue"),
        "DateOfMaturity": invoice.get("DateOfMaturity"),
        "DateOfPayment": invoice.get("DateOfPayment"),
        "PartnerId": invoice.get("PartnerId"),
        "PartnerName": partner_address.get("CompanyName"),
        "CountryId": partner_address.get("CountryId"),
        "CountryName": partner_address.get("CountryName"),
        "Description": invoice.get("Description"),
        "VariableSymbol": invoice.get("VariableSymbol"),
        "PaymentStatus": invoice.get("PaymentStatus"),
        "CurrencyId": invoice.get("CurrencyId"),
        "OrderNumber": invoice.get("OrderNumber"),
        "TotalWithoutVat": prices.get("TotalWithoutVat"),
        "TotalWithVat": prices.get("TotalWithVat"),
        "TotalPaid": prices.get("TotalPaid"),
    }
    if include_items:
        result["Items"] = [summarize_item(item) for item in invoice.get("Items", [])]
    return result


def invoice_csv_rows(invoice: dict) -> list[dict]:
    base = {key: value for key, value in invoice.items() if key != "Items"}
    items = invoice.get("Items")
    if not items:
        return [base]

    rows: list[dict] = []
    for item in items:
        row = dict(base)
        row.update(
            {
                "ItemId": item.get("Id"),
                "ItemName": item.get("Name"),
                "ItemAmount": item.get("Amount"),
                "ItemUnit": item.get("Unit"),
                "ItemUnitPrice": item.get("UnitPrice"),
                "ItemTotalWithoutVat": item.get("TotalWithoutVat"),
                "ItemTotalWithVat": item.get("TotalWithVat"),
                "ItemVatRate": item.get("VatRate"),
                "ItemVatRateType": item.get("VatRateType"),
            }
        )
        rows.append(row)
    return rows


def write_text(value: str, output_file: str | None) -> None:
    if output_file:
        Path(output_file).write_text(value, encoding="utf-8")
        return
    print(value)


def write_csv(rows: list[dict], output_file: str | None) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    if output_file:
        handle = Path(output_file).open("w", encoding="utf-8", newline="")
        should_close = True
    else:
        handle = sys.stdout
        should_close = False

    try:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    finally:
        if should_close:
            handle.close()


def emit_output(payload: dict, args: argparse.Namespace) -> None:
    if args.output_format == "json":
        write_text(json.dumps(payload, ensure_ascii=True, indent=2), args.output_file)
        return

    if "result" in payload:
        rows = invoice_csv_rows(payload["result"])
    else:
        rows = []
        for invoice in payload.get("results", []):
            rows.extend(invoice_csv_rows(invoice))
    write_csv(rows, args.output_file)


def get_invoice_detail(token: str, invoice_id: int) -> dict:
    payload = api_get(f"/v3/IssuedInvoices/{invoice_id}", token)
    return payload.get("Data", {}) or {}


def list_invoice_candidates(token: str, args: argparse.Namespace) -> list[dict]:
    results: list[dict] = []
    filter_expr = None
    if args.partner_id is not None:
        filter_expr = f"(PartnerId~eq~{args.partner_id})"

    for page in range(1, args.max_pages + 1):
        query: dict[str, object] = {
            "page": page,
            "pagesize": args.page_size,
            "sort": args.sort,
        }
        if filter_expr:
            query["filter"] = filter_expr

        payload = api_get("/v3/IssuedInvoices", token, query)
        items = payload.get("Data", {}).get("Items", [])
        if not items:
            break
        results.extend(items)
        if len(results) >= args.max_results:
            break
    return results[: args.max_results]


def maybe_hydrate(token: str, candidates: list[dict], args: argparse.Namespace) -> list[dict]:
    needs_detail = args.with_detail or args.with_items or args.country_id is not None or bool(args.country_name)
    if not needs_detail:
        return candidates

    hydrated: list[dict] = []
    for candidate in candidates:
        invoice_id = candidate.get("Id")
        if invoice_id is None:
            continue
        hydrated.append(get_invoice_detail(token, int(invoice_id)))
    return hydrated


def main() -> int:
    args = parse_args()
    try:
        token, expires_in = get_access_token()

        output: dict[str, object] = {
            "mode": "read_only",
            "writes_performed": False,
            "token_expires_in": expires_in,
        }

        if args.invoice_id is not None:
            detail = get_invoice_detail(token, args.invoice_id)
            output["query"] = {"invoice_id": args.invoice_id}
            output["result"] = summarize_invoice(detail, include_items=args.with_items or True)
            emit_output(output, args)
            return 0

        candidates = list_invoice_candidates(token, args)
        hydrated = maybe_hydrate(token, candidates, args)
        filtered = [invoice for invoice in hydrated if invoice_matches_filters(invoice, args)]

        output["query"] = {
            "partner_id": args.partner_id,
            "date_from": args.date_from,
            "date_to": args.date_to,
            "country_id": args.country_id,
            "country_name": args.country_name,
            "with_items": args.with_items,
            "with_detail": args.with_detail,
            "page_size": args.page_size,
            "max_pages": args.max_pages,
            "max_results": args.max_results,
            "sort": args.sort,
        }
        output["stats"] = {
            "candidate_count": len(candidates),
            "hydrated_count": len(hydrated),
            "result_count": len(filtered),
        }
        output["results"] = [
            summarize_invoice(invoice, include_items=args.with_items) for invoice in filtered
        ]
        emit_output(output, args)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"idoklad read invoices failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
