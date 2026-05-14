"""
Convert a CSV file into a Teradata bulk-load SQL script.

Usage:
    python csv_to_teradata.py input.csv
    python csv_to_teradata.py input.csv --table claims --out claims.sql

The script infers column types by scanning the data:
    - All values parse as int      -> INTEGER
    - All values parse as decimal  -> DECIMAL(p,s)
    - All values match YYYY-MM-DD  -> DATE
    - Otherwise                    -> VARCHAR(n)  (n = max length seen, padded)

Empty cells become NULL. The first column is used as the PRIMARY INDEX
unless --pi is specified.

Output structure:
    CREATE VOLATILE TABLE ... ON COMMIT PRESERVE ROWS;
    COMMIT;
    INSERT INTO ...
    SELECT CAST(...) ... FROM (SELECT 1 AS x) d         -- first row, all CAST
    UNION ALL SELECT ... FROM (SELECT 1 AS x) d         -- subsequent rows
    ...
    ;
    COMMIT;
"""

import argparse
import csv
import re
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INT_RE = re.compile(r"^-?\d+$")
DEC_RE = re.compile(r"^-?\d+\.\d+$")


def infer_column_types(rows, headers):
    """
    Scan all rows and decide each column's Teradata type.
    Returns list of (kind, type_str) where kind in {int, dec, date, str}.
    """
    n_cols = len(headers)
    col_kinds = []

    for i in range(n_cols):
        values = [r[i] for r in rows if r[i] != ""]

        if not values:
            # All NULLs - default to VARCHAR(50)
            col_kinds.append(("str", "VARCHAR(50)"))
            continue

        is_int = all(INT_RE.match(v) for v in values)
        is_dec = all(INT_RE.match(v) or DEC_RE.match(v) for v in values)
        is_date = all(DATE_RE.match(v) for v in values)

        if is_int:
            col_kinds.append(("int", "INTEGER"))
        elif is_date:
            col_kinds.append(("date", "DATE"))
        elif is_dec:
            # Find precision and scale needed
            max_scale = 0
            max_intpart = 0
            for v in values:
                if "." in v:
                    intpart, frac = v.lstrip("-").split(".")
                    max_scale = max(max_scale, len(frac))
                    max_intpart = max(max_intpart, len(intpart))
                else:
                    max_intpart = max(max_intpart, len(v.lstrip("-")))
            precision = max_intpart + max_scale + 2  # small buffer
            scale = max_scale
            col_kinds.append(("dec", f"DECIMAL({precision},{scale})"))
        else:
            max_len = max(len(v) for v in values)
            # Pad to a sensible VARCHAR size
            padded = max(20, ((max_len // 10) + 1) * 10)
            col_kinds.append(("str", f"VARCHAR({padded})"))

    return col_kinds


def sql_literal(v, kind):
    """Format a CSV string value as a Teradata SQL literal."""
    if v == "" or v is None:
        return "NULL"
    if kind == "int":
        return str(int(v))
    if kind == "dec":
        return v  # already a numeric string
    if kind == "date":
        return f"DATE '{v}'"
    if kind == "str":
        return "'" + v.replace("'", "''") + "'"
    raise ValueError(kind)


def build_row(values, col_kinds, force_cast=False):
    """Build a comma-separated literal row. If force_cast, wrap in CAST(... AS type)."""
    parts = []
    for v, (kind, td_type) in zip(values, col_kinds):
        lit = sql_literal(v, kind)
        if force_cast:
            lit = f"CAST({lit} AS {td_type})"
        parts.append(lit)
    return ", ".join(parts)


def convert(csv_path: Path, sql_path: Path, table_name: str, pi_col: str | None):
    with open(csv_path, newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = [r for r in reader]

    if not rows:
        raise SystemExit("CSV has no data rows.")

    col_kinds = infer_column_types(rows, headers)

    # Pick primary index column
    if pi_col is None:
        pi_col = headers[0]
    elif pi_col not in headers:
        raise SystemExit(f"--pi column '{pi_col}' not in CSV headers: {headers}")

    # Build SQL
    col_defs = ",\n    ".join(
        f"{h} {kind[1]}" for h, kind in zip(headers, col_kinds)
    )
    col_names = ", ".join(headers)

    lines = []
    lines.append(f"-- Teradata bulk-load script for {table_name}")
    lines.append(f"-- {len(rows)} rows from {csv_path.name}")
    lines.append("")
    lines.append(f"CREATE VOLATILE TABLE {table_name} (")
    lines.append(f"    {col_defs}")
    lines.append(f") PRIMARY INDEX ({pi_col})")
    lines.append("ON COMMIT PRESERVE ROWS;")
    lines.append("")
    lines.append("COMMIT;")
    lines.append("")
    lines.append(f"INSERT INTO {table_name} ({col_names})")

    # First row: CAST on every column to pin types for the UNION
    first = build_row(rows[0], col_kinds, force_cast=True)
    lines.append(f"SELECT {first} FROM (SELECT 1 AS x) d")

    # Subsequent rows
    for r in rows[1:]:
        body = build_row(r, col_kinds, force_cast=False)
        lines.append(f"UNION ALL SELECT {body} FROM (SELECT 1 AS x) d")

    lines.append(";")
    lines.append("")
    lines.append("COMMIT;")
    lines.append("")

    sql_path.write_text("\n".join(lines))
    print(f"Wrote {len(rows)} rows -> {sql_path}")
    print(f"  Table:         {table_name}")
    print(f"  Primary index: {pi_col}")
    print(f"  Columns:       {len(headers)}")
    print(f"  Inferred types:")
    for h, (kind, td) in zip(headers, col_kinds):
        print(f"    {h:30s} {td}")


def main():
    p = argparse.ArgumentParser(description="Convert CSV to Teradata bulk-load SQL.")
    p.add_argument("csv_file", help="Path to input CSV file")
    p.add_argument("--table", help="Table name (defaults to CSV filename stem)")
    p.add_argument("--out", help="Output SQL path (defaults to <table>_teradata.sql)")
    p.add_argument("--pi", help="Primary index column (defaults to first column)")
    args = p.parse_args()

    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        raise SystemExit(f"File not found: {csv_path}")

    table = args.table or csv_path.stem
    sql_path = Path(args.out) if args.out else csv_path.with_name(f"{table}_teradata.sql")

    convert(csv_path, sql_path, table, args.pi)


if __name__ == "__main__":
    main()