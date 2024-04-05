import streamlit as st
import pandas as pd
from datetime import datetime
import locale

# Set the locale to use the user's default settings
locale.setlocale(locale.LC_ALL, '')
from utils import calculate_mortgage_payments, calculate_cagr


# Function to generate DataFrame
def generate_df(down_payment, house_price, interest_rate, loan_term_years, weekly_rent):
    water = 40
    insurance = 200
    council_tax = 140
    start_date = datetime(2024, 10, 1)  # Start date of loan
    df = calculate_mortgage_payments(down_payment, house_price, interest_rate, loan_term_years, start_date,
                                      council_tax, insurance, water, weekly_rent)
    return df

# Streamlit app
st.title('Mortgage Payments Calculator')

# Input widgets
down_payment = st.sidebar.slider('Down Payment (%)', 0, 100, 20)
house_price = st.sidebar.slider('House Price', 550000, 1500000, 650000, step=5000)
interest_rate = st.sidebar.slider('Interest Rate (%)', 1.0, 10.0, 5.0, step=0.1)
loan_term_years = st.sidebar.slider('Loan Term (Years)', 1, 30, 30, step=1)
weekly_rent = st.sidebar.slider('Initial Weekly Rent', 500, 900, 550, step=20)

# Generate DataFrame based on input values
df = generate_df(down_payment, house_price, interest_rate, loan_term_years, weekly_rent)

(cash_after_tax, annualized_return, total_tax_paid, total_investment) = calculate_cagr(df, down_payment, house_price)
initial_inv = df['InitialInvestments'].max()
invest_while_rented = total_investment - initial_inv
# Display DataFrame
# st.write('Generated DataFrame:')
# st.write(df.head())

# Generate graph for total_losses
st.subheader('Graph for Total Losses/Profits Over course of Mortgage')
st.line_chart(df.set_index('Date')['Losses'].cumsum())

st.write(f"**Monthly Payment: ${df['Payment Amount'].max():.2f}**")

st.write(f"**Total Investments (Includes Gains/Losses): ${initial_inv+invest_while_rented:.2f}**")
    
st.write(f"**Cash After Sale and Tax: ${cash_after_tax:.2f}**") 

st.write(f"**Annualized Return: {annualized_return*100:.2f}%**")

