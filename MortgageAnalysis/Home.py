import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Australian Property Analyzer! 👋")

st.sidebar.success("Select an app from the above")

st.markdown(
    """

    - Investment Property Analyzer (New Property) --> Given a postcode and various other filters 
        you can project future growth and returns on property
    - Best Postcode by Gross Rental Yield --> With real sale price and weekly rentals ranks the postcodes by rent/price ratio
"""
)

if st.button("Best Postcodes Gross Rental Yield"):
    st.switch_page("pages/Best Postcodes Gross Rental Yield.py")
if st.button("Investment Property Analyzer (New Property)"):
    st.switch_page("pages/Investment Property Analyzer (New Property).py")