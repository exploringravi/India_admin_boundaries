"""Pull the metadata and citation files out of the geoBoundaries zips."""

import os
import zipfile

os.makedirs("meta", exist_ok=True)
got_citation = False

for lvl in [1, 2, 3, 4]:
    zpath = f"geoBoundaries-IND-ADM{lvl}-all.zip"
    if not os.path.exists(zpath):
        continue
    z = zipfile.ZipFile(zpath)

    for name in z.namelist():
        low = name.lower()
        if low.endswith("metadata.txt") or low.endswith("metadata.json"):
            out = f"meta/{os.path.basename(name)}"
            with open(out, "wb") as f:
                f.write(z.read(name))
            print("wrote", out)
        elif "citation-and-use" in low and not got_citation:
            with open("meta/CITATION-AND-USE-geoBoundaries.txt", "wb") as f:
                f.write(z.read(name))
            got_citation = True
            print("wrote meta/CITATION-AND-USE-geoBoundaries.txt")

print("\n--- ADM3 metadata ---")
print(open("meta/geoBoundaries-IND-ADM3-metaData.txt", encoding="utf-8").read())
print("\n--- ADM4 metadata ---")
print(open("meta/geoBoundaries-IND-ADM4-metaData.txt", encoding="utf-8").read())
