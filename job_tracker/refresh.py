#!/usr/bin/env python3
"""Fetch live job listings and bundle them with the curated data for the app.

Usage:  python3 refresh.py            # fetch everything, write data/jobs.json + data/bundle.js
        python3 refresh.py --bundle   # only rebuild data/bundle.js from existing JSON (no network)

Standard library only. Edit QUERIES / BOARDS / KEYWORDS below to tune coverage.
"""
import concurrent.futures as cf
import csv
import io
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
TODAY = datetime.now(timezone.utc).date().isoformat()

# ---------------------------------------------------------------- configuration

# Keyword searches run against academic job boards.
QUERIES = [
    "artificial intelligence", "machine learning", "AI safety", "explainable AI",
    "responsible AI", "trustworthy AI", "philosophy of science", "metascience",
    "cognitive science", "multi-agent", "human-centred AI", "computer science lecturer",
    "assistant professor computer science", "AI ethics", "science of science",
]

# Community-maintained Google Sheets of openings (must be link-viewable). Columns expected:
# Date added, Position/Resource, Title, Field/Topic, University/Organization, Region, Deadline, Link
SHEETS = {"Community sheet": "1LJ93NUxRIxKMhdZ02Fy_LkpwPS3GQy7j6EmIjaHES1s"}

# Company job boards (public ATS APIs). Only research-flavoured titles are kept.
BOARDS = {
    "greenhouse": {"anthropic": "Anthropic", "aisi": "UK AI Security Institute",
                   "isomorphiclabs": "Isomorphic Labs", "xai": "xAI", "wayve": "Wayve",
                   "helsing": "Helsing", "scaleai": "Scale AI"},
    "ashby": {"openai": "OpenAI", "cohere": "Cohere", "perplexity": "Perplexity",
              "black-forest-labs": "Black Forest Labs", "synthesia": "Synthesia"},
    "lever": {"spotify": "Spotify"},
    "workable": {"huggingface": "Hugging Face"},
}

# Relevance weights (regex -> points) matched against title + summary.
KEYWORDS = {
    r"meta-?science|meta-?research|science of science|research integrity|scientific integrity": 5,
    r"explainab|interpretab|\bxai\b|counterfactual": 4,
    r"ai safety|alignment|trustworth|responsible ai|ai governance|ai polic|sociotechnical|socio-technical": 4,
    r"epistem|science and technology studies|\bsts\b": 3,
    r"philosoph": 1,
    r"cognitive|human-cent|human-computer|\bhci\b|multi-?agent|autonomous (systems|vehicles|driving)": 3,
    r"ethic|fairness|society|social|complex (systems|social)|computational social": 2,
    r"artificial intelligence|machine learning|\bai\b|\bml\b|reinforcement|language model|llm": 1,
    r"computer science|informatics|computing": 1,
}
ROLE_BONUS = {
    r"assistant professor|lecturer|tenure|junior professor|juniorprofessor|w1|w2|group leader|research fellow|fellowship|associate professor": 3,
    r"research scientist|researcher|member of technical staff|research lead": 2,
}
# Titles we never want (students, admin, pure engineering/business roles).
EXCLUDE = re.compile(
    r"\bphd\b|studentship|\bstudents?\b|doctoral candidate|doctoral researcher|phd candidate|interns?\b|internship|\bmsc\b|\bbsc\b|"
    r"technician|administrat|coordinator|recruit|sales|account (executive|manager)|marketing|"
    r"finance|legal counsel|paralegal|office manager|executive assistant|teaching assistant|"
    r"clinical|nurse|lecturer in (nursing|midwifery|law|accounting)|chef|cleaner|porter",
    re.I)
ORGISH = re.compile(r"universit|institut|college|school|centre|center|academy|laborator|\(|ETH|EPFL|KTH|foundation|hospital", re.I)
NON_EUROPE = re.compile(
    r"cambridge,? (ma|massachusetts)|massachusetts|london,? (on|ontario)|ontario|new york|san francisco|"
    r"\b(usa|us|united states|canada|ca|ma|ny|tx|wa)\b(?!-)|california|australia|new zealand|hong kong|china|"
    r"singapore|japan|korea|india|united arab emirates|qatar|saudi|suzhou|shanghai|beijing|shenzhen|hangzhou|ningbo|"
    r"guangzhou|jiangsu|zhejiang|\(cn\)|macau|taiwan|dubai|abu dhabi|doha|malaysia|kuala lumpur|vietnam|morocco|"
    r"kazakhstan|uzbekistan|egypt|nigeria|kenya|south africa|brazil|mexico|chile|israel|asia|middle east|africa|australia/new zealand", re.I)
