import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils import get_best_postcodes_rent_yields, get_aus_postcodes, get_rental_data
import streamlit as st
import folium
from streamlit_folium import st_folium


st.set_page_config(layout="wide")
st.write("Copyright © 2024 Sominya Bajpai , Only meant for personal use")
# Streamlit app
st.title('Best Postcodes (Gross rental yield)')
states = list(get_aus_postcodes()['state_code'].unique()) + ['All Australia']
house_types = list(get_rental_data()['Type'].unique())
minimum_price = st.sidebar.slider('Minimum House Price', min_value=100000, max_value=10000000, value=500000)
selected_state = st.sidebar.selectbox('Select State', states, index=states.index('All Australia'))
selected_house_type = st.sidebar.selectbox('Select Dwelling Type', house_types, index=house_types.index('Combined'))
select_rank = st.sidebar.slider('Select Top N Postcodes', min_value=10, max_value=100, value=20)

df = get_best_postcodes_rent_yields(house_type=selected_house_type, state=selected_state, rank=select_rank, house_price=(minimum_price/1000))

display_df = df.drop(columns=['latitude', 'longitude'])
formatted_df = display_df.style.format({'Asking Price in $k': '{:.2f}', 'Weekly Rent': '{:.0f}', 'Rent To Price Ratio': '{:.2f}'})
# html = formatted_df.to_html(index=False)
# st.write(html, unsafe_allow_html=True)
st.table(formatted_df)
# st.map(df, latitude='latitude', longitude='longitude', size='Size')

# Create a Folium map centered at a specific location
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)

# Add markers to the map
for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], tooltip=[row['place_name'], row['Postcode'], row['Rent To Price Ratio']]).add_to(m)

# Display the map using st.write
st_map = st_folium(m, width=1000, height=600)