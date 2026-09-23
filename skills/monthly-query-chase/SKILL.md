---
name: monthly-query-chase
description: Finds the transactions that cannot be classified in a client's ledger, groups them into one email per client instead of a stream of separate questions, and drafts that email. Every figure comes from a bundled script. Use when running month-end queries, chasing a client about unknown or uncategorised transactions, clearing Ask My Accountant or a suspense account, or drafting the "what was this payment" email.
---

# Monthly query chase

The job that quietly consumes a bookkeeper's week. One email per client per month, listing
every unknown transaction together, instead of six separate emails as you find them.

## The one rule

**Never compute a figure yourself.** Every amount, count and total in your output comes from
`scripts/practice.py`. Language models get arithmetic wrong on real ledgers and the failure is
quiet: the total looks reasonable and is wrong. You find out in front of the client.

## Step 1: get the transactions

Ask for a CSV export covering the period. In Xero: Accounting, Reports, Account Transactions,
export to CSV. In QuickBooks Online: Reports, Transaction List by Date, export to CSV.

Either export works. The script accepts both column namings, plus any CSV with a date, an
amount, and ideally a description, account and contact.

## Step 2: run the script

```bash
python3 scripts/practice.py queries transactions.csv
```

It prints the source file, the row count, a control total and the exception count, then every
unclassified transaction grouped by contact, with the line number of each.

A transaction counts as unclassified when its account is blank or is one of: Ask My Accountant,
Uncategorised Expense, Uncategorised Income, Suspense, Unassigned, To Be Classified.

## Step 3: read the exceptions before the queries

The script reports rows it could not read: a non-numeric amount, a missing date. These are not
queries, they are data problems, and they belong in your own list rather than the client's
email. Never let an unreadable row silently vanish from the count.

## Step 4: draft one email

Group by contact where a contact exists, because a client can answer "the three Cloudhost
payments" faster than three separate questions. Order by value, largest first, since that is
where a wrong answer costs most.

The email says what you need and makes answering easy:

```
Subject: August queries, 4 items

Hi [name],

Four transactions I could not code for August. If you can tell me what each
one was for, I will finish the month.

  14 Aug   Card payment 9920      412.00
  14 Aug   Card payment 9920      412.00   (looks like a duplicate of the above)
  12 Jul   Card payment 4417      289.50
  28 Jul   Transfer             1,000.00   (no contact on the transaction)

A one-line answer against each is plenty.

[sign off]
```

Rules for the draft:
- Never guess what a transaction was for, even when the description suggests it.
- Flag a suspected duplicate as a suspicion, not a fact.
- Do not ask about anything the client already answered last month. Ask the user whether a
  previous month's answers exist, and read them first.
- Keep it to the transactions. This is not the place for other matters.

## Step 5: report what happened

```
QUERIES FOR AUGUST
  Unclassified      4 of 14 rows
  Value in query    2,113.50
  Grouped into      2 emails (Cloudhost Ltd, plus 3 with no contact)
  Data problems     1 row with a non-numeric amount, line 15, not sent to the client
```

## What this skill does not do

- **It does not send email.** The Xero connection has no email tool. Output is a draft.
- **It does not code the transactions.** It asks the question. A human applies the answer.
- **It does not watch the ledger.** It runs when you run it.
