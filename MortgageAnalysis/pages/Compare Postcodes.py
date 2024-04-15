import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils import get_postcode_metrics, get_aus_postcodes, get_rental_data
import streamlit as st
import folium
from streamlit_folium import st_folium


st.set_page_config(layout="wide")
st.write("Copyright © 2024 Sominya Bajpai , Only meant for personal use")
# Streamlit app
st.title('Compare Postcodes')
postcodes = list(get_aus_postcodes()['Postcode'].unique())
selected_postcodes = st.sidebar.multiselect('Select postcode(s):', postcodes, default=2000)
house_types = list(get_rental_data()['Type'].unique())
selected_house_type = st.sidebar.selectbox('Select Dwelling Type', house_types, index=house_types.index('Combined'))
if selected_postcodes:
    
    (metrics , suburbs)= get_postcode_metrics(postcodes = selected_postcodes, type=selected_house_type)
    metrics = metrics.sort_values(by='Rent To Price Ratio', ascending=False)
    # display_df = df.drop(columns=['latitude', 'longitude'])
    formatted_df = metrics.style.format({'Asking Price in $k': '{:.2f}', 'Weekly Rent': '{:.0f}', 'Rent To Price Ratio': '{:.2f}'})
    # html = formatted_df.to_html(index=False)
    # st.write(html, unsafe_allow_html=True)
    st.table(formatted_df)
    # st.map(df, latitude='latitude', longitude='longitude', size='Size')

    # Create a Folium map centered at a specific location
    m = folium.Map(location=[suburbs['latitude'].mean(), suburbs['longitude'].mean()], zoom_start=5)

    # Add markers to the map
    for index, row in suburbs.iterrows():
        folium.Marker([row['latitude'], row['longitude']], tooltip=[row['place_name'], row['Postcode'], row['Rent To Price Ratio']]).add_to(m)

    # Display the map using st.write
    st_map = st_folium(m, width=1000, height=600)