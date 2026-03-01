# CEAM Data Download Runbook

This runbook downloads all external data used by notebooks 02–05.

## Folder Layout

- data/basemaps/natural_earth/
- data/basemaps/osm/
- data/worldpop/raw/2019/
- data/ntl/raw/YYYYMM/


## 1) Basemaps

```bash
mkdir -p data/basemaps/natural_earth

# Countries (110m Admin 0)
curl -L -o data/basemaps/natural_earth/ne_110m_admin_0_countries.zip "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
unzip -o data/basemaps/natural_earth/ne_110m_admin_0_countries.zip -d data/basemaps/natural_earth

# Land polygons (10m)
curl -L -o data/basemaps/natural_earth/ne_10m_land.zip "https://naturalearth.s3.amazonaws.com/10m_physical/ne_10m_land.zip"
unzip -o data/basemaps/natural_earth/ne_10m_land.zip -d data/basemaps/natural_earth
```

## 2) OSM Boundary (Sundarban GeoJSON)

```bash
# One-time install
npm install -g osmtogeojson

REL_ID=14937802
mkdir -p data/basemaps/osm

curl -G "https://overpass-api.de/api/interpreter" \
  --data-urlencode "data=
[out:json][timeout:180];
relation(${REL_ID});
(._;>;);
out body;
" \
| osmtogeojson \
> data/basemaps/osm/sundarbans_relation_${REL_ID}.geojson
```

## 3) 3WorldPop (raw GeoTIFFs)

```bash
mkdir -p data/worldpop/raw/2019

curl -L -o data/worldpop/raw/2019/ind_ppp_2019_1km_Aggregated.tif \
"https://data.worldpop.org/GIS/Population/Global_2000_2020_1km/2019/IND/ind_ppp_2019_1km_Aggregated.tif"

curl -L -o data/worldpop/raw/2019/bgd_ppp_2019_1km_Aggregated.tif \
"https://data.worldpop.org/GIS/Population/Global_2000_2020_1km/2019/BGD/bgd_ppp_2019_1km_Aggregated.tif"
```

## 4) VIIRS NTL (Monthly Composites — VCMCFG)

This code downloads and extracts VIIRS DNB monthly composites tiles using curl.
We use the 75N060E tile (covers India/Bangladesh/Sundarbans region).

### Folder structure
- data/ntl/raw/YYYYMM/  (each month’s tgz + extracted .tif files)

### Base URL (NOAA/NCEI)
Monthly product directories look like:

https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10/YYYYMM/vcmcfg/

Example (June 2018):
https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10/201806/vcmcfg/

### Files required to download
- `*.avg_rade9h.tif`  → radiance (nighttime lights intensity)
- `*.cf_cvg.tif`      → cloud-free coverage / observation-coverage proxy (useful for masking)

### Download function (curl + resume + extract)

Usage:
  - download_month 201806
  - download_month 201904

Notes:
- Uses curl + grep on directory listing to find the correct filename.
- Uses resume (-C -) and retries.

```bash
download_month () {
  YYYYMM="$1"
  TILE="75N060E"
  PRODUCT="vcmcfg"
  BASE="https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10/${YYYYMM}/${PRODUCT}/"

  OUTDIR="data/ntl/raw/${YYYYMM}"
  mkdir -p "${OUTDIR}"
  cd "${OUTDIR}" || exit 1

  echo "Listing: ${BASE}"
  FNAME=$(curl -fsSL "${BASE}" | grep -oE "SVDNB_npp_${YYYYMM}[0-9]{2}-[0-9]{8}_${TILE}_${PRODUCT}_v10_c[0-9]+\.tgz" | head -n 1)

  if [ -z "${FNAME}" ]; then
    echo "ERROR: Could not find matching tgz for ${YYYYMM} tile=${TILE} product=${PRODUCT}"
    echo "Check the directory listing manually: ${BASE}"
    cd - >/dev/null 2>&1
    return 1
  fi

  echo "Downloading: ${FNAME}"
  curl -fL --retry 5 --retry-delay 2 -C - -o "${FNAME}" "${BASE}${FNAME}"

  echo "Verify gzip integrity..."
  gunzip -t "${FNAME}"

  echo "Extract..."
  tar -xzf "${FNAME}"

  echo "List extracted TIFFs:"
  ls -lh *.tif | sed -e 's/^/  /'

  cd - >/dev/null 2>&1
}
```

