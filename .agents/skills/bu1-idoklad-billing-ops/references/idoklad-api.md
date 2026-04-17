# iDoklad API Notes

Use this file only when the task needs live iDoklad API details.

## Scope

- API docs: `https://api.idoklad.cz/Help/v3/cs/`
- Main API base: `https://api.idoklad.cz/v3/`
- API v2 support ends on `2026-09-08`

## BU1 Default Auth Choice

For BU1-owned automation, prefer `client_credentials`.

Documented token endpoint for this flow:

- `POST https://identity.idoklad.cz/server/v2/connect/token`

Required form fields:

- `grant_type=client_credentials`
- `application_id`
- `client_id`
- `client_secret`
- `scope=idoklad_api`

Observed in BU1 verification on `2026-04-17`:

- `idoklad_api` worked for read-only token + API access
- `idoklad_api offline_access` returned `invalid_scope` with the tested credentials

Treat `offline_access` as optional and credential-specific, not as a hard default for BU1 automation.

Use `authorization_code` only when the integration must operate on third-party agendas that explicitly authorize the app.

Reference endpoints:

- authorize: `GET https://identity.idoklad.cz/server/connect/authorize`
- auth-code token: `POST https://identity.idoklad.cz/server/connect/token`
- refresh token: `POST https://identity.idoklad.cz/server/connect/token`

## Important API Limits

- minute limit: `200 requests / minute`
- monthly quota depends on tariff

Keep reads narrow and avoid unnecessary retries.

## Core Endpoint Groups

### Contacts

- `GET /Contacts`
- `GET /Contacts/{id}`
- `POST /Contacts`
- `PATCH /Contacts`
- `DELETE /Contacts/{id}`

Minimal create note:

- `CompanyName` is required

Useful fields for BU1 deduplication:

- `CompanyName`
- `IdentificationNumber`
- `VatIdentificationNumber`
- `Email`

### Issued invoices

- `GET /IssuedInvoices`
- `GET /IssuedInvoices/{id}`
- `GET /IssuedInvoices/Default`
- `POST /IssuedInvoices`
- `POST /IssuedInvoices/Recount`
- `PATCH /IssuedInvoices`
- `DELETE /IssuedInvoices/{id}`

Documented required create fields include:

- `CurrencyId`
- `DateOfIssue`
- `DateOfMaturity`
- `DateOfTaxing`
- `Description`
- `DocumentSerialNumber`
- `IsEet`
- `IsIncomeTax`
- `Items`
- `NumericSequenceId`
- `PartnerId`
- `PaymentOptionId`

Useful invoice traceability fields:

- `OrderNumber`
- `VariableSymbol`
- `Tags`

### Issued document payments

- `GET /IssuedDocumentPayments`
- `GET /IssuedDocumentPayments/{id}`
- `GET /IssuedDocumentPayments/Default/{documentId}`
- `POST /IssuedDocumentPayments`
- `POST /IssuedDocumentPayments/Batch`
- `DELETE /IssuedDocumentPayments/{id}`
- `DELETE /IssuedDocumentPayments/Batch`
- `PUT /IssuedDocumentPayments/FullyPay/{id}`
- `PUT /IssuedDocumentPayments/FullyUnpay/{id}`

For new payments, fetch the default payment model first when possible.

### Unpaired documents

- `GET /UnpairedDocuments/{movementType}/{documentType}`

Useful for payment and reconciliation checks.

Documented filter columns include:

- `Id`
- `VariableSymbol`
- `PartnerId`
- `PartnerName`
- `DocumentType`
- `DateOfIssue`
- `TotalAmountRemainingToPay`
- `CurrencyId`

### Webhooks

- `GET /Webhooks`
- `GET /Webhooks/{id}`
- `POST /Webhooks`
- `DELETE /Webhooks/{id}`

Useful documented enums:

- `EntityType`: includes `IssuedInvoice = 0`, `Contact = 10`
- `ActionType`: includes `Insert = 1`, `Update = 2`, `Delete = 3`, `PaymentCreated = 4`, `PaymentDeleted = 5`

## Practical Rules

- Read operations can run without confirmation.
- Write operations must always wait for user confirmation.
- Before create operations, check for duplicates with business identifiers.
- Before delete operations, load the current detail first and include it in the confirmation summary.
- Keep request payloads as small as possible.
