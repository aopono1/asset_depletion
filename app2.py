import matplotlib
matplotlib.use('Agg')

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# calculate_asset_depletion function remains the same
# ...

def plot_asset_history(asset_history):
    years = [entry[0] for entry in asset_history]
    assets = [entry[2] for entry in asset_history]
    expenses = [entry[3] for entry in asset_history]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot assets
    ax1.plot(years, assets, 'b-', label='Assets')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Assets (10,000 JPY)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Format currency in 10,000 JPY
    def ten_thousands(x, pos):
        return f'{x*1e-4:.0f}'
    
    formatter = FuncFormatter(ten_thousands)
    ax1.yaxis.set_major_formatter(formatter)

    # Plot expenses
    ax2 = ax1.twinx()
    ax2.plot(years, expenses, 'r-', label='Monthly Expenses')
    ax2.set_ylabel('Monthly Expenses (10,000 JPY)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.yaxis.set_major_formatter(formatter)

    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('Asset and Monthly Expense Projection')
    plt.grid(True)

    return fig

st.title('Asset Depletion Simulation')

# Sidebar inputs (translated to English)
st.sidebar.header('Input Parameters')
a = st.sidebar.number_input('Current Age', min_value=0, max_value=100, value=30)
b = st.sidebar.number_input('Retirement Age', min_value=0, max_value=100, value=65)
c = st.sidebar.number_input('Current Financial Assets', min_value=0, value=10000000)
pre_retirement_expenses = st.sidebar.number_input('Monthly Living Expenses', min_value=0, value=250000)

retirement_expenses_percentage = st.sidebar.slider('Post-retirement Living Expenses (% of pre-retirement)', 
                                                   min_value=0, max_value=200, value=90, step=1, 
                                                   format='%d%%') / 100

e = st.sidebar.slider('Inflation Rate', 
                      min_value=0.0, max_value=10.0, value=2.0, step=0.1, 
                      format='%.1f%%') / 100

f = st.sidebar.slider('Real Rate of Return on Financial Assets', 
                      min_value=0.0, max_value=10.0, value=2.0, step=0.1, 
                      format='%.1f%%') / 100

g = st.sidebar.number_input('Age to Start Receiving Pension', min_value=b, max_value=100, value=65)
h = st.sidebar.number_input('Monthly Pension Amount', min_value=0, value=200000)

i = st.sidebar.number_input('Monthly Savings Before Retirement', min_value=0, value=50000)
j = st.sidebar.number_input('Monthly Savings After Retirement', min_value=0, value=0)
k = st.sidebar.number_input('Age to Stop Saving', min_value=a, max_value=100, value=65)
m = st.sidebar.number_input('Additional Monthly Income After Retirement', min_value=0, value=0)

st.sidebar.subheader('Other Income/Expense Events')
num_transactions = st.sidebar.number_input('Number of Events', min_value=0, max_value=10, value=0)
transactions = []
for n in range(num_transactions):
    col1, col2 = st.sidebar.columns(2)
    amount = col1.number_input(f'Amount for Event {n+1}', value=0)
    age = col2.number_input(f'Age for Event {n+1}', min_value=a, max_value=100, value=a)
    transactions.append((amount, age))

if st.sidebar.button('Calculate'):
    depletion_age, asset_history = calculate_asset_depletion(a, b, c, pre_retirement_expenses, retirement_expenses_percentage, e, f, g, h, i, j, k, m, transactions)
    
    if depletion_age is not None:
        years = int(depletion_age)
        months = int((depletion_age - years) * 12)
        st.write(f"Assets will be depleted at age: {years} years and {months} months")
    else:
        st.write("Assets will not be depleted within the calculated period.")
    
    fig = plot_asset_history(asset_history)
    st.pyplot(fig, use_container_width=True)
    
    st.subheader('Asset History')
    for index, (year, age, assets, monthly_expenses) in enumerate(asset_history):
        years = int(age)
        months = int((age - years) * 12)
        
        if index == len(asset_history) - 1 and depletion_age is not None:
            # Last row when assets are depleted
            st.write(f"Year: {year}, Age: {years}y {months}m, Assets: {int(assets):,} JPY, Monthly Expenses: {int(monthly_expenses):,} JPY")
        else:
            # Other rows (omitting months display)
            st.write(f"Year: {year}, Age: {years}y, Assets: {int(assets):,} JPY, Monthly Expenses: {int(monthly_expenses):,} JPY")
