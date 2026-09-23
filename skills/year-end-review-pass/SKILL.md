---
name: year-end-review-pass
description: Runs a second set of eyes over a client file before year end, listing what could not be tied, what looks unusual and what is missing. Control totals and breaks come from a bundled script. Use when running a year-end review, a file review or second review, a pre-close check, tie-out or control total work, or preparing a file for a partner or auditor.
---

# Year-end review pass

A second set of eyes on a file that does not have to be yours. It finds fewer things than a
senior would. It finds them on every file, at the same standard, which a senior does not.

## The one rule

**Never compute a control total yourself.** Every total, count and break comes from
`scripts/practice.py`. A review whose own arithmetic is wrong is worse than no review, because
it carries the authority of having been checked.

## Step 1: get the file

Ask for a CSV export of the full year. In Xero: Accounting, Reports, Account Transactions, set
the range to the financial year, export to CSV. In QuickBooks Online: Reports, Transaction
List by Date, same range.

Also ask what the trial balance total should be. The script computes what the export says.
Comparing the two is the first real check, and it has to be done by a human who knows which
number is authoritative.

## Step 2: run the tie-out

```bash
python3 scripts/practice.py tieout transactions.csv --period 2026
```

Output is account totals with a row count on each, a grand total, and a breaks list. The
script flags three kinds of break:

| Break | Why it matters |
|---|---|
| Unclassified account | Ask My Accountant, suspense and blanks left at year end |
| No description | Cannot be reviewed, cannot be explained to an auditor |
| Possible duplicate | Same date, same amount, same description as an earlier line |

A possible duplicate is a suspicion. Some are genuine: two identical subscription charges in
one day happen. Present it as something to look at, never as an error found.

## Step 3: check what the script cannot

The script reads one export. It does not know the business. Work through these by hand and
record the answer, including when the answer is "not checked":

- Does the export total agree to the trial balance?
- Are there transactions after year end that belong in the year, or the reverse?
- Are accruals and prepayments present, and do they look like last year's?
- Is every bank account in the export, or only some?
- Are there related party transactions, and are they disclosed?
- Did anything change in the chart of accounts during the year?

## Step 4: write the review note

```
[Client] year-end review, FY2026
Reviewed from the export dated [date], [n] transactions, control total [amount].

Tied
  Export total agrees to the trial balance.

Breaks, [n] items
  line 412   14 Aug   Card payment 9920    412.00   unclassified account
  line 413   14 Aug   Card payment 9920    412.00   possible duplicate of line 412

Not checked
  Cut-off: no post year-end data in the export, not tested.
  Bank completeness: one account in the export, client has two.

For the partner
  The two 412.00 card payments need a decision before sign-off.
```

Rules:
- **"Not checked" is a required section.** A review note that lists only what was checked
  implies everything else was. That is how a review becomes a liability.
- Never mark something as tied when you inferred it. Tied means a number was compared.
- Do not rank the severity of a break. A reviewer does that.

## What this skill does not do

- **It does not sign off.** A qualified human does, and carries the liability.
- **It does not test cut-off, completeness or valuation.** Those need more than one export.
- **It is not an audit.** It is a review pass that makes a human's review faster.
- **It does not fix anything.** It lists. A human decides and posts.
