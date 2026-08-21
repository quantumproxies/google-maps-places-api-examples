"""Minimal collector runner used by the examples in this repo."""
from __future__ import annotations

import os
import time

import requests

BASE = "https://api.quanticdata.io/v1"
SESSION = requests.Session()


class CollectorError(RuntimeError):
    pass


def _headers() -> dict[str, str]:
    key = os.environ.get("QUANTICDATA_API_KEY")
    if not key:
        raise SystemExit("set QUANTICDATA_API_KEY — https://app.quanticdata.io/register")
    return {"Authorization": f"Bearer {key}"}


def collect(slug: str, **payload) -> list[dict]:
    """Run a collector and return its rows, waiting out an async run if needed."""
    r = SESSION.post(f"{BASE}/scraper/collectors/{slug}/run", json=payload,
                     headers=_headers(), timeout=180)
    data = r.json()
    if data.get("type") == "error" or not r.ok:
        raise CollectorError(f"{slug} ({r.status_code}): {data.get('message')}")

    run = data.get("payload", {})
    while run.get("status") == "queued" or run.get("status") == "running":
        time.sleep(3)
        s = SESSION.get(f"{BASE}/scraper/collectors/runs/{run['run_id']}",
                        headers=_headers(), timeout=60)
        run = s.json().get("payload", {})

    if run.get("status") not in ("done", None):
        raise CollectorError(f"{slug}: run {run.get('status')}")
    return run.get("results") or []
