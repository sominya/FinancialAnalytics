import pandas as pd
from datetime import datetime, timedelta

def calculate_transfer_duty(purchase_price):
    '''
    Calculate the transfer duty for a given purchase price.

    Parameters:
        purchase_price (float): The purchase price of the property.

    Returns:
        float: The transfer duty amount.

    Notes:
        - The transfer duty is calculated for QLD Australia.
        - Government fees are set statically to 3000 as the formula is unknown.
        - If the purchase price is less than or equal to 0, an error message is returned.

    '''
    if purchase_price <= 0:
        return "Invalid purchase price. Please enter a positive value."

    # Define the transfer duty thresholds and rates
    thresholds = [5000, 75000, 540000, 1500000]
    rates = [1.50, 3.50, 4.50, 5.75, 7.00]
    flat_amounts = [75, 2625, 17325, 87075]

    # Initialize transfer duty
    transfer_duty = 0

    # Calculate transfer duty based on purchase price
    if purchase_price <= thresholds[0]:
        transfer_duty = purchase_price * rates[0] / 100
    elif purchase_price <= thresholds[1]:
        transfer_duty = flat_amounts[0] + (purchase_price - thresholds[0]) * rates[1] / 100
    elif purchase_price <= thresholds[2]:
        transfer_duty = flat_amounts[1] + (purchase_price - thresholds[1]) * rates[2] / 100
    elif purchase_price <= thresholds[3]:
        transfer_duty = flat_amounts[2] + (purchase_price - thresholds[2]) * rates[3] / 100
    else:
        transfer_duty = flat_amounts[3] + (purchase_price - thresholds[3]) * rates[4] / 100
    government_fees = 3000  # Setting a static value calculation is complex
    return transfer_duty+government_fees
def calculate_mortgage_payments(down_payment_pct, 
                                house_price, 
                                interest_rate, 
                                loan_term_years, 
                                start_date, 
                                council_tax,
                                insurance,
                                water,
                                weekly_rent,
                                rent_increase_yearly = 5, # Annual rent increase is 5 %
                                misc_expenses = 100,
                                management_fee = 8.25, # Agency fee is 8.25 %
                                body_corporate_fee = 0  # In case of town houses and apartments there is a body corporate fee
                                ):
    '''
Calculate mortgage payments for a given set of parameters.

Parameters:
    down_payment_pct (float): The percentage of the house price to be paid as a down payment.
    house_price (float): The total price of the house.
    interest_rate (float): The annual interest rate for the mortgage.
    loan_term_years (int): The number of years for the mortgage loan term.
    start_date (datetime): The start date of the mortgage payments.
    council_tax (float): The monthly council tax amount.
    insurance (float): The monthly insurance amount.
    water (float): The monthly water bill amount.
    weekly_rent (float): The weekly rent amount.
    rent_increase_yearly (float, optional): The annual percentage increase in rent. Defaults to 5.
    misc_expenses (float, optional): The monthly miscellaneous expenses. Defaults to 100.
    management_fee (float, optional): The percentage of the monthly rent to be paid as a management fee. Defaults to 8.25.
    body_corporate_fee (float, optional): The monthly body corporate fee for town houses and apartments. Defaults to 0.

Returns:
    DataFrame: A pandas DataFrame containing the mortgage payment details for each month.

Notes:
    - The mortgage payment is calculated using the formula for monthly mortgage payment.
    - The loan amount is calculated as the house price minus the down payment plus the stamp duty.
    - The stamp duty is calculated using the calculate_transfer_duty function.
    - The total number of payments is calculated as the loan term in years multiplied by 12.
    - The mortgage payments are calculated for each month starting from the start date.
    - The rent, council tax, body corporate fee, insurance, water, and miscellaneous expenses are increased annually.
    - The house price is increased by 3% annually.
    - The management fee is calculated as a percentage of the monthly rent.
    - The payment details include the date, payment amount, net income, principal, interest, total expenses, house price, and initial investments.

    '''
    down_payment = house_price*(down_payment_pct/100)
    # Calculate monthly interest rate
    monthly_interest_rate = interest_rate / 12 / 100
    stamp_duty = calculate_transfer_duty(house_price)
    loan_amount = house_price - down_payment  # USD
    # Calculate total number of payments
    total_payments = loan_term_years * 12

    # Calculate monthly payment using the formula for monthly mortgage payment
    # monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -total_payments)
    monthly_payment = calculate_monthly_repayment(loan_amount, interest_rate, loan_term_years)
    # Create date range for the mortgage payments
    dates = [start_date + timedelta(days=30 * i) for i in range(total_payments)]

    # Initialize lists to store payment details
    payment_amounts = []
    principals = []
    interests = []
    expenses_tax_deductible = []
    total_payments = []
    losses = []
    house_prices = []
    momthly_rents= []

    # Initialize loan balance and momthly rent
    loan_balance = loan_amount
    monthly_rent = (weekly_rent*52)/12
    
    # Calculate payment details for each month
    for payment_num, date in enumerate(dates, start=1):
        # Calculate interest for the month
        momthly_rents.append(monthly_rent)
        interest = loan_balance * monthly_interest_rate
        # Add the initial investments only to the first line
        if payment_num == 1:
            initial_investments = [down_payment+stamp_duty]
        else:
            initial_investments.append(0)
        # At the start of every new year increase rent, council tax, body corp fee, insurance, water and misc expenses
        # Also increase the house price by 3 %
        if payment_num>1 and payment_num % 12 == 1:
            monthly_rent = monthly_rent*((rent_increase_yearly/100)+1)
            council_tax = council_tax*1.05
            body_corporate_fee = body_corporate_fee*1.01
            insurance = insurance*1.05
            water = water*1.01
            misc_expenses = misc_expenses*1.01
            house_price = round(house_price*1.06,0)
            
        
        # Other Expenses
        fee = monthly_rent*(management_fee/100)
        extra_expense = fee+council_tax+body_corporate_fee+insurance+water+misc_expenses
        
        expense_tax_deductible = extra_expense + interest
        total_payment = extra_expense + monthly_payment
        
        total_payments.append(total_payment)
        
        # Calculate Income
        income = monthly_rent-total_payment
        # Calculate principal for the month
        principal = monthly_payment - interest

        # Update loan balance
        loan_balance -= principal

        # Append payment details to lists
        payment_amounts.append(monthly_payment)
        principals.append(principal)
        interests.append(interest)
        expenses_tax_deductible.append(expense_tax_deductible)
        losses.append(income)
        house_prices.append(house_price)
    # Create DataFrame with payment details
    payment_df = pd.DataFrame({
        'Date': dates,
        'Payment Amount': payment_amounts,
        'Rent': momthly_rents,
        'Losses': losses,
        'Principal': principals,
        'Interest': interests,
        'ExpenseTaxDeductible': expenses_tax_deductible,
        'TotalPayments': total_payments,
        'HousePrice':house_prices,
        'InitialInvestments':initial_investments
    })

    return payment_df

