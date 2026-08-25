<div align="center">

# India Administrative Boundaries

**Ready-to-use administrative boundary data for India, ADM1 to ADM4**

Prepared for the CityAI GIS workshop

![Source](https://img.shields.io/badge/source-geoBoundaries-1f6feb)
![Format](https://img.shields.io/badge/format-GeoPackage-2ea043)
![CRS](https://img.shields.io/badge/CRS-EPSG%3A4326-8250df)
![Levels](https://img.shields.io/badge/levels-ADM1%20to%20ADM4-fb8500)

</div>

---

## What is in here

One GeoPackage, `india_adm.gpkg`, holding four layers.

| Layer | Level | Unit in India | Features |
|:---|:---|:---|---:|
| `adm1` | ADM1 | States and Union Territories | 36 |
| `adm2` | ADM2 | Districts | 735 |
| `adm3` | ADM3 | Sub-districts (tehsils, taluks, blocks) | 6,824 |
| `adm4` | ADM4 | See `meta/meta_adm4.txt` | 7,143 |

Plus `meta/`, the original geoBoundaries metadata for each level. That is where the source agency, build date and license for each layer are recorded.

CRS is EPSG:4326, WGS 84 geographic.

### Geometry is simplified

This GeoPackage uses the simplified geometry that geoBoundaries publishes alongside the full-resolution version. Vertex counts:

| Level | Full | Simplified | Reduction |
|:---|---:|---:|---:|
| ADM1 | 1,055,284 | 116,391 | 89% |
| ADM2 | 1,996,081 | 322,761 | 84% |
| ADM3 | 2,394,766 | 880,598 | 63% |
| ADM4 | 2,486,494 | 899,265 | 64% |

Full resolution is 133 MB, past the GitHub file limit. Simplified is 46 MB and visually identical above roughly 1:250,000.

**If you need full resolution**, run `prepare_data.py` from a folder holding the four geoBoundaries `-all.zip` files. It writes `india_adm_full.gpkg` alongside the simplified one. Do not measure boundary length or do precise point-in-polygon work on the simplified version.

**ADM5 is not included** at either resolution. The file is around 900 MB. Pull it from the API instead, see [Getting ADM5](#getting-adm5).

---

## Before the workshop

**1. Install QGIS.** Download the Long Term Release from [qgis.org/download](https://qgis.org/download/). It is free, runs on Windows, macOS and Linux. The LTR is more stable than the latest version, pick that one.

**2. Get the data.** Either clone the repo:

```bash
git clone https://github.com/cityaispace-ship-it/India_admin_boundaries.git
```

or use the green **Code** button above and choose **Download ZIP**.

**3. Open it.** Drag `india_adm.gpkg` onto the QGIS map canvas. A dialog lists the four layers. Select the ones you want and click Add.

That is the whole setup. No unzipping, no shapefile sidecar files to keep track of.

---

## Using the data

### QGIS

Drag and drop as above. To load a single layer from the Browser panel, expand the GeoPackage entry and double-click the layer.

### Python (geopandas)

```python
import geopandas as gpd

adm2 = gpd.read_file("india_adm.gpkg", layer="adm2")
print(adm2.shape)
adm2.plot()
```

List the layers without loading them:

```python
print(gpd.list_layers("india_adm.gpkg"))
```

### R (sf)

```r
library(sf)

st_layers("india_adm.gpkg")
adm2 <- st_read("india_adm.gpkg", layer = "adm2")
plot(st_geometry(adm2))
```

---

## Attributes

| Field | Meaning |
|:---|:---|
| `shapeName` | Name of the administrative unit |
| `shapeID` | Unique geoBoundaries identifier |
| `shapeGroup` | Country code, `IND` throughout |
| `shapeType` | Administrative level, for example `ADM2` |
| `shapeISO` | ISO code where one exists, often empty at lower levels |

> **Join on `shapeID`, not `shapeName`.** Names repeat across states and spellings vary between sources. A name join will silently drop or duplicate rows.

---

## Things that will bite you

- **Counts do not match official figures.** India creates new districts regularly. This is a snapshot, not a live register.
- **Lower levels are patchy.** ADM3 and ADM4 coverage and positional accuracy are weaker than ADM1 and ADM2.
- **Geometries are not always clean.** Run *Vector > Geometry Tools > Check Validity* before any overlay or dissolve.
- **Do not measure area in EPSG:4326.** Degrees are not metres. Reproject to an equal-area CRS first, for example EPSG:7755.

---

## Getting ADM5

The geoBoundaries API returns download links for any level:

```python
import requests

meta = requests.get(
    "https://www.geoboundaries.org/api/current/gbOpen/IND/ADM5/"
).json()

print(meta["boundaryName"], meta["admUnitCount"])
print(meta["simplifiedGeometryGeoJSON"])   # small, start here
print(meta["staticDownloadLink"])          # full zip, large
```

Use the simplified GeoJSON unless you genuinely need village-level precision.

---

## How to cite

Two citations, and both are needed. This repository is a compilation. The boundaries themselves come from geoBoundaries.

**For this compilation:**

> Pandey, R. K. (2026). *India Administrative Boundaries (ADM1 to ADM4): a GeoPackage compilation for GIS teaching* [Data set]. https://github.com/cityaispace-ship-it/India_admin_boundaries

**For the underlying data, required in all cases:**

> Runfola, D. et al. (2020) geoBoundaries: A global database of political administrative boundaries. *PLoS ONE* 15(4): e0231866. https://doi.org/10.1371/journal.pone.0231866

A `CITATION.cff` file is included, so GitHub renders a **Cite this repository** button in the sidebar and can export BibTeX and APA directly.

### License of the underlying data

The gbOpen release is open but **not uniformly CC BY 4.0**. Individual boundaries can carry ODbL or CC BY-SA terms inherited from the national source. Check the file in `meta/` for the level you are using before reusing the data outside teaching.

Data source: [geoboundaries.org](https://www.geoboundaries.org/)

## Boundary disclaimer

Boundaries are those supplied by geoBoundaries and are provided for teaching and analysis only. They are not authoritative and represent no position on the status of any disputed territory. For official or legal use, refer to Survey of India.
