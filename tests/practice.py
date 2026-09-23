#!/usr/bin/env python3
"""practice.py - every number these skills report is computed here, never by the model.

Reads a CSV export from Xero or QuickBooks Online (or any CSV with the same columns)
and answers four questions:

  queries    which transactions cannot be classified, grouped for one client email
  variance   period-on-period movement for a management pack
  tieout     control totals and breaks for a year-end review pass
  volume     transaction and account counts for pricing a new client

Every command prints its source file, the as-at date, the row count and a control
total, so the reader can check the arithmetic. Exceptions are reported, never dropped.

Python 3.8+. No dependencies.

Usage:
  python3 practice.py queries  transactions.csv
  python3 practice.py variance transactions.csv --period 2026-08 --compare 2026-07
  python3 practice.py tieout   transactions.csv --period 2026
  python3 practice.py volume   transactions.csv
"""
import argparse
import csv
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation

# Column names accepted for each field. Xero and QuickBooks name them differently.
FIELDS = {
    "date": ("date", "transaction date", "txn date", "*date"),
    "description": ("description", "memo", "narration", "reference", "name"),
    "account": ("account", "account code", "account name", "category", "split"),
    "amount": ("amount", "total", "gross", "debit", "value"),
    "contact": ("contact", "payee", "customer", "supplier", "vendor"),
}

# An account value matching one of these means the transaction is not classified.
UNCLASSIFIED = {
    "", "-", "n/a", "na", "none",
    "ask my accountant", "uncategorised expense", "uncategorized expense",
    "uncategorised income", "uncategorized income", "uncategorised asset",
    "uncategorized asset", "suspense", "suspense account", "unassigned",
    "to be classified", "query", "queries",
}


class DataError(Exception):
    """The input cannot be read. Reported to the user, never guessed around."""


def _norm(s):
    return (s or "").strip().lower()


def _money(raw):
    """Parse a money string to Decimal. Returns None when it is not a number."""
    if raw is None:
        return None
    t = str(raw).strip()
    if not t:
        return None
    neg = t.startswith("(") and t.endswith(")")
    for ch in "()$£€,ADNZUSGBEPR ":
        t = t.replace(ch, "")
    if not t or t in {"-", "."}:
        return None
    try:
        v = Decimal(t)
    except InvalidOperation:
        return None
    return -v if neg else v


def _map_columns(header):
    """Map the CSV header to our field names. Raises if a required field is absent."""
    lookup = {}
    lowered = [_norm(h) for h in header]
    for field, candidates in FIELDS.items():
        for cand in candidates:
            if cand in lowered:
                lookup[field] = header[lowered.index(cand)]
                break
    for required in ("date", "amount"):
        if required not in lookup:
            raise DataError(
                "column '%s' not found. Looked for any of: %s. Header was: %s"
                % (required, ", ".join(FIELDS[required]), ", ".join(header))
            )
    return lookup


def load(path):
    """Read the CSV into rows plus a list of exceptions. Nothing is silently dropped."""
    try:
        fh = open(path, newline="", encoding="utf-8-sig")
    except OSError as exc:
        raise DataError("cannot open %s: %s" % (path, exc))
    with fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            raise DataError("%s is empty" % path)
        cols = _map_columns(header)
        idx = {f: header.index(c) for f, c in cols.items()}
        rows, exceptions = [], []
        for n, raw in enumerate(reader, start=2):
            if not any(c.strip() for c in raw):
                continue
            if len(raw) < len(header):
                raw = raw + [""] * (len(header) - len(raw))
            amount = _money(raw[idx["amount"]])
            date = raw[idx["date"]].strip()
            if amount is None:
                exceptions.append((n, "amount is not a number", raw[idx["amount"]]))
                continue
            if not date:
                exceptions.append((n, "no date", ""))
                continue
            rows.append({
                "line": n,
                "date": date,
                "amount": amount,
                "description": raw[idx["description"]].strip() if "description" in idx else "",
                "account": raw[idx["account"]].strip() if "account" in idx else "",
                "contact": raw[idx["contact"]].strip() if "contact" in idx else "",
            })
    if not rows:
        raise DataError("no usable rows in %s (%d exceptions)" % (path, len(exceptions)))
    return rows, exceptions


