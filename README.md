# Google Maps places API — local pack, coordinates and contact details as rows

The [`google_maps_places` collector](https://quanticdata.io/collectors/google-maps-scraper-api/)
takes a query and a place ("coffee roasters", "Milan, Italy") and returns typed rows:
name, rating, review count, category, address, phone, website, opening hours (as text and per day),
`latitude`/`longitude`, `place_id`, `data_id` and the Maps URL.

No Selenium, no map-tile scrolling, no place-id spelunking. **$0.001 per delivered place**,
up to 300 per run.

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
| `max_results` | 1–300, default 20. You pay only for delivered rows. |
| `enrich_details` | Default `true`: fills weekly hours and review count per place. Same price. |

## Output row

```jsonc
{ "rank": 1, "name": "Blunn Creek Family Dentistry", "rating": 4.9, "reviews": 179,
  "category": "Dentist",
  "address": "2550 South Interstate 35 Frontage Road #210, Austin, TX 78704-5724",
  "phone": "(512) 442-6728", "website": "https://blunncreekdental.com/",
  "hours": "Sunday: Closed; Monday: 8 am–5 pm; Tuesday: 8 am–5 pm; …",
  "weekly_hours": { "Monday": "8 am–5 pm", "Tuesday": "8 am–5 pm", /* one entry per day */ },
  "open_state": "Closed · Opens 8 AM Mon",
  "thumbnail": "https://lh3.googleusercontent.com/…",
  "latitude": 30.230971, "longitude": -97.743781,
  "place_id": "0x8644b4f1bb0ae061:0x9f022dcd45880329",
  "data_id": "0x8644b4f1bb0ae061:0x9f022dcd45880329",
  "maps_url": "https://www.google.com/maps/search/?api=1&query=…",
  "found_by": "dentist Austin, TX" }
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

## Node.js

The same call without Python: Node 18 or newer, no dependencies. See [`places.mjs`](places.mjs):

```bash
export QUANTICDATA_API_KEY=qd_live_your_key_here
node places.mjs "dentist" "Austin, TX" 20
```

## Sample response

A real run from 4 October 2026 (collector 1.1.0): `dentist` in `Austin, TX`, 40 rows delivered. These are public business listings. The rows arrive in `payload.results`; the first one is shown here with its main fields, and the first three rows as returned are in [`sample-response.json`](sample-response.json).

```json
{
  "rank": 1,
  "name": "Blunn Creek Family Dentistry",
  "rating": 4.9,
  "reviews": 179,
  "category": "Dentist",
  "address": "2550 South Interstate 35 Frontage Road #210, Austin, TX 78704-5724",
  "phone": "(512) 442-6728",
  "website": "https://blunncreekdental.com/",
  "hours": "Sunday: Closed; Monday: 8 am–5 pm; Tuesday: 8 am–5 pm; Wednesday: 8 am–5 pm; Thursday: 8 am–5 pm; Friday: Closed; Saturday: Closed",
  "weekly_hours": {
    "Monday": "8 am–5 pm",
    "Tuesday": "8 am–5 pm",
    "Wednesday": "8 am–5 pm",
    "Thursday": "8 am–5 pm",
    "Friday": "Closed",
    "Saturday": "Closed",
    "Sunday": "Closed"
  },
  "open_state": "Closed · Opens 8 AM Mon",
  "thumbnail": "https://lh3.googleusercontent.com/gps-cs-s/ANWiy9RZAw2d3hyeJc6fgfmm2NimXQwu1KILunDvfsvCNkO8FFGSZWesggEXTqTFAHh-FQU4xczfYturYN0lpnREt_6qCm0_GKLwBH3Goh9zmjyjV1NoOjoTP8OPZs37NUlMgZBcr1JFCA=k-no-",
  "maps_url": "https://www.google.com/maps/search/?api=1&query=Blunn%20Creek%20Family%20Dentistry%202550%20South%20Interstate%2035%20Frontage%20Road%20%23210%2C%20Austin%2C%20TX%2078704-5724",
  "latitude": 30.230971,
  "longitude": -97.743781,
  "place_id": "0x8644b4f1bb0ae061:0x9f022dcd45880329",
  "data_id": "0x8644b4f1bb0ae061:0x9f022dcd45880329",
  "found_by": "dentist Austin, TX"
}
```

MIT licensed.
