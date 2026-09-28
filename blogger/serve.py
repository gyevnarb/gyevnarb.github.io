#!/usr/bin/env python3
"""Local server for the blog-post editor.

Serves blogger/index.html and a small JSON API that reads and writes posts in
this repository. Run from anywhere:

    python3 blogger/serve.py            # then open http://127.0.0.1:4010
    python3 blogger/serve.py --port 5000

It only listens on localhost and only writes inside _posts/,
assets/bibliography/ and assets/img/blog/.
"""
import argparse
import base64
import json
import re
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POSTS = ROOT / "_posts"
BIBS = ROOT / "assets" / "bibliography"
IMAGES = ROOT / "assets" / "img" / "blog"

SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
TYPES = {
    ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp",
    ".svg": "image/svg+xml", ".pdf": "application/pdf",
}


def front_value(text, key):
    m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip("\"'") if m else ""


def safe_file(folder, name):
    if not SAFE_NAME.match(name or ""):
        raise ValueError(f"invalid file name: {name!r}")
    path = (folder / name).resolve()
    if path.parent != folder.resolve():
        raise ValueError("path outside allowed folder")
    return path


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def send_file(self, path, ctype=None):
        if not path.is_file():
            return self.send(404, {"error": "not found"})
        self.send(200, path.read_bytes(), ctype or TYPES.get(path.suffix.lower(), "application/octet-stream"))

    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)
        try:
            if url.path in ("/", "/index.html"):
                return self.send_file(HERE / "index.html")
            if url.path == "/site.css":  # the site's stylesheet is plain CSS
                return self.send_file(ROOT / "_includes" / "site.scss", TYPES[".css"])
            if url.path.startswith("/assets/"):
                path = (ROOT / unquote(url.path).lstrip("/")).resolve()
                if ROOT / "assets" not in path.parents:
                    return self.send(403, {"error": "forbidden"})
                return self.send_file(path)
            if url.path == "/api/posts":
                posts = []
                for p in sorted(POSTS.glob("*.md"), reverse=True):
                    text = p.read_text(encoding="utf-8")
                    posts.append({
                        "file": p.name,
                        "title": front_value(text, "title"),
                        "external": bool(front_value(text, "redirect")),
                    })
                return self.send(200, posts)
            if url.path == "/api/post":
                path = safe_file(POSTS, q.get("file", [""])[0])
                text = path.read_text(encoding="utf-8")
                bibname = front_value(text, "bibliography")
                bib = ""
                if bibname:
                    bpath = safe_file(BIBS, bibname)
                    bib = bpath.read_text(encoding="utf-8") if bpath.exists() else ""
                return self.send(200, {"file": path.name, "text": text, "bibname": bibname, "bib": bib})
            if url.path == "/api/exists":
                name = q.get("file", [""])[0]
                return self.send(200, {"exists": safe_file(POSTS, name).exists()})
        except (ValueError, OSError) as e:
            return self.send(400, {"error": str(e)})
        self.send(404, {"error": "not found"})

    def do_POST(self):
        url = urlparse(self.path)
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
            if url.path == "/api/save":
                post = safe_file(POSTS, data["file"])
                if post.exists() and not data.get("overwrite"):
                    return self.send(409, {"error": f"{post.name} already exists"})
                written = []
                if data.get("bibname"):
                    bib = safe_file(BIBS, data["bibname"])
                    BIBS.mkdir(parents=True, exist_ok=True)
                    bib.write_text(data.get("bib", ""), encoding="utf-8")
                    written.append(str(bib.relative_to(ROOT)))
                post.write_text(data["text"], encoding="utf-8")
                written.insert(0, str(post.relative_to(ROOT)))
                old = data.get("previous")
                if old and old != post.name:  # renamed (e.g. new date or slug)
                    old_path = safe_file(POSTS, old)
                    if old_path.exists():
                        old_path.unlink()
                        written.append(f"removed {old_path.relative_to(ROOT)}")
                return self.send(200, {"written": written})
            if url.path == "/api/image":
                img = safe_file(IMAGES, data["name"])
                IMAGES.mkdir(parents=True, exist_ok=True)
                img.write_bytes(base64.b64decode(data["data"]))
                return self.send(200, {"url": "/" + str(img.relative_to(ROOT))})
        except (KeyError, ValueError, OSError, json.JSONDecodeError) as e:
            return self.send(400, {"error": str(e)})
        self.send(404, {"error": "not found"})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=4010)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://127.0.0.1:{args.port}"
    print(f"Blogger running at {url}  (Ctrl+C to stop)")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
