---
name: onboarding-workflow
description: Produces the engagement letter, the information request and the AML checklist for a new accounting client from a single intake conversation, so all three say the same thing. Use when onboarding a new client, drafting an engagement letter or letter of engagement, building a client information request or record request list, running AML or KYC customer due diligence, or setting up a new client file.
---

# Client onboarding

One intake, three documents. The point is not speed on any single document. It is that the
thirtieth client gets the same three documents as the first, instead of thirty slightly
different versions accumulating in a folder.

## What this produces

1. **An engagement letter** stating scope, fee basis, responsibilities and termination.
2. **An information request** listing exactly what you need from the client, in the order it
   is easiest for them to gather.
3. **An AML and customer due diligence checklist** recording identity, beneficial ownership
   and risk rating.

All three come from one intake, so the scope in the letter matches the records requested and
the entity in the AML file.

## Step 1: run the intake

Ask these and nothing else until they are answered. Do not infer an answer, ask.

| # | Question | Why it matters downstream |
|---|---|---|
| 1 | Legal entity name, trading name, company number and registered address | Engagement letter parties, AML record |
| 2 | Entity type: sole trader, partnership, limited company, trust | Scope, filing obligations, AML approach |
| 3 | Who are the directors, partners or trustees | AML identity checks |
| 4 | Who owns more than 25 per cent | Beneficial ownership, the step most often missed |
| 5 | Financial year end | Deadlines in the letter, records requested |
| 6 | Which services: bookkeeping, year end accounts, tax, payroll, VAT or GST, advisory | Scope clause, fee basis |
| 7 | Accounting platform and whether you get access or an export | Information request wording |
| 8 | Who signs, and their role | Engagement letter signature block |
| 9 | Is this a first year, or taking over from another firm | Handover records, professional clearance |
| 10 | Anything about this client that is unusual | Risk rating, scope exclusions |

If the user cannot answer a question, write "NOT PROVIDED" in the output. Never fill a gap
with a plausible answer. An engagement letter with an invented scope is worse than no letter.

## Step 2: read the firm's own templates first

Before drafting, ask: "Do you have an existing engagement letter or information request I
should follow?" If yes, read it and match its structure, clauses and tone. The firm's own
wording has usually been through a professional body or an insurer, and yours has not.

Only if the firm has nothing, use `references/document-outlines.md`.

## Step 3: draft the three documents

Draft all three in one pass, then check them against each other:

- Every service in the engagement letter has matching records in the information request.
- Every entity named in the letter appears in the AML checklist.
- The year end in the letter matches the period in the information request.
- No service appears in the information request that is not in the scope clause.

State the check result explicitly. "Scope lists payroll, information request has no payroll
records. Add them or remove payroll from scope."

## Step 4: hand over, do not send

Output all three as drafts for a human to review and send. Say plainly what you could not
complete:

```
DRAFTED
  Engagement letter        ready for review
  Information request      ready for review
  AML checklist            incomplete: beneficial ownership NOT PROVIDED

BEFORE SENDING
  - Confirm beneficial ownership for anyone over 25 per cent
  - Partner to set the risk rating, this skill does not rate risk
  - Check the fee basis against your current rate card
```

## What this skill does not do

- **It does not set a risk rating.** AML risk is a judgment a responsible person makes and
  signs. This skill records the facts the rating is made from.
- **It does not verify identity.** No document checking, no database lookup. It produces the
  checklist a human completes.
- **It does not give legal advice.** Engagement letter clauses come from your firm's template
  or your professional body, not from a language model.
- **It does not send anything.** Everything is a draft.

## References

- `references/document-outlines.md` - fallback structures, used only when the firm has none.
- `references/aml-checklist.md` - the CDD fields to capture, and the ones people forget.