def _period_of(row):
    """YYYY-MM from an ISO-ish date. Returns '' when the format is not recognised."""
    d = row["date"]
    if len(d) >= 7 and d[4] == "-":
        return d[:7]
    return ""


def _header(path, rows, exceptions, extra=""):
    total = sum(r["amount"] for r in rows)
    out = [
        "Source:        %s" % path,
        "Rows read:     %d" % len(rows),
        "Control total: %s" % _fmt(total),
    ]
    if extra:
        out.append(extra)
    out.append("Exceptions:    %d" % len(exceptions))
    for line, why, val in exceptions[:10]:
        out.append("  line %d: %s %s" % (line, why, ("(%s)" % val) if val else ""))
    if len(exceptions) > 10:
        out.append("  ... and %d more" % (len(exceptions) - 10))
    return "\n".join(out)


def _fmt(d):
    q = Decimal(d).quantize(Decimal("0.01"))
    return "{:,.2f}".format(q)


def cmd_queries(rows, exceptions, path, args):
    """Group unclassified transactions so one email can ask about all of them."""
    hits = [r for r in rows if _norm(r["account"]) in UNCLASSIFIED]
    print(_header(path, rows, exceptions))
    print()
    print("UNCLASSIFIED TRANSACTIONS: %d of %d rows" % (len(hits), len(rows)))
    if not hits:
        print("Nothing to query.")
        return
    by_contact = defaultdict(list)
    for r in hits:
        by_contact[r["contact"] or "(no contact)"].append(r)
    total = sum(r["amount"] for r in hits)
    print("Value in query: %s" % _fmt(total))
    print()
    for contact in sorted(by_contact, key=lambda c: -abs(sum(r["amount"] for r in by_contact[c]))):
        group = by_contact[contact]
        sub = sum(r["amount"] for r in group)
        print("%s  (%d item%s, %s)" % (contact, len(group), "" if len(group) == 1 else "s", _fmt(sub)))
        for r in sorted(group, key=lambda x: x["date"]):
            print("   %s  %-40s %12s  [line %d]" % (r["date"], r["description"][:40], _fmt(r["amount"]), r["line"]))
        print()


def cmd_variance(rows, exceptions, path, args):
    """Account-level movement between two periods, for management pack commentary."""
    if not args.period or not args.compare:
        raise DataError("variance needs --period and --compare, for example --period 2026-08 --compare 2026-07")
    cur = defaultdict(Decimal)
    prv = defaultdict(Decimal)
    n_cur = n_prv = 0
    for r in rows:
        p = _period_of(r)
        key = r["account"] or "(no account)"
        if p == args.period:
            cur[key] += r["amount"]; n_cur += 1
        elif p == args.compare:
            prv[key] += r["amount"]; n_prv += 1
    if n_cur == 0 and n_prv == 0:
        raise DataError("no rows in either %s or %s. Check the date format is YYYY-MM-DD." % (args.period, args.compare))
    print(_header(path, rows, exceptions,
                  "In scope:      %d rows in %s, %d rows in %s" % (n_cur, args.period, n_prv, args.compare)))
    print()
    print("%-34s %14s %14s %14s %9s" % ("Account", args.period, args.compare, "Movement", "Change"))
    print("-" * 90)
    accounts = sorted(set(cur) | set(prv), key=lambda a: -abs(cur.get(a, Decimal(0)) - prv.get(a, Decimal(0))))
    for a in accounts:
        c, p = cur.get(a, Decimal(0)), prv.get(a, Decimal(0))
        move = c - p
        pct = "n/a" if p == 0 else "{:.1f}%".format(float(move / p * 100))
        print("%-34s %14s %14s %14s %9s" % (a[:34], _fmt(c), _fmt(p), _fmt(move), pct))
    print("-" * 90)
    tc, tp = sum(cur.values()), sum(prv.values())
    print("%-34s %14s %14s %14s" % ("TOTAL", _fmt(tc), _fmt(tp), _fmt(tc - tp)))


