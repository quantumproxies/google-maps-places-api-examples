# Google Maps places API — local pack, coordinates and contact details as rows

The [`google_maps_places` collector](https://quanticdata.io/collectors/google-maps-scraper-api/)
takes a query and a place ("coffee roasters", "Milan, Italy") and returns typed rows:
name, rating, review count, category, price level, address, phone, website, opening hours,
`latitude`/`longitude`, `place_id`, `data_id` and the Maps URL.

No Selenium, no map-tile scrolling, no place-id spelunking. **$0.001 per delivered place**,
up to 100 per run.

```bash
pip install requests
export QUANTICDATA_API_KEY=qd_live_your_key_here
python3 places.py "coffee roasters" "Milan, Italy" --max 60 --out places.csv
```

## Files

| File | What it does |
|---|---|
| [`places.py`](places.py) | one query, one city → CSV with every field the collector returns |
| [`grid_search.py`](grid_search.py) | sweep a list of cities and de-duplicate by `place_id` — real coverage, not one lucky local pack |
| [`geo_export.py`](geo_export.py) | GeoJSON out, ready to drop on a map or into PostGIS |
| [`no_website.py`](no_website.py) | the classic agency query: rated businesses with **no website** |

## Input

| Field | Notes |
|---|---|
| `query` | what to look for — "dentist", "coffee roasters", "hardware store" |
| `location` | human-readable, e.g. `"Austin, Texas"`; drives the map viewport |
| `country` | ISO code — proxy exit and Google locale |
| `lang` | interface language |
| `max_results` | 1–100, default 20. You pay only for delivered rows. |

## Output row

```jsonc
{ "rank": 1, "name": "Orsonero Coffee", "rating": 4.6, "reviews": 812,
  "category": "Coffee shop", "price_level": "$$",
  "address": "Via Giuseppe Broggi, 15, 20129 Milano MI, Italy",
  "phone": "+39 02 3653 4054", "website": "https://orsonerocoffee.com/",
  "hours": "Tue-Sun 8:00-17:00", "service_options": "Dine-in · Takeaway",
  "latitude": 45.4785, "longitude": 9.2065,
  "place_id": "ChIJ…", "data_id": "0x4786c…:0x…",
  "maps_url": "https://www.google.com/maps/place/…", "found_by": "local_pack" }
```

`data_id` is the handle you pass to [`place_reviews`](https://quanticdata.io/collectors/google-reviews-scraper-api/)
to pull that place's reviews — see
[google-reviews-api-examples](https://github.com/quantumproxies/google-reviews-api-examples).

## Coverage, honestly

One query in one city returns what Google shows for that viewport — typically 20–60 places, not
"every business in the city". Real coverage comes from sweeping a **grid of locations** and
de-duplicating on `place_id`, which is what `grid_search.py` does. Expect 30–50% overlap between
neighbouring cities.

Need emails too? [`local_business_leads`](https://quanticdata.io/collectors/lead-scraper-api/)
does places + contact enrichment in one call.

## Related

- [Google Maps scraper API](https://quanticdata.io/collectors/google-maps-scraper-api/) · [Lead scraper API](https://quanticdata.io/collectors/lead-scraper-api/)
- [All 31 collectors](https://quanticdata.io/collectors/) · [Documentation](https://quanticdata.io/docs/)
- [Is lead generation legal?](https://quanticdata.io/blog/is-lead-generation-legal/)

MIT licensed.