def calculate_cagr(df, down_payment_pct, house_purchase_price):
    '''
    Calculate the Compound Annual Growth Rate (CAGR) for a property investment.

    Parameters:
        df (pandas.DataFrame): The dataframe containing the property investment data.
        down_payment_pct (float): The percentage of the house purchase price used as the down payment.
        house_purchase_price (float): The purchase price of the property.

    Returns:
        tuple: A tuple containing the following values:
            - new_hp (float): The current value of the property after considering any losses and agency fees.
            - annualized_return (float): The annualized rate of return as a percentage.
            - cgt (float): The Capital Gains Tax amount.
            - total_investment (float): The total investment amount including down payment, stamp duty, and losses.

    Notes:
        - The CAGR is calculated based on the formula: ((Ending Value / Beginning Value) ^ (1 / Number of Years)) - 1.
        - The down payment is calculated as a percentage of the house purchase price.
        - The loan term is calculated based on the number of months in the dataframe divided by 12.
        - The agency fee is calculated as 2% of the current property value.
        - The stamp duty is calculated using the calculate_transfer_duty function.
        - The old_hp is set to the house purchase price.
        - The income is calculated as the cumulative sum of the NetIncome column in the dataframe.
        - The tax_on_income is calculated as 32.5% of the income.
        - The total_losses is calculated as the absolute sum of negative NetIncome values in the dataframe.
        - The total_investment is calculated as the sum of total_losses, down_payment, and stamp_duty.
        - The cgt is calculated using the calculate_cgt function.
        - The roi is calculated as ((new_hp - total_investment - cgt) + income) / total_investment - 1.
        - The cagr is calculated as ((roi / 100) + 1) ^ (1 / loan_term) - 1.
        - The annualized_return is calculated by multiplying cagr by 100.

    '''
    down_payment = (down_payment_pct/100)*house_purchase_price
    loan_term = len(df)/12
    new_hp = df['HousePrice'].max()
    agency_fee = new_hp*.02
    new_hp -= agency_fee
    stamp_duty = calculate_transfer_duty(house_purchase_price)
    old_hp = house_purchase_price
    income = round(df['Losses'].cumsum().iloc[-1],0)
    tax_on_income = income*.325
    income -= tax_on_income
    try:
        total_losses = abs(df[df['Losses']<=0]['Losses'].cumsum().iloc[-1])
    except:
        total_losses = 0
    try:
        rental_gains = abs(df[df['Losses']>=0]['Losses'].cumsum().iloc[-1])
    except:
        rental_gains = 0
    total_investment = round(total_losses + down_payment+ stamp_duty,0)
    cgt = calculate_cgt(new_hp, old_hp)

    roi = (((new_hp+rental_gains-total_investment-cgt)+income)/total_investment)-1
    cagr = ((roi / 100) + 1) ** (1/loan_term) - 1

    # Convert CAGR to percentage for display
    annualized_return = cagr * 100
    return (round(new_hp-cgt, 0) , round(annualized_return,4), cgt, total_investment, rental_gains)


