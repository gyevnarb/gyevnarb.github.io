# Job Market Hub

A small local web app for the 2026–27 academic and industry research job market, focused on the UK and Europe.

## Use

The app is published as an unlisted page at <https://gbalint.me/jobs/>: it isn't linked from the nav, is marked `noindex`, and is left out of the sitemap. `index.html` is a Jekyll page that uses the site layout, and `app.css` takes its colours and fonts from the site (`_includes/site.scss`), scoped to `.jobhub`.

The deploy workflow (`.github/workflows/deploy.yml`) runs `refresh.py` on every push and once a day, so the live listings stay current. The previous `data/jobs.json` is kept in the Actions cache so each listing's first-seen date carries over. `data/jobs.json` and `data/bundle.js` are generated and not committed. The build leaves out `refresh.py`, this README and the `data/*.json` files; only `app.css`, `app.js` and `data/bundle.js` are published.

To preview locally:

```sh
python3 job_tracker/refresh.py        # fetch live listings (~30 s), then rebuild data/bundle.js
bundle exec jekyll serve              # then open http://127.0.0.1:4000/jobs/
```

Listings that appeared since your last visit get a **new** badge.

## Tabs

| Tab | What it does |
|---|---|
| Positions | Live listings. Filter by region, role type and source, and set a minimum relevance score. Use ★ to track a listing, ⊘ to mark an ad as no longer available, and ✕ to hide it. |
| Tracker | Kanban-style columns for each application stage, from *Interested* to *Closed*, with deadlines and notes. You can add applications by hand, export deadlines to your calendar as `.ics`, and back up or restore as JSON. |
| Deadlines | Month-by-month timeline of tracked applications, fellowship calls and (optionally) relevant open positions. |
| Fellowships | Curated early-career schemes (ERC, MSCA, UKRI FLF, Leverhulme, SNSF, NWO…) with a fit rating. Dates not confirmed on an official call page are flagged *date unconfirmed*. |
| Watchlist | Target departments, institutes, labs and policy bodies, each with a link to its careers page. Tracks when you last checked each one; filter for anything not checked in 14+ days. |
| Country guides | Career ladder, tenure, hiring cycle, interview format, salaries, visa notes and job boards for each country. |
| Checklist | Application-materials checklist that saves your progress, filterable by region (UK, DE, NL, CH, Nordic, FR, industry). |
| Resources | Job boards, advice guides, salary data, visa information and mailing lists. |

Your tracker, checklist ticks, hidden and unavailable listings, and last-visit date live in your browser's `localStorage`. They are **not** in these files, so use *Tracker → Back up* now and then.

## Live sources (`refresh.py`)

| Source | Method |
|---|---|
| jobs.ac.uk | search result pages |
| THE Unijobs, Nature Careers, Science Careers | Madgex RSS (`/jobsrss/`) |
| TenureTracker (includes EURAXESS postings) | search result pages |
| Community academic jobs Google Sheet | CSV export; add more sheets in `SHEETS` |
| AcademicTransfer (NL) | search result pages |
| 80,000 Hours board (AI safety & policy) | public Algolia index |
| Anthropic, UK AISI, Isomorphic, xAI, Wayve, Helsing, Scale | Greenhouse API |
| OpenAI, Cohere, Perplexity, Black Forest Labs, Synthesia | Ashby API |
| Spotify · Hugging Face | Lever · Workable API |
| Microsoft (incl. MSR Cambridge) | careers search API |

These sources can't be fetched this way, so they're covered by links in the Watchlist or Resources tab instead: EURAXESS directly (it's partly covered through TenureTracker), AcademicPositions (behind Cloudflare), Google DeepMind (moved off Greenhouse), Meta, Apple, ELLIS and university HR portals.

To tune coverage, edit these constants at the top of `refresh.py`:
- `QUERIES` for the keyword searches.
- `BOARDS` for company job boards. Add any Greenhouse, Ashby, Lever or Workable slug.
- `KEYWORDS` / `ROLE_BONUS` for relevance weights.
- `EXCLUDE` for title patterns to drop.

## Curated data (`data/*.json`)

Researched in September 2026. Check dates and salaries against the official pages before relying on them.

- `fellowships.json`: grants and fellowships
- `guides.json`: country hiring systems
- `checklist.json`: application materials
- `watchlist.json`: target organisations
- `resources.json`: links

After editing any of these files, push to redeploy, or run `python3 job_tracker/refresh.py --bundle` to rebuild locally without fetching.
