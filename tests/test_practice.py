"""Tests for practice.py, against a fixture with hand-computed answers.

Run:  python3 tests/test_practice.py
"""
import io
import os
import sys
from contextlib import redirect_stdout
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import practice  # noqa: E402

FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "sample_transactions.csv")


class Args:
    def __init__(self, period="", compare=""):
        self.period = period
        self.compare = compare


def run(cmd, **kw):
    rows, exceptions = practice.load(FIXTURE)
    buf = io.StringIO()
    with redirect_stdout(buf):
        practice.COMMANDS[cmd](rows, exceptions, FIXTURE, Args(**kw))
    return buf.getvalue()


def check(name, got, want):
    assert got == want, "%s: got %r, want %r" % (name, got, want)
    print("  ok  %s" % name)


def test_money_parsing():
    check("plain", practice._money("120.00"), Decimal("120.00"))
    check("comma", practice._money("1,250.50"), Decimal("1250.50"))
    check("parens are negative", practice._money("(89.10)"), Decimal("-89.10"))
    check("currency stripped", practice._money("$1,000"), Decimal("1000"))
    check("blank is None", practice._money(""), None)
    check("text is None", practice._money("abc"), None)
    check("lone dash is None", practice._money("-"), None)


def test_load():
    rows, exceptions = practice.load(FIXTURE)
    # 15 data lines, 1 has a non-numeric amount, so 14 usable rows and 1 exception.
    check("rows loaded", len(rows), 14)
    check("exceptions found", len(exceptions), 1)
    check("exception is the bad amount", exceptions[0][1], "amount is not a number")
    total = sum(r["amount"] for r in rows)
    # Hand-computed: 2400+1850+3100+900 = 8250 in. Out: 120+289.50+46.20+1000+120+78.40
    # +412+412+59+12.50 = 2549.60. Net 8250 - 2549.60 = 5700.40
    check("control total", total, Decimal("5700.40"))


def test_queries():
    out = run("queries")
    # Ask My Accountant x3, plus one row with a blank account = 4
    check("unclassified count", "UNCLASSIFIED TRANSACTIONS: 4 of 14 rows" in out, True)
    # -289.50 + -412 + -412 + -1000 = -2113.50
    check("value in query", "Value in query: -2,113.50" in out, True)
    check("groups the no-contact rows", "(no contact)" in out, True)


def test_variance():
    out = run("variance", period="2026-08", compare="2026-07")
    check("both periods in scope", "8 rows in 2026-08, 6 rows in 2026-07" in out, True)
    # Sales: Aug 3100+900 = 4000, Jul 2400+1850 = 4250, movement -250
    check("sales movement", "-250.00" in out, True)
    # Computer Expenses: Aug -120-59 = -179, Jul -120, movement -59
    check("computer expenses row", "-179.00" in out, True)


def test_tieout():
    out = run("tieout", period="2026-08")
    check("duplicate detected", "possible duplicate" in out, True)
    check("blank description flagged", "no description" in out, True)
    check("unclassified flagged", "unclassified account" in out, True)


def test_volume():
    out = run("volume")
    check("transaction count", "Transactions              14" in out, True)
    check("two months", "Months covered            2" in out, True)
    check("unclassified percentage", "Unclassified              4" in out, True)


def test_missing_column_is_an_error():
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as fh:
        fh.write("Foo,Bar\n1,2\n")
        path = fh.name
    try:
        practice.load(path)
    except practice.DataError as exc:
        check("names the missing column", "'date' not found" in str(exc), True)
    else:
        raise AssertionError("expected DataError for a CSV with no date column")
    finally:
        os.unlink(path)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        print(t.__name__)
        t()
    print("\nAll %d test groups passed." % len(tests))
