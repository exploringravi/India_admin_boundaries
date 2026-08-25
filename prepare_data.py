"""
Repack geoBoundaries India zips into GeoPackages.

Run from the folder containing the four -all.zip files:
    python prepare_data.py

Outputs:
    india_adm.gpkg        simplified geometry, goes in the repo
    india_adm_full.gpkg   full resolution, kept local, too big for GitHub
    meta/                 original geoBoundaries metadata per level
"""

import os
import zipfile
import geopandas as gpd

LEVELS = [1, 2, 3, 4]
SIMP = "india_adm.gpkg"
FULL = "india_adm_full.gpkg"

for base in (SIMP, FULL):
    for ext in ("", "-shm", "-wal"):
        if os.path.exists(base + ext):
            os.remove(base + ext)

os.makedirs("meta", exist_ok=True)
rows = []

for lvl in LEVELS:
    zpath = f"geoBoundaries-IND-ADM{lvl}-all.zip"
    if not os.path.exists(zpath):
        print(f"MISSING {zpath}, skipped")
        continue

    z = zipfile.ZipFile(zpath)
    shps = [n for n in z.namelist() if n.lower().endswith(".shp")]
    simp = [n for n in shps if "simplified" in n.lower()]
    full = [n for n in shps if "simplified" not in n.lower()]

    row = {"lvl": lvl}

    if full:
        src = f"/vsizip/{os.path.abspath(zpath)}/{full[0]}"
        g = gpd.read_file(src)
        g.to_file(FULL, layer=f"adm{lvl}", driver="GPKG")
        row["n"] = len(g)
        row["v_full"] = int(g.count_coordinates().sum())

    if simp:
        src = f"/vsizip/{os.path.abspath(zpath)}/{simp[0]}"
        g = gpd.read_file(src)
        g.to_file(SIMP, layer=f"adm{lvl}", driver="GPKG")
        row["v_simp"] = int(g.count_coordinates().sum())
    else:
        print(f"ADM{lvl}: no simplified version in the zip")

    metas = [n for n in z.namelist() if n.lower().endswith("meta.txt")]
    if metas:
        with open(f"meta/meta_adm{lvl}.txt", "wb") as f:
            f.write(z.read(metas[0]))

    rows.append(row)
    print(f"ADM{lvl}: {row.get('n', 0):,} features, "
          f"vertices {row.get('v_full', 0):,} -> {row.get('v_simp', 0):,}")

print("\n--- values for the README table ---")
for r in rows:
    print(f"| `adm{r['lvl']}` | ADM{r['lvl']} | ... | {r.get('n', 0):,} |")

print()
for f in (SIMP, FULL):
    if os.path.exists(f):
        print(f"{f}: {os.path.getsize(f) / 1024 / 1024:.1f} MB")