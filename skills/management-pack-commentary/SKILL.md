---
name: management-pack-commentary
description: Turns period reports from Xero or QuickBooks into a one-page management commentary: what moved, by how much, and the two or three things worth a sentence. Every variance is computed by a bundled script. Use when writing management pack commentary, a monthly or quarterly board report, a variance analysis, an MI pack narrative, or explaining what changed against last month or budget.
---

# Management pack commentary

Three reports go in, a one-page commentary comes out. The draft takes minutes instead of an
afternoon, and a human edits and signs it.

## The one rule

**Never compute a variance yourself.** Every figure and percentage comes from
`scripts/practice.py`. A commentary built on a hand-totalled number is a commentary that gets
withdrawn in a board meeting.

## Step 1: get the data

Ask for a CSV export covering both periods in one file. In Xero: Accounting, Reports, Account
Transactions, set the date range to cover both months, export to CSV. In QuickBooks Online:
Reports, Transaction List by Date, same approach.

One file covering both periods matters. Two files invite a period mismatch nobody notices.

## Step 2: run the variance

```bash
python3 scripts/practice.py variance transactions.csv --period 2026-08 --compare 2026-07
```

Output is every account with the current period, the comparison period, the movement and the
percentage change, sorted by absolute movement so the largest mover is first. It also states
how many rows fell into each period, which is the check that catches a wrong date format
before it reaches the client.

If either period shows zero rows, stop. Do not write commentary from a half-loaded file.

## Step 3: pick what is worth a sentence

A management pack is not a list of every account. Three tests for inclusion:

1. **Size.** The movement is large enough to change a decision.
2. **Surprise.** The movement is not what the reader would expect.
3. **Actionability.** Somebody could do something about it.

An account that moves 4 per cent on a small base fails all three. Leave it out. Most packs
carry three to five points, not fifteen.

## Step 4: write the commentary

Structure, one page:

```
[Client] management commentary, August 2026
Prepared from the ledger export dated [date], [n] transactions.

Headline
  One or two sentences. The single thing the reader needs to know.

What moved
  - [Account]: [current] against [prior], a movement of [amount] ([percentage]).
    One sentence on why, or "cause not established from the ledger".
  - [next]

What to watch
  - The thing that is not yet a problem.

Not explained
  - [Account] moved [amount] and the ledger does not say why.
```

Rules:
- **Never invent a cause.** The ledger shows what moved, not why. If the reason is not in the
  data or given by the user, write "cause not established from the ledger". A confident wrong
  explanation is the fastest way to lose a client's trust in the whole pack.
- Every number in the prose matches the script output exactly. No rounding to make a sentence
  read better.
- State the source file and the transaction count at the top, so the reader can check it.
- Do not compare against budget unless the user supplies the budget. The ledger does not
  contain one.

## Step 5: report the limits

```
COMMENTARY DRAFTED
  Period            August 2026 against July 2026
  Rows in scope     8 and 6
  Points made       3
  Not explained     1 account, Computer Expenses, no cause in the ledger

BEFORE SENDING
  - Confirm the Computer Expenses movement with the client
  - No budget supplied, so no budget variance in this pack
```

## What this skill does not do

- **It does not explain causes.** It identifies movements. A human who knows the business
  explains them.
- **It does not do budget variance** unless a budget is supplied as data.
- **It does not sign the pack.** A named person does.
