#!/usr/bin/env python3
"""
Push plan_events.json to Intervals.icu calendar.
Uses external_id for idempotent upsert — re-running updates, not duplicates.
Zero external dependencies — stdlib only (urllib).
"""

import json
import os
import sys
import base64
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

INTERVALS_BASE_URL = "https://intervals.icu/api/v1"
EXTERNAL_ID_PREFIX = "claude-plan-"
PLAN_EVENTS_FILE = Path(__file__).resolve().parent.parent / "data" / "plan_events.json"


def _api_request(method, url, auth, data=None):
    headers = {"Authorization": f"Basic {auth}", "Accept": "application/json"}
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"❌ API {e.code}: {error_body[:300]}")
        sys.exit(1)


def load_config():
    config = {}
    config_path = Path(__file__).resolve().parent.parent / ".sync_config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)

    athlete_id = config.get("athlete_id") or os.getenv("ATHLETE_ID")
    api_key = config.get("intervals_key") or os.getenv("INTERVALS_KEY")

    if not athlete_id or not api_key:
        print("❌ Нужны athlete_id и intervals_key в .sync_config.json или env vars")
        sys.exit(1)

    auth = base64.b64encode(f"API_KEY:{api_key}".encode()).decode()
    return athlete_id, auth


def load_plan_events():
    path = Path(PLAN_EVENTS_FILE)
    if not path.exists():
        print(f"❌ Файл {PLAN_EVENTS_FILE} не найден")
        sys.exit(1)

    with open(path) as f:
        events = json.load(f)

    if not isinstance(events, list) or not events:
        print(f"❌ {PLAN_EVENTS_FILE} должен быть непустым массивом")
        sys.exit(1)

    for e in events:
        required = ["category", "start_date_local", "name", "description", "external_id"]
        missing = [k for k in required if k not in e]
        if missing:
            print(f"❌ Event '{e.get('name', '?')}' — нет полей: {', '.join(missing)}")
            sys.exit(1)
        if not e["external_id"].startswith(EXTERNAL_ID_PREFIX):
            print(f"⚠️  external_id '{e['external_id']}' не начинается с '{EXTERNAL_ID_PREFIX}'")

    return events


def fetch_existing(athlete_id, auth, oldest, newest):
    params = urllib.parse.urlencode({"oldest": oldest, "newest": newest})
    url = f"{INTERVALS_BASE_URL}/athlete/{athlete_id}/events?{params}"
    return _api_request("GET", url, auth)


def check_conflicts(existing, plan_events):
    plan_dates = {e["start_date_local"][:10] for e in plan_events}
    our_ext_ids = {e["external_id"] for e in plan_events}

    conflicts = []
    for ev in existing:
        ev_date = ev.get("start_date_local", "")[:10]
        ev_ext_id = ev.get("external_id") or ""
        if ev_date in plan_dates and ev_ext_id not in our_ext_ids:
            cat = ev.get("category", "?")
            name = ev.get("name") or ev.get("description", "")[:40] or "без названия"
            conflicts.append(f"  {ev_date} — [{cat}] {name}")

    return conflicts


def push_events(athlete_id, auth, events):
    url = f"{INTERVALS_BASE_URL}/athlete/{athlete_id}/events/bulk?upsert=true"
    return _api_request("POST", url, auth, data=events)


def clear_events(athlete_id, auth, date_from, date_to):
    existing = fetch_existing(athlete_id, auth, date_from, date_to)
    to_delete = [
        {"external_id": ev["external_id"]}
        for ev in existing
        if (ev.get("external_id") or "").startswith(EXTERNAL_ID_PREFIX)
    ]

    if not to_delete:
        print(f"Нет наших events ({EXTERNAL_ID_PREFIX}*) за {date_from}..{date_to}")
        return

    print(f"Удаляю {len(to_delete)} events:")
    for d in to_delete:
        print(f"  {d['external_id']}")

    url = f"{INTERVALS_BASE_URL}/athlete/{athlete_id}/events/bulk-delete"
    result = _api_request("PUT", url, auth, data=to_delete)
    print(f"✅ Удалено: {result}")


def main():
    parser = argparse.ArgumentParser(description="Push plan_events.json → Intervals.icu")
    parser.add_argument("--dry-run", action="store_true", help="Показать events + конфликты, не отправлять")
    parser.add_argument("--clear", nargs=2, metavar=("FROM", "TO"),
                        help="Удалить наши events за период (YYYY-MM-DD YYYY-MM-DD)")
    args = parser.parse_args()

    athlete_id, auth = load_config()

    if args.clear:
        clear_events(athlete_id, auth, args.clear[0], args.clear[1])
        return

    events = load_plan_events()

    dates = [e["start_date_local"][:10] for e in events]
    oldest = min(dates)
    newest = max(dates)

    print(f"📋 {len(events)} events, {oldest} → {newest}\n")
    for e in sorted(events, key=lambda x: x["start_date_local"]):
        date = e["start_date_local"][:10]
        print(f"  {date}  {e['name']}")
    print()

    existing = fetch_existing(athlete_id, auth, oldest, newest)
    conflicts = check_conflicts(existing, events)
    if conflicts:
        print("⚠️  На эти даты уже есть другие events:")
        for c in conflicts:
            print(c)
        print()

    if args.dry_run:
        print("🔍 Dry run — ничего не отправлено")
        return

    result = push_events(athlete_id, auth, events)
    print(f"✅ Отправлено {len(result)} events в Intervals.icu")


if __name__ == "__main__":
    main()
