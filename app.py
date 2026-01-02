import streamlit as st
import ee
import json
import geemap.foliumap as geemap
from google.oauth2 import service_account
from datetime import datetime
import pandas as pd

# ============================================================
# 1. Page Configuration
# ============================================================
st.set_page_config(
    layout="wide",
    page_title="Jordan Air Quality Tracker"
)

# ============================================================
# 2. Google Earth Engine Authentication
# ============================================================
def authenticate_gee():
    """Authenticate Google Earth Engine using Streamlit Secrets"""
    if "GEE_JSON" in st.secrets:
        try:
            info = json.loads(st.secrets["GEE_JSON"])
            scopes = ["https://www.googleapis.com/auth/earthengine"]
            credentials = service_account.Credentials.from_service_account_info(
                info, scopes=scopes
            )
            ee.Initialize(credentials=credentials)
            return True
        except Exception as e:
            st.error(f"❌ GEE Authentication Failed: {e}")
            return False
    return False

# ============================================================
# 3. App Title
# ============================================================
st.title("🌫️ Jordan Air Quality Monitoring System")
st.markdown("### Sentinel-5P TROPOMI Satellite Analysis")

st.sidebar.header("📊 Settings & Parameters")

# ============================================================
# 4. Main App Logic
# ============================================================
if authenticate_gee():

    # Jordan center
    jordan_center = [31.2, 36.5]

    # --------------------------------------------------------
    # Pollutant Selection
    # --------------------------------------------------------
    pollutant = st.sidebar.selectbox(
        "Select Air Pollutant",
        [
            "Nitrogen Dioxide (NO2)",
            "Sulfur Dioxide (SO2)",
            "Carbon Monoxide (CO)",
            "Aerosol Index (Dust/Smoke)"
        ]
    )

    # --------------------------------------------------------
    # Temporal Selection
    # --------------------------------------------------------
    st.sidebar.subheader("📅 Temporal Filter")
    year = st.sidebar.slider("Select Year", 2019, 2025, 2024)
    month = st.sidebar.select_slider(
        "Select Month",
        options=list(range(1, 13)),
        format_func=lambda x: datetime(2000, x, 1).strftime('%B')
    )

    # --------------------------------------------------------
    # Pollutant Configurations
    # --------------------------------------------------------
    gas_configs = {
        "Nitrogen Dioxide (NO2)": {
            "collection": "COPERNICUS/S5P/OFFL/L3_NO2",
            "band": "tropospheric_NO2_column_number_density",
            "min": 0,
            "max": 0.0002,
            "palette": ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
            "unit": "mol/m²"
        },
        "Sulfur Dioxide (SO2)": {
            "collection": "COPERNICUS/S5P/OFFL/L3_SO2",
            "band": "SO2_column_number_density",
            "min": 0,
            "max": 0.0005,
            "palette": ['blue', 'green', 'yellow', 'orange', 'red'],
            "unit": "mol/m²"
        },
        "Carbon Monoxide (CO)": {
            "collection": "COPERNICUS/S5P/OFFL/L3_CO",
            "band": "CO_column_number_density",
            "min": 0,
            "max": 0.05,
            "palette": ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
            "unit": "mol/m²"
        },
        "Aerosol Index (Dust/Smoke)": {
            "collection": "COPERNICUS/S5P/OFFL/L3_AER_AI",
            "band": "absorbing_aerosol_index",
            "min": -1,
            "max": 2,
            "palette": ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
            "unit": "Index"
        }
    }

    config = gas_configs[pollutant]

    # --------------------------------------------------------
    # Date Handling
    # --------------------------------------------------------
    start_date = f"{year}-{month:02d}-01"
    if month < 12:
        end_date = f"{year}-{month+1:02d}-01"
    else:
        end_date = f"{year+1}-01-01"

    # --------------------------------------------------------
    # Jordan Boundary
    # --------------------------------------------------------
    jordan_boundary = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017") \
        .filter(ee.Filter.eq("country_na", "Jordan"))

    # --------------------------------------------------------
    # Satellite Data Processing
    # --------------------------------------------------------
    image = (
        ee.ImageCollection(config["collection"])
        .filterDate(start_date, end_date)
        .select(config["band"])
        .mean()
        .clip(jordan_boundary)
    )

    # ========================================================
    # 5. Dashboard Metrics
    # ========================================================
    col1, col2, col3 = st.columns(3)
    col1.metric("Pollutant", pollutant.split(" ")[0])
    col2.metric("Year", year)
    col3.metric("Month", datetime(2000, month, 1).strftime('%B'))

    # ========================================================
    # 6. Map Visualization
    # ========================================================
    m = geemap.Map(center=jordan_center, zoom=7)
    m.add_basemap("HYBRID")

    vis_params = {
        "min": config["min"],
        "max": config["max"],
        "palette": config["palette"]
    }

    m.addLayer(jordan_boundary, {"color": "white"}, "Jordan Boundary")
    m.addLayer(image, vis_params, pollutant)
    m.add_colorbar(vis_params=vis_params, label=f"Concentration ({config['unit']})")

    m.to_streamlit(height=600)

    # ========================================================
    # 7. City-Based Statistics
    # ========================================================
    st.markdown("---")
    st.subheader("📥 City-Based Statistical Report")

    if st.button("Generate Statistical Report"):
        with st.spinner("Processing Sentinel-5P data..."):

            locations = {
                "Irbid": [32.55, 35.85],
                "Amman": [31.95, 35.92],
                "Zarqa": [32.06, 36.10],
                "Aqaba": [29.53, 35.00],
                "Mafraq": [32.34, 36.24]
            }

            results = []

            for city, coords in locations.items():
                geom = ee.Geometry.Point(coords)
                val = image.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=geom,
                    scale=7000,
                    maxPixels=1e9
                ).getInfo()

                results.append({
                    "City": city,
                    "Pollutant": pollutant,
                    "Value": val.get(config["band"]),
                    "Unit": config["unit"],
                    "Date": f"{year}-{month:02d}"
                })

            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)

            safe_name = pollutant.split(" ")[0]
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download CSV Report",
                data=csv,
                file_name=f"Jordan_AirQuality_{safe_name}_{year}_{month}.csv",
                mime="text/csv"
            )

    # ========================================================
    # 8. Scientific Insights
    # ========================================================
    st.markdown("---")
    st.subheader("💡 Scientific Interpretation")

    if pollutant.startswith("Nitrogen"):
        st.info("🚗 **NO₂** mainly originates from traffic and fossil fuel combustion.")
    elif pollutant.startswith("Sulfur"):
        st.info("🏭 **SO₂** indicates industrial emissions and power generation.")
    elif pollutant.startswith("Carbon"):
        st.info("🔥 **CO** is linked to incomplete combustion in urban areas.")
    elif pollutant.startswith("Aerosol"):
        st.info("🏜️ **Aerosol Index** highlights dust storms and smoke transport.")

else:
    st.warning("⚠️ Google Earth Engine authentication is required. Check Streamlit secrets.")