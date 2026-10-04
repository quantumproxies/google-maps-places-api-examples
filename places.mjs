// Google Maps scraper API: one typed row per place.
//
//   export QUANTICDATA_API_KEY=...        # https://app.quanticdata.io/register
//   node places.mjs "dentist" "Austin, TX" 20
//
// Node 18+, no dependencies.
// Docs and schema: https://quanticdata.io/collectors/google-maps-scraper-api/

const BASE = "https://api.quanticdata.io/v1";
const KEY = process.env.QUANTICDATA_API_KEY;
if (!KEY) {
  console.error("Set QUANTICDATA_API_KEY first: https://app.quanticdata.io/register");
  process.exit(1);
}
const headers = { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" };

const [query = "dentist", location = "Austin, TX", max = "20"] = process.argv.slice(2);
const input = { query, location, max_results: Number(max) };

const res = await fetch(`${BASE}/scraper/collectors/google_maps_places/run`, {
  method: "POST",
  headers,
  body: JSON.stringify(input),
});
const body = await res.json();
if (!res.ok || body.type === "error") {
  console.error(`Request failed (${res.status}): ${body.message}`);
  process.exit(1);
}
let run = body.payload;

// Long runs answer 202 and finish in the background: poll the run until it is done.
while (run.status === "queued" || run.status === "running") {
  await new Promise((r) => setTimeout(r, 3000));
  const s = await fetch(`${BASE}/scraper/collectors/runs/${run.run_id}`, { headers });
  run = (await s.json()).payload;
}

const rows = run.results ?? [];
console.table(rows.map((p) => ({
  rank: p.rank,
  name: p.name,
  rating: p.rating,
  reviews: p.reviews,
  phone: p.phone,
  website: p.website,
})));
console.log(`${rows.length} place rows`);
