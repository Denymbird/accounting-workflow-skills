# Six accounting workflows for Claude, Xero and QuickBooks

Six open-source agent skills for an accounting practice. Client onboarding, the monthly query
chase, management pack commentary, the year-end review pass, fee scoping and the client email
desk. Build order included.

They work with Claude, Claude Code, Codex and Cursor, because a skill is a folder of
instructions plus a script, and the script is plain Python with no dependencies.

Built by the team at [Paidnice](https://paidnice.com).

## What a skill is

A folder holding a file of instructions in plain English, plus any scripts it needs. When you
ask a question the skill covers, the assistant loads those instructions and follows them.
There is no model training, no data upload and no new platform.

The practical effect is that a procedure stops living in one person's head. Your best preparer
writes down how your firm does a debtor review, and everyone else runs that exact review.

## The one rule these all follow

**The model never does the arithmetic.**

Language models handle twenty numbers well and a hundred badly, and the failure is quiet: the
total comes back looking reasonable and wrong. You find out in front of the client.

So every amount, count, variance and total in these skills is computed by `practice.py`, a
plain Python script. The model reads the request, runs the script, and explains the result.
Four consequences:

1. **The numbers are right.** Decimal arithmetic, not floating point, and not a model.
2. **The same question gives the same answer** every time you ask.
3. **Every output shows its workings.** Source file, row count, control total.
4. **Nothing is hidden.** Unreadable rows, missing dates and duplicates are reported as
   exceptions, never silently dropped.

The calculations are covered by tests against a fixture ledger with hand-computed answers.

```bash
python3 tests/test_practice.py
```

## Build order

Build them in this order. Most practices stop after two and that is a reasonable place to stop.

| # | Skill | Build it when | Needs a script |
|---|---|---|---|
| 1 | `monthly-query-chase` | Always first. It repeats most often and it is the least interesting work in the building | Yes |
| 2 | `client-email-desk` | Second. Highest time saved per afternoon, lowest setup | No |
| 3 | `management-pack-commentary` | When more than a handful of clients get a monthly pack | Yes |
| 4 | `onboarding-workflow` | Before you take on the next ten clients, not after | No |
| 5 | `fee-scoping-workflow` | When you suspect some clients are unprofitable and cannot prove which | Yes |
| 6 | `year-end-review-pass` | Last, because it needs your review checklist to exist in writing first | Yes |

**If you only build one, build the monthly query chase.** It happens every month for every
client, it is almost entirely templated once written down, and it is the job most likely to be
done differently by whoever picks it up that week.

## Install

```bash
git clone https://github.com/Denymbird/accounting-workflow-skills.git
```

- **Claude Code**: copy any `skills/<name>` folder into `.claude/skills/` in your project, or
  into `~/.claude/skills/` to have it everywhere.
- **claude.ai**: upload the `skills/<name>` folder in Settings, Capabilities, Skills.
- **Codex or Cursor**: point the agent at `skills/<name>/SKILL.md`.

Each folder installs on its own. Take one, take all six.

Python 3.8 or newer. Nothing to install.

## Use them

Ask in plain language. The skill picks itself up from what you asked.

```
Run the August queries for Baker Joinery from this export.
Draft the management commentary for August against July.
Scope a fee for this prospect from their last twelve months.
What did the year-end review pass find on this file?
```

## Getting the data in

Every script command reads a CSV export. You do not need a live connection.

- **Xero**: Accounting, Reports, Account Transactions. Set the date range, export to CSV.
- **QuickBooks Online**: Reports, Transaction List by Date. Set the range, export to CSV.

The script accepts either platform's column naming, plus any CSV with a date and an amount.

The CSV route is also the only one that scales across a book of clients. Every live connection
holds a single organisation, so a bookkeeper with twenty clients would reconnect twenty times.

## What these do not do

Being straight about the ceiling saves a lot of wasted setup.

- **They cannot watch your ledger.** Nothing fires when something happens. Neither the Xero
  API nor the QuickBooks API can trigger on an event. Every run starts because a person asked.
- **They mostly cannot send.** There is no email tool in the Xero connection at all, so every
  email comes out as a draft for a human to send.
- **They do not sign anything.** A review note, an engagement letter and a fee quote are all
  drafts. A qualified human reviews, signs and carries the liability.
- **They do not give tax or legal advice.** Where a technical position is needed, the draft
  marks it `[CONFIRM]` for a human rather than answering confidently.

Anything that has to happen on a schedule, without a person present, is an automation job
rather than an assistant job.

## The script

`practice.py` ships inside the four skills that need it. Four commands:

```bash
python3 practice.py queries  transactions.csv
python3 practice.py variance transactions.csv --period 2026-08 --compare 2026-07
python3 practice.py tieout   transactions.csv --period 2026
python3 practice.py volume   transactions.csv
```

Each prints its source file, row count, control total and exception list before anything else.

## Also from Paidnice

[accounts-receivable-skills](https://github.com/Denymbird/accounts-receivable-skills): aged
receivables, DSO, late fee schedules, customer statements and a ranked call sheet.

## Licence

MIT. Take it, change it, ship it in your practice.