INDUSTRY_KEEP = re.compile(r"research|scientist|fellow|alignment|safety|interpretab", re.I)

UK = re.compile(r"\b(uk|united kingdom|england|scotland|wales|northern ireland|london|cambridge|oxford|edinburgh|"
                r"glasgow|manchester|bristol|birmingham|leeds|sheffield|york|warwick|coventry|bath|durham|"
                r"nottingham|southampton|liverpool|newcastle|belfast|cardiff|st andrews|aberdeen|dundee|exeter|"
                r"lancaster|leicester|sussex|brighton|surrey|guildford|reading|kent|canterbury|norwich|"
                r"loughborough|swansea|stirling|heriot|strathclyde|hull|plymouth|essex|colchester|milton keynes)\b", re.I)
EUROPE = re.compile(r"\b(europe|eu|remote - emea|emea|germany|deutschland|berlin|munich|münchen|hamburg|frankfurt|"
                    r"heidelberg|tübingen|tubingen|stuttgart|saarbrücken|darmstadt|bonn|cologne|köln|dresden|aachen|"
                    r"karlsruhe|freiburg|göttingen|leipzig|netherlands|amsterdam|delft|utrecht|leiden|eindhoven|"
                    r"nijmegen|groningen|tilburg|rotterdam|maastricht|twente|enschede|wageningen|switzerland|zurich|"
                    r"zürich|lausanne|geneva|basel|bern|lugano|france|paris|grenoble|lyon|toulouse|nancy|lille|"
                    r"sophia|belgium|brussels|leuven|ghent|antwerp|luxembourg|austria|vienna|wien|graz|linz|"
                    r"klosterneuburg|denmark|copenhagen|aarhus|lyngby|sweden|stockholm|gothenburg|göteborg|lund|"
                    r"uppsala|linköping|umeå|norway|oslo|bergen|trondheim|finland|helsinki|espoo|tampere|oulu|"
                    r"turku|ireland|dublin|cork|galway|spain|madrid|barcelona|valencia|bilbao|italy|milan|milano|"
                    r"rome|roma|turin|torino|bologna|pisa|trento|padua|genoa|portugal|lisbon|porto|poland|warsaw|"
                    r"krakow|kraków|wrocław|czech|prague|brno|hungary|budapest|greece|athens|estonia|tallinn|"
                    r"latvia|riga|lithuania|vilnius|slovenia|ljubljana|croatia|zagreb|romania|bucharest|cyprus|"
                    r"malta|iceland|reykjavik|slovakia|bratislava|bulgaria|sofia|serbia|belgrade)\b", re.I)


# ---------------------------------------------------------------- helpers

