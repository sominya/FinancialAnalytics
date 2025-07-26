import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils import (simulate_super_growth, format_currency)
import streamlit as st
from datetime import datetime
import locale

super_return_rate = st.sidebar.slider('Super Return Rate (%)', 0.0, 10.0, 5.0, step=0.1)
super_initial_investment = st.sidebar.slider('Super Initial Balance', 0, 300000, 30000, step=1000)
monthly_contribution = st.sidebar.slider('Monthly Contribution', 0, 5000, 500, step=100)
period_years = st.sidebar.slider('Investment Period (Years)', 1, 30, 10, step=1)
start_date = st.sidebar.date_input('Start Date', datetime.now())

df = simulate_super_growth(start_date, super_initial_investment , super_return_rate/100, monthly_contribution, months=period_years * 12)
c1,c2,c3 = st.columns(3)
c1.metric("Initital Super Balance", format_currency(super_initial_investment))
c2.metric('Monthly Contributions', f"{monthly_contribution:.2f}")
c3.metric("Period", str(period_years)+ " years")
c4 = st.columns(1)[0]
c4.metric("Total Balance", format_currency(df['Total_Super'].max()))
st.line_chart(df.set_index('Date')['Total_Super'])