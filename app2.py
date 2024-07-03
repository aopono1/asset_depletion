import matplotlib
matplotlib.use('Agg')
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import io

def calculate_asset_depletion(a, b, c, pre_retirement_expenses, retirement_expenses_percentage, e, f, g, h, transactions):
    current_age = a
    retirement_age = b
    current_assets = c
    inflation_rate = e
    annual_return_rate = f
    pension_start_age = g
    monthly_pension = h
    current_year = 2024
    
    annual_pre_retirement_expenses = pre_retirement_expenses * 12
    annual_pension = monthly_pension * 12
    
    asset_history = []
    adjusted_retirement_expenses = None
    
    while current_assets > 0:
        if current_age < retirement_age:
            annual_expenses_adjusted = 0
            monthly_expenses_adjusted = 0
        elif current_age < pension_start_age:
            annual_expenses_adjusted = annual_pre_retirement_expenses * ((1 + inflation_rate) ** (current_age - a))
            monthly_expenses_adjusted = annual_expenses_adjusted / 12
        else:
            if current_age == pension_start_age:
                last_year_expenses = annual_pre_retirement_expenses * ((1 + inflation_rate) ** (pension_start_age - a - 1))
                adjusted_retirement_expenses = last_year_expenses * retirement_expenses_percentage
            annual_expenses_adjusted = adjusted_retirement_expenses * ((1 + inflation_rate) ** (current_age - pension_start_age))
            monthly_expenses_adjusted = annual_expenses_adjusted / 12
        
        annual_other_transactions = sum(amount for (amount, age) in transactions if age == current_age)
        
        asset_history.append((current_year, current_age, current_assets, monthly_expenses_adjusted))
        
        if current_age >= pension_start_age:
            current_assets = current_assets * (1 + annual_return_rate) - annual_expenses_adjusted + annual_pension + annual_other_transactions
        else:
            current_assets = current_assets * (1 + annual_return_rate) - annual_expenses_adjusted + annual_other_transactions
        
        if current_assets <= 0:
            return current_age, asset_history
        
        current_age += 1
        current_year += 1
    
    return None, asset_history

def plot_asset_history(asset_history):
    years = [entry[0] for entry in asset_history]
    assets = [entry[2] for entry in asset_history]
    
    fig, ax = plt.subplots()
    ax.plot(years, assets, label='Asset Value Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Assets')
    ax.legend()
    
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
    
    return fig

# Streamlitコード：入力を収集し、結果を表示
st.title('資産枯渇計算機')

a = st.sidebar.number_input('現在の年齢', min_value=0, value=40)
b = st.sidebar.number_input('退職年齢', min_value=a, max_value=100, value=65)
c = st.sidebar.number_input('現在の資産', min_value=0, value=5000000)
pre_retirement_expenses = st.sidebar.number_input('退職前の月間費用', min_value=0, value=300000)
retirement_expenses_percentage = st.sidebar.slider('退職後の費用（退職前の%）', 
                                                   min_value=0, max_value=200, value=90, step=1, 
                                                   format='%d%%') / 100
e = st.sidebar.slider('インフレ率', 
                      min_value=0.0, max_value=10.0, value=2.0, step=0.1, 
                      format='%.1f%%') / 100
f = st.sidebar.slider('年利', 
                      min_value=0.0, max_value=10.0, value=2.0, step=0.1, 
                      format='%.1f%%') / 100
g = st.sidebar.number_input('年金開始年齢', min_value=b, max_value=100, value=70)
h = st.sidebar.number_input('月間年金額', min_value=0, value=150000)

st.sidebar.subheader('その他の取引')
num_transactions = st.sidebar.number_input('その他の取引の数', min_value=0, max_value=10, value=0)
transactions = []
for i in range(num_transactions):
    col1, col2 = st.sidebar.columns(2)
    amount = col1.number_input(f'取引{i+1}の金額', value=0)
    age = col2.number_input(f'取引{i+1}の年齢', min_value=a, max_value=100, value=a)
    transactions.append((amount, age))

if st.sidebar.button('計算'):
    depletion_age, asset_history = calculate_asset_depletion(a, b, c, pre_retirement_expenses, retirement_expenses_percentage, e, f, g, h, transactions)
    
    if depletion_age:
        st.write(f"資産が枯渇する年齢: {depletion_age}")
    else:
        st.write("計算期間内に資産は枯渇しません。")
    
    fig = plot_asset_history(asset_history)
    st.pyplot(fig, use_container_width=True)
    
    st.subheader('資産履歴')
    for year, age, assets, monthly_expenses in asset_history:
        st.write(f"年: {year}, 年齢: {age}, 資産: {assets:.2f}, 月間費用: {monthly_expenses:.2f}")