def fetch(url, data=None, headers=None, timeout=40):
    h = {"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))


def fetch_json(url, **kw):
    return json.loads(fetch(url, **kw))


def text(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def region_of(location):
    loc = location or ""
    # Namesakes abroad (Cambridge MA, London ON, Paris TX…) must not count as Europe.
    loc_eu = NON_EUROPE.sub(" ", loc)
    if NON_EUROPE.search(loc) and not (UK.search(loc_eu) or EUROPE.search(loc_eu)):
        return "Other"
    loc = loc_eu
    if UK.search(loc):
        return "UK"
    if EUROPE.search(loc):
        return "Europe"
    if re.search(r"remote", loc, re.I) and not re.search(r"us|usa|united states|canada|america", loc, re.I):
        return "Remote"
    return "Other"


def parse_date(s, fmts):
    if not s:
        return None
    s = s.strip()
    for f in fmts:
        try:
            if "%Y" not in f:  # e.g. "20 Oct" -> choose the next occurrence
                now = datetime.now()
                d = datetime.strptime(f"{s} {now.year}", f + " %Y")
                if (now - d).days > 60:
                    d = d.replace(year=now.year + 1)
            else:
                d = datetime.strptime(s, f)
            return d.date().isoformat()
        except ValueError:
            continue
    return None


def ts_date(ts):
    try:
        return datetime.fromtimestamp(float(ts), timezone.utc).date().isoformat()
    except (TypeError, ValueError):
        return None


def job(source, title, org, location, url, kind, posted=None, deadline=None, summary="", salary="", tags=None):
    return {"source": source, "title": text(title), "org": text(org), "location": text(location),
            "url": url, "kind": kind, "posted": posted, "deadline": deadline,
            "summary": text(summary)[:400], "salary": text(salary)[:120], "tags": tags or []}


def classify_kind(title, default):
    t = title.lower()
    if re.search(r"professor|lecturer|reader|faculty|tenure|juniorprof|chair in|w1|w2|w3", t):
        return "Faculty"
    if re.search(r"fellowship|fellow\b", t):
        return "Fellowship"
    if re.search(r"postdoc|post-doc|postdoctoral|research associate|research assistant", t):
        return "Postdoc"
    if re.search(r"group leader|principal investigator|research leader|head of", t):
        return "Group leader"
    return default


# ---------------------------------------------------------------- sources

def src_jobs_ac_uk():
    out = []
    for q in QUERIES:
        for start in (1, 26):
            u = "https://www.jobs.ac.uk/search/?" + urllib.parse.urlencode(
                {"keywords": q, "sortOrder": 1, "pageSize": 25, "startIndex": start})
            h = fetch(u)
            blocks = h.split('class="j-search-result__result')[1:]
            for b in blocks:
                m = re.search(r'<a href="(/job/[^"]+)">\s*(.*?)\s*</a>', b, re.S)
                if not m:
                    continue
                g = lambda cls: (re.search(r'class="j-search-result__%s">(.*?)</div>' % cls, b, re.S) or [None, ""])[1]
                loc = (re.search(r"Location:\s*(.*?)</div>", b, re.S) or [None, ""])[1]
                sal = (re.search(r"Salary: </strong>(.*?)</div>", b, re.S) or [None, ""])[1]
                placed = (re.search(r"Date Placed: </strong>([^<]+)", b) or [None, ""])[1]
                closes = (re.search(r'date--blue[^"]*">\s*([^<]+)', b) or [None, ""])[1]
                title = m.group(2)
                out.append(job("jobs.ac.uk", title, text(g("employer")), text(loc) or "UK",
                               "https://www.jobs.ac.uk" + m.group(1), classify_kind(title, "Academic"),
                               posted=parse_date(text(placed), ["%d %b %Y", "%d %b"]),
                               deadline=parse_date(text(closes), ["%d %b %Y", "%d %b"]),
                               summary=text(g("department")), salary=sal))
            if len(blocks) < 25:
                break
    return out


def madgex_rss(base, source, pages=3):
    out = []
    for q in QUERIES:
        for page in range(1, pages + 1):
            u = f"{base}/jobsrss/?" + urllib.parse.urlencode({"keywords": q, "page": page})
            root = ET.fromstring(fetch(u).encode())
            items = root.findall(".//item")
            for it in items:
                title = it.findtext("title") or ""
                org = ""
                head = title.split(": ", 1)[0]
                if ": " in title and len(head) < 100 and (head.isupper() or ORGISH.search(head)):
                    org, title = title.split(": ", 1)
                desc = it.findtext("description") or ""
                dtext = text(desc)
                # Madgex descriptions end with the location line after the recruiter name.
                loc = ""
                lines = [l.strip() for l in re.split(r"<br\s*/?>|\n", html.unescape(desc)) if text(l)]
                if lines:
                    loc = text(lines[-1])
                posted = None
                try:
                    posted = datetime.strptime(it.findtext("pubDate")[:25].strip(), "%a, %d %b %Y %H:%M:%S").date().isoformat()
                except Exception:
                    pass
                link = re.sub(r"[?&](TrackID|utm_[a-z]+)=[^&]*", "", it.findtext("link") or "").rstrip("?&")
                out.append(job(source, title.strip(), org.title() if org.isupper() else org, loc, link,
                               classify_kind(title, "Academic"), posted=posted, summary=dtext))
            if len(items) < 20:
                break
    return out


def src_the():
    return madgex_rss("https://www.timeshighereducation.com/unijobs", "THE Unijobs")


def src_nature():
    return madgex_rss("https://www.nature.com/naturecareers", "Nature Careers")


def src_science():
    return madgex_rss("https://jobs.sciencecareers.org", "Science Careers", pages=2)


def src_tenuretracker():
    out = []
    for q in QUERIES:
        for page in range(3):
            h = fetch("https://tenuretracker.info/?" + urllib.parse.urlencode({"q": q, "page": page}))
            items = re.split(r'<li class="position-item', h)[1:]
            for it in items:
                it = it.split("</li>")[0]
                t = re.search(r'href="(https://tenuretracker\.info/l/[^"]+)"[^>]*>\s*(.*?)\s*</a>', it, re.S)
                if not t:
                    continue
                orig = re.findall(r'href="(https?://(?!tenuretracker)[^"]+)"', it)
                inst = re.search(r'data-institute="([^"]*)"', it)
                pills = [text(p) for p in re.findall(r'tt-pill-plain tt-pill-truncate">(.*?)</span>', it, re.S)]
                dl = re.search(r"Deadline:&nbsp;</span>\s*([^<]+)", it)
                posted = re.search(r"Posted on:&nbsp;</span>\s*([^<]+)", it)
                title = t.group(2)
                out.append(job("TenureTracker", title, html.unescape(inst.group(1)) if inst else "",
                               ", ".join(pills), orig[0] if orig else t.group(1), classify_kind(title, "Academic"),
                               posted=parse_date(text(posted.group(1)) if posted else "", ["%d %B %Y"]),
                               deadline=parse_date(text(dl.group(1)) if dl else "", ["%d %B %Y"])))
            if len(items) < 50:
                break
    return out


def src_sheets():
    out = []
    kinds = {"Professor/Lecturer": "Faculty", "Postdoc": "Postdoc", "Fellowship": "Fellowship",
             "Industry": "Industry", "Research Scholar": "Postdoc"}
    grace = datetime.now().date().toordinal() - 45
    for label, sid in SHEETS.items():
        rows = csv.reader(io.StringIO(fetch(f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=0")))
        for r in rows:
            if len(r) < 8 or not r[7].startswith("http"):
                continue
            added, kind, title, field, org, region, deadline, link = [x.strip() for x in r[:8]]
            dl = parse_date(deadline, ["%m/%d/%Y"])
            note = f"Field: {field}." if field else ""
            if dl and dl < TODAY:
                # The sheet notes that many dates are review start dates, so keep recently passed ones.
                if datetime.fromisoformat(dl).toordinal() < grace:
                    continue
                note += f" Listed deadline {fmt_d(dl)}: review may be ongoing."
                dl = None
            j = job(label, title, org, region if region not in ("Europe", "Any/All") else "", link,
                    kinds.get(kind) or classify_kind(title, "Other"), posted=parse_date(added, ["%m/%d/%Y"]),
                    deadline=dl, summary=note)
            j["sheet_region"] = region
            out.append(j)
    return out


def fmt_d(iso):
    return datetime.fromisoformat(iso).strftime("%-d %b %Y")


def src_academictransfer():
    out = []
    for q in QUERIES[:10]:
        u = "https://www.academictransfer.com/en/jobs/?" + urllib.parse.urlencode({"q": q})
        h = fetch(u)
        for art in h.split("<article")[1:]:
            m = re.search(r'href="(/en/jobs/\d+/[^"]+)"', art)
            t = re.search(r"<h3[^>]*>(.*?)</h3>", art, re.S)
            if not (m and t):
                continue
            dl = re.search(r'Deadline <time datetime="(\d{4}-\d\d-\d\d)', art)
            pub = re.search(r'Published <time datetime="(\d{4}-\d\d-\d\d)', art)
            city = re.findall(r"</svg>\s*([^<]{2,60})</span>", art)
            org = re.search(r'alt="([^"]+)" class="w-full', art)
            summ = re.search(r"<p[^>]*>(.*?)</p>", art, re.S)
            title = t.group(1)
            out.append(job("AcademicTransfer", title, org.group(1) if org else "",
                           (city[-1].strip() + ", Netherlands") if city else "Netherlands",
                           "https://www.academictransfer.com" + m.group(1), classify_kind(title, "Academic"),
                           posted=pub and pub.group(1), deadline=dl and dl.group(1),
                           summary=summ.group(1) if summ else ""))
    return out


def src_80k():
    out = []
    url = "https://W6KM1UDIB3-dsn.algolia.net/1/indexes/jobs_prod/query"
    hdr = {"X-Algolia-API-Key": "d1d7f2c8696e7b36837d5ed337c4a319", "X-Algolia-Application-Id": "W6KM1UDIB3",
           "Content-Type": "application/json", "Referer": "https://jobs.80000hours.org/"}
    for page in range(5):
        body = json.dumps({"query": "", "hitsPerPage": 200, "page": page,
                           "facetFilters": [["tags_area:AI safety & policy"]]}).encode()
        d = json.loads(fetch(url, data=body, headers=hdr))
        for h in d.get("hits", []):
            title = h.get("title", "")
            roles = " ".join(h.get("tags_role_type") or [])
            if not re.search(r"research|fellow", roles + " " + title, re.I):
                continue
            locs = ", ".join(h.get("card_locations") or h.get("tags_country") or [])
            out.append(job("80,000 Hours", title, h.get("company_name", ""), locs, h.get("url_external", ""),
                           "AI safety & policy" if "Fellow" not in title else "Fellowship",
                           posted=ts_date(h.get("posted_at")), deadline=ts_date(h.get("closes_at")),
                           summary=h.get("description_short", ""), salary=h.get("salary") or "",
                           tags=h.get("tags_skill") or []))
        if page + 1 >= d.get("nbPages", 0):
            break
    return out


def src_greenhouse():
    out = []
    for board, name in BOARDS["greenhouse"].items():
        try:
            d = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs")
        except Exception:
            continue
        for j in d.get("jobs", []):
            if INDUSTRY_KEEP.search(j["title"]):
                out.append(job(name, j["title"], name, (j.get("location") or {}).get("name", ""),
                               j["absolute_url"], "Industry" if board != "aisi" else "AI safety & policy",
                               posted=(j.get("first_published") or j.get("updated_at") or "")[:10] or None))
    return out


def src_ashby():
    out = []
    for board, name in BOARDS["ashby"].items():
        try:
            d = fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{board}", timeout=90)
        except Exception:
            continue
        for j in d.get("jobs", []):
            if not INDUSTRY_KEEP.search(j.get("title", "")):
                continue
            locs = [j.get("location") or ""] + [s.get("location", "") for s in j.get("secondaryLocations") or []]
            out.append(job(name, j["title"], name, " / ".join(l for l in locs if l), j.get("jobUrl", ""),
                           "Industry", posted=(j.get("publishedAt") or "")[:10] or None,
                           summary=j.get("descriptionPlain", "")[:400]))
    return out


def src_lever():
    out = []
    for board, name in BOARDS["lever"].items():
        for j in fetch_json(f"https://api.lever.co/v0/postings/{board}?mode=json"):
            if INDUSTRY_KEEP.search(j.get("text", "")):
                cat = j.get("categories") or {}
                out.append(job(name, j["text"], name, cat.get("location", ""), j.get("hostedUrl", ""),
                               "Industry", posted=ts_date((j.get("createdAt") or 0) / 1000),
                               summary=j.get("descriptionPlain", "")[:400]))
    return out


def src_workable():
    out = []
    for board, name in BOARDS["workable"].items():
        d = fetch_json(f"https://apply.workable.com/api/v1/widget/accounts/{board}")
        for j in d.get("jobs", []):
            if INDUSTRY_KEEP.search(j.get("title", "")):
                loc = ", ".join(x for x in [j.get("city"), j.get("country")] if x)
                if j.get("telecommuting"):
                    loc = (loc + " / Remote").strip(" /")
                out.append(job(name, j["title"], name, loc, j.get("url", ""), "Industry",
                               posted=(j.get("published_on") or "")[:10] or None))
    return out


def src_microsoft():
    out = []
    for loc in ["United Kingdom", "Switzerland", "Netherlands", "Germany", "France", "Ireland", "Denmark", "Spain"]:
        for q in ["researcher", "research scientist"]:
            u = "https://apply.careers.microsoft.com/api/pcsx/search?" + urllib.parse.urlencode(
                {"domain": "microsoft.com", "query": q, "location": loc, "start": 0})
            d = fetch_json(u).get("data", {})
            for p in d.get("positions", []):
                if INDUSTRY_KEEP.search(p["name"]):
                    out.append(job("Microsoft", p["name"], "Microsoft" + (" Research" if "Research" in (p.get("department") or "") else ""),
                                   "; ".join(p.get("locations") or []),
                                   "https://apply.careers.microsoft.com" + p.get("positionUrl", ""),
                                   "Industry", posted=ts_date(p.get("postedTs")), summary=p.get("department", "")))
    return out


SOURCES = {
    "jobs.ac.uk": src_jobs_ac_uk, "THE Unijobs": src_the, "Nature Careers": src_nature,
    "AcademicTransfer": src_academictransfer, "80,000 Hours": src_80k, "Greenhouse boards": src_greenhouse,
    "Ashby boards": src_ashby, "Lever boards": src_lever, "Workable boards": src_workable,
    "Microsoft": src_microsoft, "Science Careers": src_science, "TenureTracker": src_tenuretracker,
    "Community sheet": src_sheets,
}


# ---------------------------------------------------------------- pipeline

def score(j):
    # Title matches count fully; matches only in the (often long, boilerplate) summary are capped.
    title, rest = j["title"].lower(), f"{j['summary']} {j['org']}".lower()
    in_title = sum(w for pat, w in KEYWORDS.items() if re.search(pat, title))
    in_rest = sum(w for pat, w in KEYWORDS.items() if not re.search(pat, title) and re.search(pat, rest))
    role = sum(w for pat, w in ROLE_BONUS.items() if re.search(pat, title))
    return in_title + min(in_rest, 4) + role


def norm_key(j):
    return re.sub(r"\W+", "", (j["title"] + j["org"]).lower())[:120]


def refresh():
    statuses, jobs = [], []
    with cf.ThreadPoolExecutor(len(SOURCES)) as ex:
        futs = {ex.submit(fn): name for name, fn in SOURCES.items()}
        for f in cf.as_completed(futs):
            name = futs[f]
            try:
                got = f.result()
                jobs += got
                statuses.append({"source": name, "ok": True, "count": len(got)})
                print(f"  ✓ {name:<20} {len(got):>5} raw")
            except Exception as e:
                statuses.append({"source": name, "ok": False, "count": 0, "error": str(e)[:200]})
                print(f"  ✗ {name:<20} {e}")

    prev = {}
    if (DATA / "jobs.json").exists():
        for p in json.loads((DATA / "jobs.json").read_text()).get("jobs", []):
            prev[p["id"]] = p.get("first_seen", TODAY)

    seen, clean = set(), []
    for j in jobs:
        if not j["title"] or not j["url"] or EXCLUDE.search(j["title"]):
            continue
        if j["deadline"] and j["deadline"] < TODAY:
            continue
        k = norm_key(j)
        if k in seen:
            continue
        seen.add(k)
        j["id"] = k[:60]
        j["region"] = region_of(j["location"])
        if j["region"] == "Other" and not NON_EUROPE.search(j["location"]):  # vague location: try the org name
            j["region"] = region_of(j["location"] + " " + j["org"])
        sheet_region = j.pop("sheet_region", "")
        if j["region"] == "Other" and sheet_region == "Europe":
            j["region"] = "Europe"
        j["location"] = j["location"] or sheet_region
        j["score"] = score(j)
        j["first_seen"] = prev.get(j["id"], TODAY)
        clean.append(j)
    clean.sort(key=lambda j: (-j["score"], j["deadline"] or "9999"))
    out = {"generated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "sources": statuses, "jobs": clean}
    (DATA / "jobs.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    by = {}
    for j in clean:
        by[j["region"]] = by.get(j["region"], 0) + 1
    print(f"\n  {len(clean)} listings after filtering/dedup  {by}")


def bundle():
    parts = {}
    for name in ["jobs", "fellowships", "guides", "checklist", "watchlist", "resources"]:
        p = DATA / f"{name}.json"
        parts[name] = json.loads(p.read_text()) if p.exists() else ([] if name != "jobs" else {"jobs": []})
    (DATA / "bundle.js").write_text("window.JOBDATA = " + json.dumps(parts, ensure_ascii=False) + ";\n")
    print(f"  wrote {DATA / 'bundle.js'}")


if __name__ == "__main__":
    DATA.mkdir(exist_ok=True)
    if "--bundle" not in sys.argv:
        print("Fetching live listings…")
        refresh()
    bundle()