def cmd_tieout(rows, exceptions, path, args):
    """Control totals and the breaks a reviewer has to look at."""
    scope = [r for r in rows if not args.period or _period_of(r).startswith(args.period)]
    if not scope:
        raise DataError("no rows in period %s" % args.period)
    print(_header(path, rows, exceptions,
                  "In scope:      %d rows matching %s" % (len(scope), args.period or "(all)")))
    print()
    by_account = defaultdict(Decimal)
    counts = defaultdict(int)
    for r in scope:
        by_account[r["account"] or "(no account)"] += r["amount"]
        counts[r["account"] or "(no account)"] += 1
    print("ACCOUNT TOTALS")
    for a in sorted(by_account, key=lambda x: -abs(by_account[x])):
        print("  %-40s %14s  (%d)" % (a[:40], _fmt(by_account[a]), counts[a]))
    print("  %-40s %14s" % ("TOTAL", _fmt(sum(by_account.values()))))
    print()
    print("BREAKS TO REVIEW")
    breaks = []
    for r in scope:
        if _norm(r["account"]) in UNCLASSIFIED:
            breaks.append((r, "unclassified account"))
        elif not r["description"]:
            breaks.append((r, "no description"))
    seen = defaultdict(list)
    for r in scope:
        seen[(r["date"], r["amount"], _norm(r["description"]))].append(r)
    for key, group in seen.items():
        if len(group) > 1:
            for r in group[1:]:
                breaks.append((r, "possible duplicate of line %d" % group[0]["line"]))
    if not breaks:
        print("  None.")
    for r, why in sorted(breaks, key=lambda b: b[0]["line"]):
        print("  line %-5d %s  %-30s %12s  %s" % (r["line"], r["date"], r["description"][:30], _fmt(r["amount"]), why))
    print()
    print("  %d break%s out of %d rows in scope" % (len(breaks), "" if len(breaks) == 1 else "s", len(scope)))


def cmd_volume(rows, exceptions, path, args):
    """The counts a fee is priced from, instead of a guess about how messy a client is."""
    print(_header(path, rows, exceptions))
    print()
    periods = defaultdict(int)
    accounts = set()
    contacts = set()
    unclassified = 0
    no_description = 0
    for r in rows:
        p = _period_of(r)
        if p:
            periods[p] += 1
        if r["account"]:
            accounts.add(_norm(r["account"]))
        if r["contact"]:
            contacts.add(_norm(r["contact"]))
        if _norm(r["account"]) in UNCLASSIFIED:
            unclassified += 1
        if not r["description"]:
            no_description += 1
    n_months = len(periods) or 1
    print("VOLUME")
    print("  Transactions              %d" % len(rows))
    print("  Months covered            %d" % n_months)
    print("  Transactions per month    %.1f" % (len(rows) / n_months))
    print("  Distinct accounts used    %d" % len(accounts))
    print("  Distinct contacts         %d" % len(contacts))
    print()
    print("MESSINESS")
    pct_unc = (unclassified / len(rows) * 100) if rows else 0
    pct_nod = (no_description / len(rows) * 100) if rows else 0
    print("  Unclassified              %d  (%.1f%%)" % (unclassified, pct_unc))
    print("  No description            %d  (%.1f%%)" % (no_description, pct_nod))
    print()
    print("MONTHLY SPREAD")
    for p in sorted(periods):
        print("  %s  %4d" % (p, periods[p]))
    if len(periods) > 1:
        vals = sorted(periods.values())
        print()
        print("  Lightest month %d, heaviest %d" % (vals[0], vals[-1]))
    print()
    print("These are counts, not a price. The fee model lives in references/fee-model.md.")


COMMANDS = {
    "queries": cmd_queries,
    "variance": cmd_variance,
    "tieout": cmd_tieout,
    "volume": cmd_volume,
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=sorted(COMMANDS))
    ap.add_argument("csv")
    ap.add_argument("--period", default="", help="YYYY-MM, or YYYY for tieout")
    ap.add_argument("--compare", default="", help="YYYY-MM to compare against, for variance")
    args = ap.parse_args(argv)
    try:
        rows, exceptions = load(args.csv)
        COMMANDS[args.command](rows, exceptions, args.csv, args)
    except DataError as exc:
        print("Cannot continue: %s" % exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
