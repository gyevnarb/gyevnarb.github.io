# Blogger

A small local editor for writing posts for gbalint.me.

```
python3 blogger/serve.py
```

This opens <http://127.0.0.1:4010>. Posts are saved to `_posts/`, bibliographies to `assets/bibliography/`, and uploaded images to `assets/img/blog/`. The folder is excluded from the Jekyll build.

- **Write**: Markdown with a live preview styled like the site. `###` headings become the contents list.
- **Cite**: the `[1]` button (Ctrl/Cmd+Shift+C) or **cite** in the References tab inserts `<d-cite key="…"/>`. Citing right after an existing citation adds to it.
- **Footnotes**: the `¹` button (Ctrl/Cmd+Shift+F) inserts `<d-footnote>…</d-footnote>`.
- **References**: import or drop `.bib` files, paste BibTeX (also straight into the editor), or add by DOI through Crossref.
- **Checks**: flags missing references, uncited entries, missing alt text, and more.
- **Save to site** (Ctrl/Cmd+S) writes the files. **Download** saves them locally instead, which also works without the server.

Drafts are kept in the browser automatically. Open an existing post from the **Open…** menu, or with `?open=<file>.md`.
