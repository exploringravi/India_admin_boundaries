"""
Build shapefile-only zips from the geoBoundaries -all archives.

Keeps .shp .shx .dbf .prj plus the metadata and citation files.
Drops .geojson and .topojson, which are duplicate geometry.

    python make_shp_zips.py            # full resolution
    python make_shp_zips.py simplified # simplified geometry, much smaller
"""

import os
import sys
import zipfile

SIMPLIFIED = len(sys.argv) > 1 and sys.argv[1].startswith("simp")
KEEP = (".shp", ".shx", ".dbf", ".prj", ".cpg")
OUTDIR = "shp_simplified" if SIMPLIFIED else "shp"

os.makedirs(OUTDIR, exist_ok=True)

for lvl in [1, 2, 3, 4]:
    src = f"geoBoundaries-IND-ADM{lvl}-all.zip"
    if not os.path.exists(src):
        print(f"MISSING {src}")
        continue

    z = zipfile.ZipFile(src)
    suffix = "-simplified" if SIMPLIFIED else ""
    out = f"{OUTDIR}/geoBoundaries-IND-ADM{lvl}-shp{suffix}.zip"

    picked = []
    for n in z.namelist():
        low = n.lower()
        is_simp = "_simplified" in low
        if low.endswith(KEEP) and is_simp == SIMPLIFIED:
            picked.append(n)
        elif low.endswith("metadata.txt") or "citation-and-use" in low:
            picked.append(n)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as o:
        for n in picked:
            o.writestr(os.path.basename(n), z.read(n))

    mb = os.path.getsize(out) / 1024 / 1024
    print(f"ADM{lvl}: {len(picked)} files -> {out}  {mb:.1f} MB")

total = sum(os.path.getsize(os.path.join(OUTDIR, f))
            for f in os.listdir(OUTDIR)) / 1024 / 1024
print(f"\nTotal: {total:.1f} MB in {OUTDIR}/")
