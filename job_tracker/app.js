/* Job Market Hub: static app, data comes from data/bundle.js (window.JOBDATA). */
(() => {
  const D = window.JOBDATA || {};
  const JOBS = (D.jobs && D.jobs.jobs) || [];
  const FELLOWS = D.fellowships || [];
  const GUIDES = D.guides || [];
  const CHECK = D.checklist || [];
  const WATCH = D.watchlist || [];
  const RES = D.resources || [];
  const TODAY = new Date().toISOString().slice(0, 10);
  const STATUSES = ["Interested", "Preparing", "Applied", "Interview", "Offer", "Closed"];

  // ------------------------------------------------------------ storage
  const KEY = "jobhub:v1";
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } };
  const S = Object.assign({ tracked: {}, hidden: {}, gone: {}, checklist: {}, watched: {}, prefs: {}, visit: {} }, load());
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch {} };
  const prevVisit = S.visit.current && S.visit.current !== TODAY ? S.visit.current : S.visit.prev;
  S.visit = { prev: prevVisit, current: TODAY };
  save();

  // ------------------------------------------------------------ helpers
  const $ = (s, r = document) => r.querySelector(s);
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const safeUrl = u => /^https?:\/\//i.test(u || "") ? esc(u) : "#";
  const days = d => d ? Math.round((new Date(d) - new Date(TODAY)) / 864e5) : null;
  const fmt = d => d ? new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }) : "";
  const dlBadge = d => {
    if (!d) return "";
    const n = days(d);
    const cls = n < 0 ? "muted" : n <= 14 ? "warn" : "muted";
    const txt = n < 0 ? "closed" : n === 0 ? "closes today" : `closes ${fmt(d)} (${n}d)`;
    return `<span class="b ${cls}">${txt}</span>`;
  };
  const opts = (sel, list, all) => { sel.innerHTML = `<option value="">${all}</option>` + list.map(x => `<option>${esc(x)}</option>`).join(""); };
  const uniq = a => [...new Set(a.filter(Boolean))].sort();
  const bind = (ids, fn) => ids.forEach(id => { const el = document.getElementById(id); el.addEventListener("input", fn); el.addEventListener("change", fn); });

  // ------------------------------------------------------------ tabs
  const renderers = {};
  function show(tab) {
    document.querySelectorAll(".tabs button").forEach(b => b.classList.toggle("active", b.dataset.tab === tab));
    document.querySelectorAll(".tab").forEach(s => s.classList.toggle("active", s.id === tab));
    S.prefs.tab = tab; save();
    renderers[tab] && renderers[tab]();
  }
  $("#tabs").addEventListener("click", e => { const b = e.target.closest("button"); if (b) show(b.dataset.tab); });

  // ------------------------------------------------------------ header
  (() => {
    const g = D.jobs && D.jobs.generated;
    const bad = ((D.jobs && D.jobs.sources) || []).filter(s => !s.ok).map(s => s.source);
    $("#meta").innerHTML = g
      ? `Listings updated ${esc(new Date(g).toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" }))} · ${JOBS.length} listings from ${(D.jobs.sources || []).length} sources` +
        (bad.length ? `<br><span class="bad">Failed on last refresh: ${esc(bad.join(", "))}</span>` : "")
      : `No listings yet.`;
  })();

  // ------------------------------------------------------------ tracker core
  function track(item) {
    if (S.tracked[item.id]) delete S.tracked[item.id];
    else S.tracked[item.id] = { status: "Interested", notes: "", added: TODAY, ...item };
    save(); updateTrackCount();
  }
  const updateTrackCount = () => { const n = Object.keys(S.tracked).length; $("#trackCount").textContent = n || ""; };
  updateTrackCount();

  // ------------------------------------------------------------ positions
  const REGIONS = ["UK", "Europe", "Remote", "Other"];
  const pos = Object.assign({ regions: ["UK", "Europe", "Remote"], minScore: 3 }, S.prefs.pos || {});
  $("#regionChips").innerHTML = REGIONS.map(r => `<button class="chip" data-r="${r}">${r} <small>${JOBS.filter(j => j.region === r).length}</small></button>`).join("");
  opts($("#kind"), uniq(JOBS.map(j => j.kind)), "All role types");
  opts($("#source"), uniq(JOBS.map(j => j.source)), "All sources");
  $("#minScore").value = pos.minScore;
  ["q", "kind", "source", "sort"].forEach(k => { if (pos[k]) $("#" + k).value = pos[k]; });
  $("#regionChips").addEventListener("click", e => {
    const b = e.target.closest(".chip"); if (!b) return;
    const r = b.dataset.r;
    pos.regions = pos.regions.includes(r) ? pos.regions.filter(x => x !== r) : [...pos.regions, r];
    renderPositions();
  });
  bind(["q", "kind", "source", "minScore", "sort", "onlyNew", "showHidden"], () => renderPositions());

  const shapeOf = kind => ({ Faculty: "faculty", Industry: "industry", Fellowship: "fellowship", Postdoc: "postdoc",
    "AI safety & policy": "safety" }[kind] || "other");
  const LEGEND = [["faculty", "Faculty"], ["industry", "Industry"], ["safety", "AI safety & policy"], ["fellowship", "Fellowship"],
    ["postdoc", "Postdoc"], ["other", "Other"]];

  function jobCard(j) {
    const isNew = prevVisit && j.first_seen > prevVisit;
    const hid = S.hidden[j.id], gone = S.gone[j.id];
    return `<div class="card job ${hid ? "hidden" : ""} ${gone ? "gone" : ""}" data-id="${esc(j.id)}">
      <i class="shape ${shapeOf(j.kind)}" title="${esc(j.kind)}"></i>
      <div>
        <h3><a href="${safeUrl(j.url)}" target="_blank" rel="noopener">${esc(j.title)}</a></h3>
        <div class="org">${esc(j.org)}${j.org && j.location ? " · " : ""}${esc(j.location)}</div>
        <div class="badges">
          ${gone ? `<span class="b gone">no longer available · marked ${fmt(gone)}</span>` : ""}
          ${isNew && !gone ? `<span class="b new">new</span>` : ""}
          <span class="b">${esc(j.kind)}</span>
          <span class="b muted">${esc(j.region)}</span>
          <span class="b muted">${esc(j.source)}</span>
          ${gone ? "" : dlBadge(j.deadline)}
          ${j.posted ? `<span class="b muted">posted ${fmt(j.posted)}</span>` : ""}
          ${j.salary ? `<span class="b ok">${esc(j.salary)}</span>` : ""}
        </div>
      </div>
      <div>
        <div class="actions">
          <button class="icon ${S.tracked[j.id] ? "on" : ""}" data-act="star" title="Save to tracker">★</button>
          <button class="icon ${gone ? "on-gone" : ""}" data-act="gone" title="${gone ? "Mark as still available" : "Mark ad as no longer available"}">⊘</button>
          <button class="icon" data-act="hide" title="${hid ? "Unhide" : "Hide"}">${hid ? "↺" : "✕"}</button>
        </div>
        <div class="score" title="Relevance score">rel ${j.score}</div>
      </div>
      ${j.summary ? `<p class="sum">${esc(j.summary)}</p>` : ""}
    </div>`;
  }

  function renderPositions() {
    Object.assign(pos, { q: $("#q").value, kind: $("#kind").value, source: $("#source").value, minScore: +$("#minScore").value, sort: $("#sort").value });
    S.prefs.pos = pos; save();
    $("#minScoreVal").textContent = pos.minScore;
    document.querySelectorAll("#regionChips .chip").forEach(c => c.classList.toggle("on", pos.regions.includes(c.dataset.r)));
    const q = pos.q.toLowerCase().trim();
    const onlyNew = $("#onlyNew").checked, showHidden = $("#showHidden").checked;
    let xs = JOBS.filter(j =>
      pos.regions.includes(j.region) && j.score >= pos.minScore &&
      (!pos.kind || j.kind === pos.kind) && (!pos.source || j.source === pos.source) &&
      (showHidden || (!S.hidden[j.id] && !S.gone[j.id])) && (!onlyNew || (prevVisit && j.first_seen > prevVisit)) &&
      (!q || `${j.title} ${j.org} ${j.location} ${j.summary}`.toLowerCase().includes(q)));
    const by = {
      score: (a, b) => b.score - a.score || (a.deadline || "9").localeCompare(b.deadline || "9"),
      deadline: (a, b) => (a.deadline || "9").localeCompare(b.deadline || "9") || b.score - a.score,
      posted: (a, b) => (b.posted || b.first_seen || "").localeCompare(a.posted || a.first_seen || ""),
    }[pos.sort || "score"];
    xs.sort(by);
    $("#posCount").innerHTML = `<span>${xs.length} positions${xs.length > 300 ? " · showing the first 300; narrow the filters to see others" : ""}</span>
      <span class="legend">${LEGEND.map(([c, l]) => `<span><i class="shape ${c}"></i>${l}</span>`).join("")}</span>`;
    $("#posList").innerHTML = xs.slice(0, 300).map(jobCard).join("") || `<div class="empty">No positions match these filters.</div>`;
  }
  renderers.positions = renderPositions;
  $("#posList").addEventListener("click", e => {
    const b = e.target.closest("[data-act]"); if (!b) return;
    const id = b.closest(".job").dataset.id, j = JOBS.find(x => x.id === id);
    if (b.dataset.act === "star") {
      track({ id, title: j.title, org: j.org, location: j.location, url: j.url, deadline: j.deadline, kind: j.kind });
      b.classList.toggle("on", !!S.tracked[id]);
    } else {
      const store = b.dataset.act === "gone" ? S.gone : S.hidden;
      store[id] ? delete store[id] : (store[id] = b.dataset.act === "gone" ? TODAY : 1);
      save(); renderPositions();
    }
  });

  // ------------------------------------------------------------ tracker board
  function renderTracker() {
    const items = Object.values(S.tracked);
    $("#board").innerHTML = items.length ? STATUSES.map(st => {
      const col = items.filter(i => i.status === st).sort((a, b) => (a.deadline || "9").localeCompare(b.deadline || "9"));
      return `<div class="col"><h4>${st} · ${col.length}</h4>${col.map(i => `
        <div class="card" data-id="${esc(i.id)}">
          <b><a href="${safeUrl(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></b>
          <span style="color:var(--muted)">${esc(i.org)}${i.location ? " · " + esc(i.location) : ""}</span>
          <div class="badges"><span class="b">${esc(i.kind || "")}</span>${S.gone[i.id] ? `<span class="b gone">ad no longer available</span>` : dlBadge(i.deadline)}</div>
          <div class="row">
            <select data-f="status">${STATUSES.map(s => `<option ${s === i.status ? "selected" : ""}>${s}</option>`).join("")}</select>
            <input type="date" data-f="deadline" value="${esc(i.deadline || "")}" title="Deadline">
            <button class="icon ${S.gone[i.id] ? "on-gone" : ""}" data-act="gone" title="${S.gone[i.id] ? "Mark as still available" : "Mark ad as no longer available"}">⊘</button>
            <button class="icon" data-act="del" title="Remove">✕</button>
          </div>
          <textarea data-f="notes" placeholder="Notes: contacts, referees asked, documents sent…">${esc(i.notes)}</textarea>
        </div>`).join("")}</div>`;
    }).join("") : `<div class="empty">Nothing tracked yet. Star (★) a position, fellowship or organisation, or add an application by hand.</div>`;
  }
  renderers.tracker = renderTracker;
  $("#board").addEventListener("change", e => {
    const f = e.target.dataset.f; if (!f) return;
    const id = e.target.closest(".card").dataset.id;
    S.tracked[id][f] = e.target.value; save();
    if (f !== "notes") renderTracker();
  });
  $("#board").addEventListener("click", e => {
    const act = e.target.dataset.act; if (!act) return;
    const id = e.target.closest(".card").dataset.id;
    if (act === "gone") { S.gone[id] ? delete S.gone[id] : (S.gone[id] = TODAY); save(); renderTracker(); return; }
    if (act !== "del") return;
    if (confirm(`Remove "${S.tracked[id].title}" from the tracker?`)) { delete S.tracked[id]; save(); updateTrackCount(); renderTracker(); }
  });
  $("#addManual").onclick = () => { $("#manualForm").hidden = !$("#manualForm").hidden; };
  $("#manualForm").addEventListener("submit", e => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(e.target));
    track({ id: "manual-" + Date.now(), ...f });
    e.target.reset(); e.target.hidden = true; renderTracker();
  });
  const download = (name, text, type) => {
    const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(new Blob([text], { type })), download: name });
    a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  };
  $("#exportJson").onclick = () => download(`jobhub-backup-${TODAY}.json`, JSON.stringify(S, null, 1), "application/json");
  $("#importJson").onchange = async e => {
    const file = e.target.files[0]; if (!file) return;
    try {
      const data = JSON.parse(await file.text());
      if (!confirm("Replace the tracker, checklist, hidden and unavailable items with the contents of this backup?")) return;
      Object.assign(S, data); save(); updateTrackCount(); renderTracker();
    } catch { alert("That file isn't a valid backup."); }
  };
  $("#exportIcs").onclick = () => {
    const ev = allDeadlines().filter(x => x.date >= TODAY);
    const d8 = d => d.replace(/-/g, "");
    const next = d => { const t = new Date(d + "T00:00:00Z"); t.setUTCDate(t.getUTCDate() + 1); return t.toISOString().slice(0, 10); };
    const clean = s => String(s || "").replace(/[\\;,]/g, m => "\\" + m).replace(/\n/g, " ");
    const body = ev.map(x => ["BEGIN:VEVENT", `UID:${clean(x.id)}@jobhub`, `DTSTAMP:${d8(TODAY)}T000000Z`,
      `DTSTART;VALUE=DATE:${d8(x.date)}`, `DTEND;VALUE=DATE:${d8(next(x.date))}`,
      `SUMMARY:Deadline: ${clean(x.title)}`, `DESCRIPTION:${clean(x.sub)} ${clean(x.url)}`, "END:VEVENT"].join("\r\n"));
    download("job-deadlines.ics", ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//jobhub//EN", ...body, "END:VCALENDAR"].join("\r\n"), "text/calendar");
  };

  // ------------------------------------------------------------ deadlines
  function allDeadlines() {
    const out = [];
    if ($("#dlTracked").checked) Object.values(S.tracked).forEach(i => i.deadline && i.status !== "Closed" && !S.gone[i.id] &&
      out.push({ id: i.id, date: i.deadline, title: i.title, sub: `${i.org || ""} · ${i.status}`, url: i.url, tag: "Tracked" }));
    if ($("#dlFellow").checked) FELLOWS.forEach(f => f.next_deadline && f.fit !== "low" && !S.tracked["fellow-" + f.id] &&
      out.push({ id: "fellow-" + f.id, date: f.next_deadline, title: f.name, sub: `${f.funder}${f.deadline_verified ? "" : " · date unconfirmed"}`, url: f.url, tag: "Fellowship" }));
    if ($("#dlJobs").checked) JOBS.forEach(j => j.deadline && j.score >= 6 && !S.gone[j.id] && ["UK", "Europe"].includes(j.region) && !S.tracked[j.id] &&
      out.push({ id: j.id, date: j.deadline, title: j.title, sub: `${j.org} · ${j.location}`, url: j.url, tag: "Open position" }));
    return out.sort((a, b) => a.date.localeCompare(b.date));
  }
  function renderDeadlines() {
    const xs = allDeadlines().filter(x => x.date >= TODAY);
    let month = "";
    $("#dlList").innerHTML = xs.map(x => {
      const m = new Date(x.date + "T00:00:00").toLocaleDateString("en-GB", { month: "long", year: "numeric" });
      const head = m !== month ? `<div class="month">${m}</div>` : ""; month = m;
      const n = days(x.date);
      return `${head}<div class="card dl ${n <= 14 ? "soon" : ""}">
        <div class="date">${fmt(x.date).replace(/ \d{4}$/, "")}<br><small style="color:var(--muted);font-weight:400">${n === 0 ? "today" : `in ${n}d`}</small></div>
        <div><a href="${safeUrl(x.url)}" target="_blank" rel="noopener"><b>${esc(x.title)}</b></a><br><small style="color:var(--muted)">${esc(x.sub)}</small></div>
        <span class="b ${x.tag === "Tracked" ? "ok" : "muted"}">${x.tag}</span></div>`;
    }).join("") || `<div class="empty">No upcoming deadlines for this selection.</div>`;
  }
  renderers.deadlines = renderDeadlines;
  bind(["dlTracked", "dlFellow", "dlJobs"], renderDeadlines);

  // ------------------------------------------------------------ fellowships
  function renderFellows() {
    const q = $("#fq").value.toLowerCase(), fit = $("#fFit").value, reg = $("#fRegion").value;
    const rank = { high: 0, medium: 1, low: 2 };
    const xs = FELLOWS.filter(f => (!q || JSON.stringify(f).toLowerCase().includes(q)) && (!reg || f.region === reg) &&
      (!fit || (fit === "high" ? f.fit === "high" : f.fit !== "low")))
      .sort((a, b) => (a.next_deadline && a.next_deadline >= TODAY ? a.next_deadline : "9").localeCompare(b.next_deadline && b.next_deadline >= TODAY ? b.next_deadline : "9") || rank[a.fit] - rank[b.fit]);
    $("#fList").innerHTML = xs.map(f => {
      const id = "fellow-" + f.id;
      return `<div class="card job" data-id="${esc(f.id)}">
        <i class="shape fellowship"></i>
        <div>
          <h3><a href="${safeUrl(f.url)}" target="_blank" rel="noopener">${esc(f.name)}</a></h3>
          <div class="org">${esc(f.funder)} · ${esc(f.country)}</div>
          <div class="badges">
            <span class="b ${f.fit === "high" ? "ok" : f.fit === "medium" ? "" : "muted"}">${esc(f.fit)} fit</span>
            ${f.next_deadline ? dlBadge(f.next_deadline) : ""}
            ${f.next_deadline && !f.deadline_verified ? `<span class="b warn">date unconfirmed</span>` : ""}
            <span class="b muted">${esc(f.duration)}</span>
            <span class="b muted">${esc(f.amount)}</span>
          </div>
        </div>
        <div class="actions"><button class="icon ${S.tracked[id] ? "on" : ""}" data-act="star" title="Save to tracker">★</button></div>
        <p class="sum" style="-webkit-line-clamp:unset"><b>Eligibility:</b> ${esc(f.eligibility)}. <b>Deadline:</b> ${esc(f.deadline_note)}<br>${esc(f.notes)}</p>
      </div>`;
    }).join("") || `<div class="empty">No fellowships match.</div>`;
  }
  renderers.fellowships = renderFellows;
  bind(["fq", "fFit", "fRegion"], renderFellows);
  $("#fList").addEventListener("click", e => {
    const b = e.target.closest("[data-act=star]"); if (!b) return;
    const f = FELLOWS.find(x => x.id === b.closest(".job").dataset.id);
    track({ id: "fellow-" + f.id, title: f.name, org: f.funder, location: f.country, url: f.url, deadline: f.next_deadline, kind: "Fellowship" });
    b.classList.toggle("on");
  });

  // ------------------------------------------------------------ watchlist
  const wTags = new Set();
  opts($("#wKind"), uniq(WATCH.map(w => w.kind)), "All kinds");
  $("#wTags").innerHTML = uniq(WATCH.flatMap(w => w.tags || [])).map(t => `<button class="chip" data-t="${esc(t)}">${esc(t)}</button>`).join("");
  $("#wTags").addEventListener("click", e => {
    const b = e.target.closest(".chip"); if (!b) return;
    wTags.has(b.dataset.t) ? wTags.delete(b.dataset.t) : wTags.add(b.dataset.t);
    b.classList.toggle("on"); renderWatch();
  });
  function renderWatch() {
    const q = $("#wq").value.toLowerCase(), kind = $("#wKind").value, stale = $("#wStale").checked;
    const xs = WATCH.filter(w => (!q || JSON.stringify(w).toLowerCase().includes(q)) && (!kind || w.kind === kind) &&
      [...wTags].every(t => (w.tags || []).includes(t)) &&
      (!stale || !S.watched[w.id] || days(S.watched[w.id]) <= -14));
    $("#wList").innerHTML = xs.map(w => {
      const last = S.watched[w.id], id = "org-" + w.id;
      return `<div class="card" data-id="${esc(w.id)}">
        <h3>${esc(w.name)}</h3>
        <div class="org" style="color:var(--muted);font-size:13px">${esc(w.kind)} · ${esc(w.city ? w.city + ", " : "")}${esc(w.country)}</div>
        <p>${esc(w.why)}</p>
        <div class="badges">${(w.tags || []).map(t => `<span class="b muted">${esc(t)}</span>`).join("")}</div>
        <div class="foot" style="margin-top:8px">
          <a href="${safeUrl(w.careers_url)}" target="_blank" rel="noopener" data-act="open">Careers page ↗</a>
          <span>${last ? `checked ${-days(last)}d ago` : "never checked"}
            <button class="icon ${S.tracked[id] ? "on" : ""}" data-act="star" title="Save to tracker">★</button></span>
        </div></div>`;
    }).join("") || `<div class="empty">No organisations match.</div>`;
  }
  renderers.watchlist = renderWatch;
  bind(["wq", "wKind", "wStale"], renderWatch);
  $("#wList").addEventListener("click", e => {
    const b = e.target.closest("[data-act]"); if (!b) return;
    const w = WATCH.find(x => x.id === b.closest(".card").dataset.id);
    if (b.dataset.act === "open") { S.watched[w.id] = TODAY; save(); setTimeout(renderWatch, 50); }
    else { track({ id: "org-" + w.id, title: `Watch: ${w.name}`, org: w.name, location: w.city || w.country, url: w.careers_url, kind: w.kind }); b.classList.toggle("on"); }
  });

  // ------------------------------------------------------------ guides
  let gSel = S.prefs.guide || (GUIDES[0] && GUIDES[0].code);
  function renderGuides() {
    $("#gNav").innerHTML = GUIDES.map(g => `<button data-c="${esc(g.code)}" class="${g.code === gSel ? "active" : ""}"><span class="cc">${esc(g.code)}</span>${esc(g.country)}</button>`).join("");
    const g = GUIDES.find(x => x.code === gSel);
    if (!g) { $("#gBody").innerHTML = `<div class="empty">No guides yet.</div>`; return; }
    const sec = (t, v) => v ? `<h4>${t}</h4><p>${esc(v)}</p>` : "";
    $("#gBody").innerHTML = `<h2><span class="cc">${esc(g.code)}</span>${esc(g.country)}</h2>
      ${sec("Career ladder", g.titles)}${sec("Tenure and permanence", g.tenure)}${sec("Hiring cycle", g.hiring_cycle)}
      ${sec("Application and interview process", g.process)}${sec("Salary", g.salary)}${sec("Start-up and funding", g.startup)}
      ${sec("Teaching load", g.teaching_load)}${sec("Language", g.language)}${sec("Visa and right to work", g.visa)}
      ${(g.tips || []).length ? `<h4>Tips</h4><ul>${g.tips.map(t => `<li>${esc(t)}</li>`).join("")}</ul>` : ""}
      ${(g.boards || []).length ? `<h4>Job boards</h4><p>${g.boards.map(b => `<a href="${safeUrl(b.url)}" target="_blank" rel="noopener">${esc(b.name)}</a>`).join(" · ")}</p>` : ""}`;
  }
  renderers.guides = renderGuides;
  $("#gNav").addEventListener("click", e => { const b = e.target.closest("button"); if (b) { gSel = S.prefs.guide = b.dataset.c; save(); renderGuides(); } });

  // ------------------------------------------------------------ checklist
  opts($("#cRegion"), uniq(CHECK.map(c => c.region)).filter(r => r !== "All"), "All regions");
  $("#cRegion").value = S.prefs.cRegion || "";
  function renderChecklist() {
    const reg = S.prefs.cRegion = $("#cRegion").value; save();
    const xs = CHECK.filter(c => !reg || c.region === "All" || c.region === reg);
    const done = xs.filter(c => S.checklist[c.id]).length;
    $("#cBar").style.width = xs.length ? (100 * done / xs.length) + "%" : 0;
    $("#cPct").textContent = `${done} / ${xs.length} done`;
    const groups = uniq(xs.map(c => c.group));
    const order = ["Core documents", "Research", "Teaching", "References", "Industry", "Region-specific", "Interview prep"];
    groups.sort((a, b) => order.indexOf(a) - order.indexOf(b));
    $("#cList").innerHTML = groups.map(g => `<div class="group"><h3>${esc(g)}</h3>${xs.filter(c => c.group === g).map(c => `
      <label class="card ck ${S.checklist[c.id] ? "done" : ""}">
        <input type="checkbox" data-id="${esc(c.id)}" ${S.checklist[c.id] ? "checked" : ""}>
        <div><div class="t">${esc(c.item)}</div><div class="d">${esc(c.detail)}</div></div>
        <span class="b muted">${esc(c.region)}</span></label>`).join("")}</div>`).join("");
  }
  renderers.checklist = renderChecklist;
  $("#cRegion").addEventListener("change", renderChecklist);
  $("#cList").addEventListener("change", e => {
    const id = e.target.dataset.id; if (!id) return;
    e.target.checked ? (S.checklist[id] = TODAY) : delete S.checklist[id];
    save(); renderChecklist();
  });

  // ------------------------------------------------------------ resources
  function renderResources() {
    const q = $("#rq").value.toLowerCase();
    const xs = RES.filter(r => !q || JSON.stringify(r).toLowerCase().includes(q));
    $("#rList").innerHTML = `<div class="res">` + uniq(xs.map(r => r.category)).map(cat => `<h3>${esc(cat)}</h3>` +
      xs.filter(r => r.category === cat).map(r => `<div class="card">
        <a href="${safeUrl(r.url)}" target="_blank" rel="noopener"><b>${esc(r.name)}</b></a>
        <span class="b muted" style="grid-row:1/3;grid-column:2;align-self:center">${esc(r.region)}</span>
        <span>${esc(r.description)}</span></div>`).join("")).join("") + `</div>` || `<div class="empty">No resources match.</div>`;
  }
  renderers.resources = renderResources;
  bind(["rq"], renderResources);

  show(S.prefs.tab || "positions");
})();
