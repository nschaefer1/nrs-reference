"""TimeClock - PyWebview desktop app.

Everything lives inside this folder: the UI in ./static and all data in ./data
(SQLite database, daily backups, and the embedded browser profile). Nothing is
written anywhere else.

Run:  python app.py      (use pythonw app.py on Windows to avoid the console window)
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
import threading
from contextlib import closing
from datetime import date
from pathlib import Path

FROZEN = getattr(sys, "frozen", False)  # True when bundled with PyInstaller
ROOT = Path(sys.executable).parent if FROZEN else Path(__file__).resolve().parent
STATIC = Path(getattr(sys, "_MEIPASS", ROOT)) / "static"
DATA = ROOT / "data"
DB = DATA / "timeclock.db"
BACKUPS = DATA / "backups"
KEEP_BACKUPS = 14

TYPES = {"work", "pto", "sick", "flex", "holiday", "comp"}
KV_KEYS = ("openClock", "config", "weekReq", "settings", "compLots", "ui")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^\d{2}:\d{2}$")
LOCK = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS entries(
    id       INTEGER PRIMARY KEY,
    date     TEXT NOT NULL,
    type     TEXT NOT NULL,
    hours    REAL NOT NULL,
    time_in  TEXT,
    time_out TEXT,
    note     TEXT
);
CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(date);
CREATE TABLE IF NOT EXISTS kv(key TEXT PRIMARY KEY, value TEXT NOT NULL);
"""


def connect() -> sqlite3.Connection:
    DATA.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB, timeout=10)
    con.executescript(SCHEMA)
    return con


def backup() -> None:
    """Copy the database once per day into ./data/backups, keeping the newest few."""
    if not DB.exists():
        return
    BACKUPS.mkdir(parents=True, exist_ok=True)
    dest = BACKUPS / f"timeclock-{date.today():%Y%m%d}.db"
    if dest.exists():
        return
    with closing(sqlite3.connect(DB)) as src, closing(sqlite3.connect(dest)) as dst:
        src.backup(dst)
    for old in sorted(BACKUPS.glob("timeclock-*.db"))[:-KEEP_BACKUPS]:
        old.unlink()


def clean_entries(raw) -> list[tuple]:
    if not isinstance(raw, list):
        raise ValueError("entries must be a list")
    rows, seen = [], set()
    for e in raw:
        if not isinstance(e, dict):
            raise ValueError(f"bad entry: {e!r}")
        eid, d, t, h = int(e["id"]), str(e["date"]), str(e["type"]), float(e["hours"])
        tin, tout, note = e.get("in"), e.get("out"), e.get("note")
        if (
            eid in seen
            or not DATE_RE.match(d)
            or t not in TYPES
            or not (0 <= h <= 24 * 7)
            or (tin is not None and not TIME_RE.match(str(tin)))
            or (tout is not None and not TIME_RE.match(str(tout)))
        ):
            raise ValueError(f"invalid entry: {e!r}")
        seen.add(eid)
        rows.append((eid, d, t, h, tin, tout, None if note is None else str(note)[:500]))
    return rows


class Api:
    """Methods here are callable from JavaScript as window.pywebview.api.<name>()."""

    def load_state(self) -> dict:
        with LOCK, closing(connect()) as con:
            entries = []
            for eid, d, t, h, tin, tout, note in con.execute(
                "SELECT id, date, type, hours, time_in, time_out, note FROM entries ORDER BY date, id"
            ):
                e = {"id": eid, "date": d, "type": t, "hours": h}
                if tin:
                    e["in"] = tin
                if tout:
                    e["out"] = tout
                if note:
                    e["note"] = note
                entries.append(e)
            state = {"entries": entries}
            for key, value in con.execute("SELECT key, value FROM kv"):
                state[key] = json.loads(value)
            return state

    def save_state(self, state: dict) -> bool:
        if not isinstance(state, dict) or "entries" not in state:
            raise ValueError("state must be an object with an 'entries' list")
        rows = clean_entries(state["entries"])  # validate everything before touching the DB
        with LOCK, closing(connect()) as con, con:  # `with con` = one transaction (commit / rollback)
            con.execute("DELETE FROM entries")
            con.executemany(
                "INSERT INTO entries(id, date, type, hours, time_in, time_out, note) VALUES (?,?,?,?,?,?,?)", rows
            )
            for key in KV_KEYS:
                if key in state:
                    con.execute(
                        "INSERT INTO kv(key, value) VALUES (?, ?) "
                        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                        (key, json.dumps(state[key])),
                    )
        return True


def set_windows_icon() -> None:
    """Windows only: give the window/taskbar our icon instead of Python's."""
    if sys.platform != "win32":
        return
    import ctypes

    user32 = ctypes.windll.user32
    # own taskbar identity so Windows doesn't group us under pythonw's icon
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("TimeClock.App")
    hwnd = user32.FindWindowW(None, "TimeClock")
    ico = str(STATIC / "icon.ico")
    for size, which in ((32, 0), (16, 0), (256, 1)):  # which: 0 = small, 1 = big
        h = user32.LoadImageW(None, ico, 1, size, size, 0x10)  # IMAGE_ICON, LR_LOADFROMFILE
        if h and hwnd:
            user32.SendMessageW(hwnd, 0x80, which, h)  # WM_SETICON


def main() -> None:
    import webview  # imported here so the data layer can be used/tested without a GUI

    DATA.mkdir(parents=True, exist_ok=True)
    backup()
    window = webview.create_window(
        "TimeClock",
        url=(STATIC / "index.html").as_uri(),
        js_api=Api(),
        width=1180,
        height=900,
        min_size=(920, 640),
        text_select=True,
        background_color="#0e0e10",
    )
    window.events.shown += set_windows_icon
    # private_mode=False + storage_path keeps the embedded browser profile inside ./data
    webview.start(private_mode=False, storage_path=str(DATA / "webview"), icon=str(STATIC / "icon.ico"))


if __name__ == "__main__":
    main()
