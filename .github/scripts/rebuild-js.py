#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys
import urllib.request

EXPECTED_SHA256 = "ac6b3406c9678401b1a807fb2a832d6dc80f6cb79b7c85932f8e0f4a28baf014"
EXPECTED_BYTES = 201330
SOURCES = [
    "https://litter.catbox.moe/41sduf.js",
]

out = Path("assets/index-BdOqqwd8.js")
out.parent.mkdir(parents=True, exist_ok=True)

last_err = None
data = None
for url in SOURCES:
    try:
        print("fetch", url)
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = resp.read()
        break
    except Exception as exc:
        last_err = exc
        print("fetch failed", url, exc)

if data is None:
    print("all fetches failed", last_err)
    sys.exit(1)

sha = hashlib.sha256(data).hexdigest()
print("bytes", len(data), "sha256", sha)
if len(data) != EXPECTED_BYTES or sha != EXPECTED_SHA256:
    print("checksum mismatch")
    sys.exit(1)

out.write_bytes(data)
print("wrote", out)
print("ok")
