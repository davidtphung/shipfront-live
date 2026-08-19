#!/usr/bin/env python3
from pathlib import Path
import base64
import hashlib
import sys

EXPECTED_SHA256 = "ac6b3406c9678401b1a807fb2a832d6dc80f6cb79b7c85932f8e0f4a28baf014"
EXPECTED_BYTES = 201330
N_PARTS = 12

parts_dir = Path("assets/_js_parts")
parts = [parts_dir / f"part{i:02d}.b64" for i in range(N_PARTS)]
missing = [str(p) for p in parts if not p.exists()]
if missing:
    print("missing parts:", ", ".join(missing))
    sys.exit(1)

blobs = []
for p in parts:
    blobs.append(base64.b64decode("".join(p.read_text(encoding="ascii").split())))
data = b"".join(blobs)
out = Path("assets/index-BdOqqwd8.js")
out.write_bytes(data)
sha = hashlib.sha256(data).hexdigest()
print("wrote", out, "bytes", len(data), "sha256", sha)
if len(data) != EXPECTED_BYTES or sha != EXPECTED_SHA256:
    print("checksum mismatch")
    sys.exit(1)
print("ok")