def calculate_monthly_repayment(loan_amount, annual_interest_rate, loan_term_years):
    # Calculate monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12 / 100

    # Calculate number of monthly payments
    num_monthly_payments = loan_term_years * 12

    # Calculate monthly repayment using the formula
    monthly_repayment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_monthly_payments)

    return monthly_repayment

def calculate_cgt(new_hp, old_hp):
    '''
Calculate Capital Gains Tax

Parameters:
    new_hp (float): The current value of the property.
    old_hp (float): The original purchase price of the property.

Returns:
    float: The amount of Capital Gains Tax.

Notes:
    - The Capital Gains Tax is calculated based on the formula: (new_hp - old_hp) * tax_rate.
    - The tax_rate is determined based on the capital_gain amount.
    - If the capital_gain is greater than 180,001, the tax_rate is 45%.
    - If the capital_gain is between 135,001 and 180,000, the tax_rate is 37%.
    - If the capital_gain is between 45,001 and 135,000, the tax_rate is 30%.
    - If the capital_gain is between 18,201 and 45,000, the tax_rate is 16%.
    - If the capital_gain is less than or equal to 18,200, the tax_rate is 0%.

    '''
    capital_gain = (new_hp - old_hp)*.5
    if capital_gain>180001:
        tax = 51667 + ((capital_gain-180000)*.45)
    elif capital_gain>=135001 and capital_gain<=180000:
        tax = 31288 + ((capital_gain-135000)*.37)
    elif capital_gain>=45001 and capital_gain<=135000:
        tax = 4288 + ((capital_gain-45000)*.30)
    elif capital_gain>=18201 and capital_gain<=45000:
        tax = 0 + ((capital_gain-18200)*.16)
    else:
        tax=0
    return tax
def super_balance(initial_balance, term_years, annual_return_rate, monthly_payment):
    """
    Calculate the balance of a superannuation account over a given term.

    Parameters:
    - initial_balance (float): The initial balance of the account.
    - term_years (int): The number of years for the term.
    - annual_return_rate (float): The annual return rate as a decimal.
    - monthly_payment (float): The monthly payment amount.

    Returns:
    - df (pandas.DataFrame): A DataFrame containing the month and corresponding balance for each month in the term.

    Example:
    super_balance(10000, 10, 0.05, 500) returns a DataFrame with 120 rows, representing 10 years of monthly balances for an account with an initial balance of $10,000, an annual return rate of 5%, and a monthly payment of $500.

    Note:
    - The monthly return rate is calculated by converting the annual return rate to a monthly rate.
    - The balance is calculated by adding the monthly payment, applying monthly compound interest, and storing the balance for each month.
    - The DataFrame is created using the 'months' and 'balances' lists.
    """
    # Convert annual return rate to monthly rate
    monthly_return_rate = calculate_monthly_return_rate(annual_return_rate)
    
    # Calculate the number of months in the term
    term_months = term_years * 12
    
    # Initialize lists to store data
    months = []
    balances = []
    monthly_payments = [] 
    # Initialize the balance
    balance = initial_balance
    total_payment = 0
    # Loop through each month
    for month in range(1, term_months + 1):
        # Add the monthly payment to the balance
        balance += monthly_payment
        monthly_payments.append(monthly_payment)
        
        # Apply monthly compound interest
        balance *= (1 + monthly_return_rate)
        
        # Append the month and balance to the lists
        months.append(month)
        balances.append(balance)
        
    
    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'Month': months,
        'Balance': balances,
        'Payments': monthly_payments
    })
    
    return df

def calculate_monthly_return_rate(annual_return_rate):
    return (1 + annual_return_rate)**(1/12) - 1

def calculate_daily_return_rate(annual_return_rate):
    return (1 + annual_return_rate)**(1/365) - 1