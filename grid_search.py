"""Sweep many cities for the same query and de-duplicate by place_id.

One local pack is a sample. A grid is a dataset. Overlap between neighbouring
cities is normal — that is exactly why the dedup key is place_id and not name.

    python3 grid_search.py "vegan bakery" --cities cities.txt --max 40
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from client import CollectorError, collect

DEFAULT_CITIES = [
    "New York, New York, United States",
    "Brooklyn, New York, United States",
    "Jersey City, New Jersey, United States",
    "Newark, New Jersey, United States",
    "Yonkers, New York, United States",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--cities", type=pathlib.Path, default=None, help="one location per line")
    ap.add_argument("--country", default="us")
    ap.add_argument("--max", type=int, default=40)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="grid.csv")
    args = ap.parse_args()

    cities = (
        [ln.strip() for ln in args.cities.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if args.cities else DEFAULT_CITIES
    )

    def sweep(city: str):
        try:
            return city, collect("google_maps_places", query=args.query, location=city,
                                 country=args.country, max_results=args.max)
        except CollectorError as exc:
            print(f"  !! {city}: {exc}")
            return city, []

    unique: dict[str, dict] = {}
    seen_in = Counter()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for city, rows in pool.map(sweep, cities):
            fresh = 0
            for row in rows:
                key = row.get("place_id") or row.get("data_id") or row.get("maps_url")
                if not key:
                    continue
                seen_in[key] += 1
                if key not in unique:
                    unique[key] = {**row, "first_seen_in": city}
                    fresh += 1
            print(f"{city:<45} {len(rows):>3} rows, {fresh:>3} new")

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["name", "rating", "reviews", "category", "address",
                                           "phone", "website", "latitude", "longitude",
                                           "place_id", "first_seen_in"], extrasaction="ignore")
        w.writeheader()
        w.writerows(unique.values())

    duplicates = sum(1 for c in seen_in.values() if c > 1)
    print(f"\n{len(unique)} unique places from {sum(seen_in.values())} rows "
          f"({duplicates} appeared in more than one city) → {args.out}")


if __name__ == "__main__":
    main()
