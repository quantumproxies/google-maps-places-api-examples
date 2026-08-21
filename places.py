"""One query, one place, one CSV.

    python3 places.py "coffee roasters" "Milan, Italy" --max 60 --out places.csv
"""
from __future__ import annotations

import argparse
import csv

from client import collect

FIELDS = ["rank", "name", "rating", "reviews", "category", "price_level", "address",
          "phone", "website", "hours", "service_options", "latitude", "longitude",
          "place_id", "data_id", "maps_url", "found_by"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("location")
    ap.add_argument("--country", default="us")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--max", type=int, default=20)
    ap.add_argument("--out", default="places.csv")
    args = ap.parse_args()

    rows = collect("google_maps_places", query=args.query, location=args.location,
                   country=args.country, lang=args.lang, max_results=args.max)

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    rated = [r for r in rows if r.get("rating")]
    avg = sum(r["rating"] for r in rated) / len(rated) if rated else 0
    with_site = sum(1 for r in rows if r.get("website"))
    print(f"{len(rows)} places → {args.out}")
    print(f"average rating {avg:.2f} over {len(rated)} rated, {with_site} with a website")
    for row in rows[:10]:
        print(f"  {row.get('rating') or '-':>3} ({row.get('reviews') or 0:>4})  "
              f"{row.get('name')}  ·  {row.get('category')}")


if __name__ == "__main__":
    main()
