"""Rated businesses with no website — the oldest local-agency prospect list there is.

Sorted by review count, because a place with 400 reviews and no site is a much
warmer conversation than one with three.

    python3 no_website.py "hair salon" "Phoenix, Arizona" --min-reviews 25
"""
from __future__ import annotations

import argparse
import csv

from client import collect


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("location")
    ap.add_argument("--country", default="us")
    ap.add_argument("--max", type=int, default=100)
    ap.add_argument("--min-reviews", type=int, default=10)
    ap.add_argument("--out", default="no-website.csv")
    args = ap.parse_args()

    rows = collect("google_maps_places", query=args.query, location=args.location,
                   country=args.country, max_results=args.max)

    prospects = [
        r for r in rows
        if not r.get("website") and (r.get("reviews") or 0) >= args.min_reviews
    ]
    prospects.sort(key=lambda r: -(r.get("reviews") or 0))

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["name", "category", "rating", "reviews",
                                           "phone", "address", "maps_url"],
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(prospects)

    print(f"{len(prospects)} of {len(rows)} places have no website "
          f"and at least {args.min_reviews} reviews → {args.out}\n")
    for row in prospects[:15]:
        print(f"  {row.get('reviews'):>4} reviews  {row.get('rating')}★  "
              f"{row.get('name')}  {row.get('phone') or ''}")


if __name__ == "__main__":
    main()
