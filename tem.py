import streamlit as st

def redirect_to_street_view(lon, lat):
    url = f"https://www.gps-coordinates.net/street-view/@{lon},{lat},h237,p9,z1"
    st.markdown(f"[Open Street View]({url})")

# Example usage:
lon = 76.8
lat = 15.05
redirect_to_street_view(lon, lat)