import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(page_title="PVGIS TMY Data by KTSXM", layout="centered")

st.title("☀️ PVGIS TMY Data by KTSXM")
st.markdown("Get Typical Meteorological Year (TMY) data from PVGIS using latitude and longitude.")

lat = st.number_input("Enter Latitude", format="%.6f", value=12.9716)
lon = st.number_input("Enter Longitude", format="%.6f", value=77.5946)

if st.button("Fetch TMY Data"):
    with st.spinner("Fetching data from PVGIS..."):
        try:
            url = "https://re.jrc.ec.europa.eu/api/v5_3/tmy"
            params = {
                'lat': lat,
                'lon': lon,
                'outputformat': 'csv'
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                csv_text = response.text
                start_idx = csv_text.find("time(UTC)")
                csv_data = csv_text[start_idx:]
                df = pd.read_csv(StringIO(csv_data))

                st.success("Data fetched successfully!")
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "pvgis_tmy.csv", "text/csv")
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("Powered by PVGIS • Developed by XELION MARVEL & NOVA MARVEL")
