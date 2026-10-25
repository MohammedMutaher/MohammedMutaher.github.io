#!/usr/bin/env python3
"""Refresh the numbers in the title card (_data/live_stats.yml).

  * Publications  -> number of works listed on your ORCID record
  * Citations     -> "All" citations on your Google Scholar profile

Runs automatically from .github/workflows/update-stats.yml (weekly).
If either source can't be reached, the previous number is kept.
Only uses the Python standard library.
"""
import datetime
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATS_FILE = ROOT / "_data" / "live_stats.yml"
CONFIG_FILE = ROOT / "_config.yml"


def read_config(key):
    match = re.search(rf"^{key}:\s*(\S+)", CONFIG_FILE.read_text(), re.M)
    return match.group(1).strip("\"'") if match else None


def http_get(url, headers=None):
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_orcid_count(payload):
    """ORCID groups duplicate versions of the same work, so count groups."""
    return len(json.loads(payload).get("group", []))


def parse_scholar_citations(html):
    """The first number in the sidebar table is the all-time citation count."""
    match = re.search(r'<td class="gsc_rsb_std">([\d,]+)</td>', html)
    return int(match.group(1).replace(",", "")) if match else None


def fetch_publications(orcid):
    payload = http_get(
        f"https://pub.orcid.org/v3.0/{orcid}/works",
        {"Accept": "application/json"},
    )
    return parse_orcid_count(payload)


def fetch_citations(scholar_id):
    html = http_get(
        f"https://scholar.google.com/citations?user={scholar_id}&hl=en",
        {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
         "Accept-Language": "en-US,en;q=0.9"},
    )
    return parse_scholar_citations(html)


def read_previous():
    previous = {}
    if STATS_FILE.exists():
        text = STATS_FILE.read_text()
        for key in ("publications", "citations"):
            match = re.search(rf'^{key}:\s*\n\s*display:\s*"?(\d+)"?', text, re.M)
            if match:
                previous[key] = int(match.group(1))
    return previous


def main():
    orcid = read_config("orcid")
    scholar_id = read_config("google_scholar")
    values = read_previous()
    got_something = False

    for key, fetch, source in (
        ("publications", lambda: fetch_publications(orcid), "ORCID"),
        ("citations", lambda: fetch_citations(scholar_id), "Google Scholar"),
    ):
        try:
            value = fetch()
        except Exception as error:  # network error, blocked, etc.
            print(f"WARNING: could not read {key} from {source}: {error}")
            continue
        if value is None:
            print(f"WARNING: {source} page did not contain a {key} number; keeping old value.")
            continue
        values[key] = value
        got_something = True
        print(f"{key}: {value} (from {source})")

    if not got_something:
        print("Nothing updated.")
        return 0

    today = datetime.date.today()
    label = f"{today.strftime('%b')} {today.day}, {today.year}"
    lines = ["# Written automatically by scripts/update_live_stats.py (weekly).",
             "# You can also edit these numbers by hand."]
    if "publications" in values:
        lines += ["publications:", f'  display: "{values["publications"]}"',
                  '  label: "Publications"']
    if "citations" in values:
        lines += ["citations:", f'  display: "{values["citations"]}"',
                  '  label: "Citations"']
    lines.append(f'updated_label: "{label}"')
    STATS_FILE.write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
