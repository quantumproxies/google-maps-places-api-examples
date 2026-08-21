"""Places → GeoJSON, ready for Leaflet, QGIS, Mapbox or PostGIS.

    python3 geo_export.py "bike shop" "Amsterdam, Netherlands" --out shops.geojson
"""
from __future__ import annotations

import argparse
import json

from client import collect


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("location")
    ap.add_argument("--country", default="nl")
    ap.add_argument("--max", type=int, default=60)
    ap.add_argument("--out", default="places.geojson")
    args = ap.parse_args()

    rows = collect("google_maps_places", query=args.query, location=args.location,
                   country=args.country, max_results=args.max)

    features = []
    skipped = 0
    for row in rows:
        lat, lon = row.get("latitude"), row.get("longitude")
        if lat is None or lon is None:
            skipped += 1
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {k: row.get(k) for k in
                           ("name", "rating", "reviews", "category", "price_level",
                            "address", "phone", "website", "place_id", "maps_url")},
        })

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": features}, fh,
                  ensure_ascii=False, indent=1)

    print(f"{len(features)} points → {args.out}"
          + (f" ({skipped} rows had no coordinates)" if skipped else ""))


if __name__ == "__main__":
    main()
