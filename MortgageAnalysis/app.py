import streamlit as st
import pandas as pd
from datetime import datetime
import locale

# Set the locale to use the user's default settings
locale.setlocale(locale.LC_ALL, '')
from utils import calculate_mortgage_payments, calculate_cagr

def format_currency(value):
    return "${:,.0f}".format(value)

# Function to generate DataFrame
def generate_df(down_payment, house_price, interest_rate, loan_term_years, weekly_rent, start_date):
    water = 40
    insurance = 200
    council_tax = 140
    # start_date = datetime(2024, 10, 1)  # Start date of loan
    df = calculate_mortgage_payments(down_payment, house_price, interest_rate, loan_term_years, start_date,
                                      council_tax, insurance, water, weekly_rent)
    return df

st.set_page_config(layout="wide")
st.markdown('<h3 style="text-align: center;">Copyright © 2024 Sominya Bajpai . All Rights Reserved.</h3>', unsafe_allow_html=True)
# Streamlit app
st.title('Mortgage Payments Calculator')


# Input widgets

down_payment = st.sidebar.slider('Down Payment (%)', 0, 100, 20)
house_price = st.sidebar.slider('House Price', 550000, 2500000, 650000, step=5000)
interest_rate = st.sidebar.slider('Interest Rate (%)', 1.0, 10.0, 6.2, step=0.1)
loan_term_years = st.sidebar.slider('Loan Term (Years)', 1, 30, 30, step=1)
weekly_rent = st.sidebar.slider('Initial Weekly Rent', 500, 1500, 580, step=20)
start_date = st.sidebar.date_input('Loan Start Date', datetime.now())

# Generate DataFrame based on input values
df = generate_df(down_payment, house_price, interest_rate, loan_term_years, weekly_rent, start_date)

(cash_after_tax, annualized_return, total_tax_paid, total_investment, rental_gains) = calculate_cagr(df, down_payment, house_price)
initial_inv = df['InitialInvestments'].max()
invest_while_rented = total_investment - initial_inv
# Display DataFrame
# st.write('Generated DataFrame:')
# st.write(df.head())
st.metric("Rental Gains over loan period", format_currency(rental_gains))
monthly_rental = format_currency(df['Payment Amount'].max())
col1, col2, col3= st.columns(3)
col1.metric("Monthly Payment", monthly_rental)
col2.metric("Initial Investments", format_currency(initial_inv))
col3.metric("Rental Losses", format_currency(invest_while_rented))
col4, col5, col6 = st.columns(3)
col4.metric("Cash at Sale (After Tax)", format_currency(cash_after_tax))
col5.metric("Total Investments(Initial+WhileRented)", format_currency(invest_while_rented+initial_inv))
col6.metric("Annualized Return", f"{annualized_return * 100:.2f}%")

profit_start_date = df[df["Losses"]>=0]["Date"].min()
st.subheader('It is worth noting that property starts making positive cashflow only from ' f"{profit_start_date}")
chart1, chart2 = st.columns(2)
# Generate graph for total_losses
with chart1:
    st.subheader('Cumulative (Cashflow In/Out)')
    st.line_chart(df.set_index('Date')['Losses'].cumsum())
with chart2:
    st.subheader('Monthly (Cashflow In/Out)')
    st.line_chart(df.set_index('Date')['Losses'])

st.subheader('Net of [Mortage Payment + Expense] - [Gross Rental Income] = Cashflow In/Out')
st.subheader('The Calculation makes following assumptions-')
st.markdown("""
- The body corporate fee is 0
- The house is based in Queensland Australia (Stamp Duty is Calculated based on QLD rules)
- The house price goes up by "6%" annually
- Council tax, rent payments go up by 5%, whereas all other costs go up by 1%
- The House is sold immediately after the loan term ends
- Captial Gains tax etc have been calculated
- Management fee is "8.25%" and tax deduction on negative gearing hasnt been accounted for
- Interest Rate stays consistent throughout the loan
""")

