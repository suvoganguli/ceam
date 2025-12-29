# NTL Data Download + Extract (curl) — VIIRS DNB Monthly Composites (VCMCFG)

This runbook downloads and extracts VIIRS DNB monthly composites tiles using curl.
We use the 75N060E tile (covers India/Bangladesh/Sundarbans region).

## Folder structure
- data/ntl/raw/YYYYMM/  (each month’s tgz + extracted .tif files)

## Prereqs
- macOS/Linux shell
- curl, tar, gunzip, unzip

## Base URL (NOAA/NCEI)
Monthly product directories look like:

https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10/YYYYMM/vcmcfg/

Example (June 2018):
https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10/201806/vcmcfg/

## Files you care about (after extract)
- `*.avg_rade9h.tif`  → radiance (nighttime lights intensity)
- `*.cf_cvg.tif`      → cloud-free coverage / observation-coverage proxy (useful for masking)

## Download function (curl + resume + extract)

Usage:
  - download_month 201806
  - download_month 201801

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
