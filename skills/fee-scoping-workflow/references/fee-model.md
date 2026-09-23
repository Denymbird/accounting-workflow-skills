# Building a rate card that prices messiness

Use this only when the firm has no rate card. The output is a worksheet, not a quote, and the
skill says so.

## Why volume alone underprices

Two clients at 200 transactions a month are not the same client. The one with a quarter of its
transactions uncategorised costs several times more to serve, because every unknown becomes a
query, an email, a wait and a re-open. Volume is the base. Messiness is the multiplier.

## A structure that works

```
Monthly fee = base + (volume rate x transactions) + (complexity loadings) x messiness factor
```

**Base.** Covers existing the client: software, file maintenance, the minimum monthly contact.
Every client pays it whether or not they trade that month.

**Volume rate.** Per transaction, usually in bands rather than linear. Banding stops a client
that grows 10 per cent triggering a repricing conversation.

**Complexity loadings.** Add for each that applies: multiple bank accounts, foreign currency,
payroll, VAT or GST, stock, multiple entities, a consolidation.

**Messiness factor.** Measured, not guessed. `practice.py volume` reports the unclassified
percentage. Set bands against it, for example under 5 per cent no loading, 5 to 15 per cent a
modest loading, over 15 per cent a significant one plus a cleanup fee in month one.

## Setting the numbers

This file deliberately contains no rates. A rate that fits a two-partner firm in Auckland does
not fit a sole practitioner in Leeds, and a number invented here would be quoted by somebody.

Derive yours from your own data: take five existing clients, pull their actual recoverable
hours for a year, run `practice.py volume` on each of their ledgers, and fit the model to what
you already earn. That is a real afternoon of work and it is the only honest way to do it.

## The reprice clause

Every quote built this way carries triggers, stated to the client up front:

- Monthly transactions exceed the heaviest month observed, for two consecutive months
- Unclassified percentage stays above the band quoted after month three
- A new complexity loading becomes applicable

A trigger agreed at quote time is a conversation. A fee increase without one is a dispute.
