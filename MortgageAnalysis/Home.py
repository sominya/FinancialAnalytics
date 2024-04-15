import streamlit as st

st.set_page_config(
    page_title="Australian Property Analyzer",
    #page_icon="👋",
    page_icon="🏠"
)

st.write("# Welcome to Australian Property Analyzer! 👋")

st.sidebar.success("Select an app from the above")

st.markdown(
    """
    - <h3 style='text-align: Left; color: green;'>Investment Property Analyzer (New Property) </h3>
       Given a postcode and various other filters  you can project future growth and returns on property
    - <h3 style='text-align: Left; color: green;'> Compare returns of different postcodes </h3>
       Key metrics on postcodes
    - <h3 style='text-align: Left; color: green;'> Best Postcode by Gross Rental Yield </h3>
       With real sale price and weekly rentals ranks the postcodes by rent/price ratio
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .my_button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

if st.button(":green[Best Postcodes Gross Rental Yield]"):
    st.switch_page("pages/Best Postcodes Gross Rental Yield.py")
if st.button(":green[Compare Postcodes]"):
    st.switch_page("pages/Compare Postcodes.py")
if st.button(":green[Investment Property Analyzer (New Property)]"):
    st.switch_page("pages/Investment Property Analyzer (New Property).py")