---
name: bu1-idoklad-billing-ops
description: "Use when working on BU1 invoicing and billing operations in iDoklad: contact lookup, issued invoices, payment registration, unpaid document checks, and webhook setup. Read operations can run immediately; create, update, delete, and other write operations must always be confirmed first."
---

# BU1 iDoklad Billing Ops

Use this skill for BU1 billing work that touches iDoklad.

## When To Use

- reading contacts, invoices, payments, webhook state, or unpaid documents in iDoklad
- preparing or executing invoice creation from BU1 order data
- checking whether a contact or invoice already exists before creating a new one
- registering, correcting, or removing invoice payments
- setting up or auditing iDoklad webhooks for billing automation

## Required Context

Read these first when relevant:

- `agents.md`
- `docs/integrations-catalog.md`
- `docs/skills-roadmap.md`

Read `references/idoklad-api.md` before touching live auth, payloads, or endpoint selection.

## Operating Model

- Use iDoklad API v3 directly.
- Prefer `client_credentials` for BU1-owned agenda automation.
- Keep the skill workflow-first. Do not dump raw API docs back to the user.
- Keep reads lean and targeted.
- Keep writes narrow, explicit, and reversible.

## Confirmation Policy

Read operations do not need confirmation.

Write operations always need explicit confirmation before execution, even when the user clearly asked for the change.

This includes:

- creating, editing, or deleting contacts
- creating, editing, or deleting issued invoices
- creating, editing, or deleting payments
- creating or deleting webhooks

Before any write, do this:

1. Gather the exact target entity and required fields.
2. Run duplicate and safety checks.
3. Show a short execution summary.
4. Ask for explicit confirmation.
5. Execute only after the user confirms.

Use a confirmation prompt in this shape:

```text
Plánovaná operace v iDokladu:
- akce: create issued invoice
- kontakt: <name / id>
- kontrola duplicit: <result>
- klíčová data: <order number, amount, due date>

Potvrď prosím provedení zápisu.
```

## Workflow

### Read workflow

1. Identify the entity type: contact, invoice, payment, webhook, or unpaired document.
2. Choose the narrowest lookup key first.
3. Use pagination, sorting, and filters instead of broad pulls.
4. Return the result with the lookup logic and any uncertainty.

### Write workflow

1. Read the relevant auth and endpoint notes from `references/idoklad-api.md`.
2. Validate that required credentials are available from the environment or existing local config.
3. Build the smallest correct payload.
4. Run duplicate checks before create operations.
5. For payments, prefer fetching `IssuedDocumentPayments/Default/{documentId}` first.
6. Ask for confirmation.
7. Execute the write.
8. Return the created or changed identifiers and the next verification step.

## Duplicate Checks

Before creating a contact, check a stable combination such as:

- `CompanyName` + `IdentificationNumber`
- `CompanyName` + `VatIdentificationNumber`
- `CompanyName` + `Email`

Before creating an invoice, check a stable combination such as:

- `OrderNumber`
- `VariableSymbol`
- `PartnerId` + date + amount

Before creating a payment, check:

- target invoice id
- payment date
- amount

Before creating a webhook, check:

- callback URL
- entity type
- action type

## Mapping Hints

- BU1 customer or company record maps to `Contacts`
- BU1 order maps to `IssuedInvoices`
- settlement or bank capture maps to `IssuedDocumentPayments`
- recurring sync trigger maps to `Webhooks`

When creating invoices, keep external traceability visible:

- put the upstream order reference into `OrderNumber` when available
- keep business identifiers stable across retries
- use tags only when they help deduplication or downstream reporting

## Guardrails

- Do not ask the user to paste secrets into chat if they should already exist in config or env.
- Do not create a new contact or invoice before checking whether one already exists.
- Do not delete an entity without loading its detail first.
- Do not assume agenda defaults are safe for invoicing.
- Respect API limits and avoid wasteful polling.
- Treat date and datetime values carefully; use the format the API expects and keep timezone handling explicit.
- If credentials, agenda context, or required fields are missing, stop and say exactly what is missing.

## Expected Output

For reads, return:

- what was searched
- what was found
- what key or filter was used
- any ambiguity or next lookup

For writes before confirmation, return:

- planned action
- target entity
- duplicate-check result
- required confirmation

For writes after execution, return:

- created or changed id
- important business identifier such as document number or variable symbol
- follow-up verification step
