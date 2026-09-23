---
name: fee-scoping-workflow
description: Prices a new accounting client from their actual transaction data instead of a guess about how messy they will be. Counts and messiness measures come from a bundled script, and the firm supplies the rate card. Use when scoping a fee, quoting a new client, pricing an engagement, repricing an existing client, or working out why a client is unprofitable.
---

# Fee scoping

Underpricing the messy ones is where practice margin goes. This prices from the client's own
data: how many transactions, how many accounts, how much of it is uncategorised.

## The one rule

**Never compute a count or a price yourself.** Counts come from `scripts/practice.py`. The
price comes from the firm's rate card applied to those counts. A fee quoted from a model's
impression of a ledger is a guess wearing a number.

## Step 1: get a real sample

Ask for a CSV export covering at least three months, ideally twelve. In Xero: Accounting,
Reports, Account Transactions. In QuickBooks Online: Reports, Transaction List by Date.

Three months is the minimum that shows seasonality. One month prices the quietest month and
you find out in March.

If the prospect will not share data before quoting, say what that costs: the quote becomes a
range with a repricing clause, not a fixed fee. Write that in the output.

## Step 2: run the volume count

```bash
python3 scripts/practice.py volume transactions.csv
```

Output is three blocks:

- **Volume.** Transactions, months covered, transactions per month, distinct accounts,
  distinct contacts.
- **Messiness.** Unclassified count and percentage, missing description count and percentage.
- **Monthly spread.** Transactions per month, plus the lightest and heaviest month.

The messiness block is the part that predicts cost. Two clients with 200 transactions a month
are not the same client when one has 2 per cent unclassified and the other has 25 per cent.

## Step 3: apply the firm's rate card

Ask: "What is your rate card or pricing model?" Read it and apply it. If the firm has none,
`references/fee-model.md` sets out a structure to build one, and you say clearly that the
output is a worksheet rather than a quote.

Never invent a price point. A number in a fee quote that came from nowhere is the single most
damaging thing this skill could produce.

## Step 4: state the basis, not just the number

```
FEE SCOPING, [client]
Measured from [file], [n] transactions across [n] months.

Volume
  Transactions per month     142
  Distinct accounts          31
  Distinct contacts          58
  Lightest month 96, heaviest 211

Messiness
  Unclassified               18.3%
  No description             6.1%

Basis
  [rate card line] x [count] = [amount]
  Messiness loading applied: [yes/no, and why]

Quoted
  [amount] per month, reviewed after 3 months.

Assumptions this quote depends on
  - The export covers all bank accounts. Not verified.
  - Volume stays within the heaviest month observed, 211.
  - Unclassified percentage falls after the first quarter of cleanup.

Reprice if
  - Monthly transactions exceed 211 for two consecutive months.
  - Unclassified stays above 15% after month three.
```

The assumptions and the reprice triggers are the point. A fee without them is a fee you cannot
revisit without an awkward conversation.

## Step 5: check the quote against reality

Before presenting, ask the user one question: "Does this feel high or low against your similar
clients?" If they say low, the rate card probably does not price messiness, and that is worth
knowing before the quote goes out rather than after.

## What this skill does not do

- **It does not set prices.** The firm's rate card does. This applies it to measured counts.
- **It does not verify the export is complete.** A client can send one bank account of three.
- **It does not predict future volume.** It reports what the sample shows.
- **It does not send the quote.** Output is a worksheet for a human.

## References

- `references/fee-model.md` - how to structure a rate card that prices messiness, used only
  when the firm has no rate card of its own.
