# ceam_config.py
from pathlib import Path

# Project root (one level above prelim_analysis)
ROOT = Path(__file__).resolve().parent.parent

DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"

CRS_WGS84 = "EPSG:4326"
CRS_METRIC = "EPSG:3857"

BBOX = {
    "lon_min": 88.50,
    "lat_min": 21.50,
    "lon_max": 89.92,
    "lat_max": 22.50,
}

# Maps are obtained using the following:
#
#curl -L -o data/worldpop/raw/2019/ind_ppp_2019_1km_Aggregated.tif \
#  "https://data.worldpop.org/GIS/Population/Global_2000_2020_1km/2019/IND/ind_ppp_2019_1km_Aggregated.tif"
#
#curl -L -o data/worldpop/raw/2019/bgd_ppp_2019_1km_Aggregated.tif \
#  "https://data.worldpop.org/GIS/Population/Global_2000_2020_1km/2019/BGD/bgd_ppp_2019_1km_Aggregated.tif"
#
#npm install -g osmtogeojson
#
#REL_ID=14937802
#mkdir -p data/basemaps/osm
#
#curl -G "https://overpass-api.de/api/interpreter" \
#  --data-urlencode "data=
#[out:json][timeout:180];
#relation(${REL_ID});
#(._;>;);
#out body;
#" \
#| osmtogeojson \
#> data/basemaps/osm/sundarbans_relation_${REL_ID}.geojson

PATHS = {
    # Basemaps
    "countries_shp": DATA / "basemaps/natural_earth/ne_110m_admin_0_countries.shp",
    "land_shp": DATA / "basemaps/natural_earth/ne_10m_land.shp",
    "sund_osm_geojson": DATA / "basemaps/osm/sundarbans_relation_14937802.geojson",

    # WorldPop raw files
    "worldpop_ind_raw": DATA / "worldpop/raw/2019/ind_ppp_2019_1km_Aggregated.tif",
    "worldpop_bgd_raw": DATA / "worldpop/raw/2019/bgd_ppp_2019_1km_Aggregated.tif",

    # WorldPop processed files
    "fig_worldpop_clip": OUTPUTS / "figures/worldpop_2019_ppp_clip.png",
    "fig_worldpop_overlay": OUTPUTS / "figures/worldpop_2019_ppp_overlay.png",

    # Processed outputs
    "worldpop_3857": OUTPUTS / "worldpop/worldpop_2019_ppp_3857.tif",

    # Hero figure
    "hero_png": OUTPUTS / "figures/ceam_sundarbans_admin_hero.png",

    # OSM outputs
    "outputs_osm": OUTPUTS / "osm",

    # Admin dir
    "admin_dir": OUTPUTS / "admin",

    # NTL Data
    "ntl_201806_rad": DATA / "ntl" / "raw" / "201806" /
    "SVDNB_npp_20180601-20180630_75N060E_vcmcfg_v10_c201904251200.avg_rade9h.tif",

    "ntl_201806_cvg": DATA / "ntl" / "raw" / "201806" /
    "SVDNB_npp_20180601-20180630_75N060E_vcmcfg_v10_c201904251200.cf_cvg.tif",

    "ntl_201904_rad": DATA / "ntl" / "raw" / "201904" /
    "SVDNB_npp_20190401-20190430_75N060E_vcmcfg_v10_c201905191000.avg_rade9h.tif",

    "ntl_201904_cvg": DATA / "ntl" / "raw" / "201904" /
    "SVDNB_npp_20190401-20190430_75N060E_vcmcfg_v10_c201905191000.cf_cvg.tif",


}