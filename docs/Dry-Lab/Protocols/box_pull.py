#!/usr/bin/env python3
"""Download Penn Box shared links straight onto a cluster (Betty or PMACS).

rclone's Box backend sees only your own Box tree; it cannot open a shared link
(https://upenn.box.com/s/...). This script uses your rclone Box login for the
token and Box's API with the `BoxApi: shared_link=` header to resolve each
link, list the folder, and stream every file to disk, checking its size and
Box's SHA-1. The token is read inside this process and never printed or logged.

One-time setup: an rclone remote named `box` in ~/.config/rclone/rclone.conf
(lab manual: Dry Lab > Protocols > Data Transfer, section 1).

Usage: box_pull.py <dest dir> <label>=<shared link> [<label>=<link> ...]
       [--list]            list the contents only, download nothing
       [--only SUBSTR]     download only files whose path contains SUBSTR
       [--exclude SUBSTR]  skip files whose path contains SUBSTR (e.g. .tif)
Each link is saved under <dest dir>/<label>/, keeping its folder structure.
Files already complete (same size) are skipped, so a rerun resumes.
Standard library only: /usr/bin/python3 on Betty works.

From prj2401 (scripts/00_box_pull.py), used to pull the 777/843/851 H&E and
annotations onto VAST, 2026-09-24.
"""
import sys, os, json, shutil, hashlib, subprocess, configparser, urllib.error, urllib.request, urllib.parse

args = [a for a in sys.argv[1:] if not a.startswith("--")]
LIST = "--list" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
EXCL = sys.argv[sys.argv.index("--exclude") + 1] if "--exclude" in sys.argv else None
args = [a for a in args if a not in (ONLY, EXCL)]
if len(args) < 2:
    sys.exit(__doc__)
dest, links = args[0], [a.split("=", 1) for a in args[1:]]
RCLONE = os.environ.get("RCLONE") or shutil.which("rclone") or os.path.expanduser("~/bin/rclone")
CONF = os.path.expanduser("~/.config/rclone/rclone.conf")

# let rclone refresh the OAuth token (it rewrites its config), then read it; never print it
subprocess.run([RCLONE, "lsd", "box:", "--max-depth", "1"], capture_output=True, timeout=120)
cfg = configparser.ConfigParser()
cfg.read(CONF)
if "box" not in cfg:
    sys.exit(f"no [box] remote in {CONF}: do the one-time rclone setup first")
TOKEN = json.loads(cfg["box"]["token"])["access_token"]


def api(url, link, stream=False):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}",
                                               "BoxApi": f"shared_link={link}"})
    try:
        r = urllib.request.urlopen(req, timeout=600)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit(f"404 for {link}: the link is probably collaborators-only. Ask its owner to set "
                     "'People with the link' to 'People in University of Pennsylvania'.")
        raise
    return r if stream else json.load(r)


def items(folder_id, link):
    out, off = [], 0
    while True:
        q = urllib.parse.urlencode({"fields": "id,type,name,size,sha1", "limit": 1000, "offset": off})
        page = api(f"https://api.box.com/2.0/folders/{folder_id}/items?{q}", link)
        out += page["entries"]
        off += len(page["entries"])
        if off >= page["total_count"] or not page["entries"]:
            return out


def walk(folder_id, link, prefix=""):
    # files carry their subfolder path in "rel" so the tree is mirrored on disk
    for e in items(folder_id, link):
        if e["type"] == "folder":
            yield from walk(e["id"], link, prefix + e["name"] + "/")
        elif e["type"] == "file":
            yield dict(e, rel=prefix + e["name"])


bad = 0
for label, link in links:
    root = api("https://api.box.com/2.0/shared_items?fields=id,type,name,size,sha1", link)
    files = [dict(root, rel=root["name"])] if root["type"] == "file" else list(walk(root["id"], link))
    print(f"[{label}] {root['type']} '{root['name']}': {len(files)} file(s)", flush=True)
    for f in files:
        print(f"    {f['size'] / 1e9:8.3f} GB  {f.get('sha1') or '-':40s}  {f['rel']}", flush=True)
    if LIST:
        continue
    os.makedirs(os.path.join(dest, label), exist_ok=True)
    for f in files:
        if ONLY and ONLY not in f["rel"]:
            continue
        if EXCL and EXCL in f["rel"]:
            continue
        path = os.path.join(dest, label, f["rel"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path) and os.path.getsize(path) == f["size"]:
            print(f"    skip (already complete): {f['rel']}", flush=True)
            continue
        h, n = hashlib.sha1(), 0
        with api(f"https://api.box.com/2.0/files/{f['id']}/content", link, stream=True) as r, \
                open(path + ".part", "wb") as w:
            for chunk in iter(lambda: r.read(8 << 20), b""):
                w.write(chunk)
                h.update(chunk)
                n += len(chunk)
        ok = n == f["size"] and (not f.get("sha1") or h.hexdigest() == f["sha1"])
        if ok:
            os.replace(path + ".part", path)
        else:
            bad += 1
        print(f"    {'OK  ' if ok else 'FAIL'} {f['rel']}  {n:,} bytes  sha1 {'match' if ok else 'MISMATCH'}", flush=True)
sys.exit(1 if bad else 0)
