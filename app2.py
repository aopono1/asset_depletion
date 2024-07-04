# 修正点1: Matplotlibのバックエンドを設定
import matplotlib
matplotlib.use('Agg')

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
        # 現在の生活費を計算
        if current_age < retirement_age:
            annual_expenses_adjusted = annual_pre_retirement_expenses * ((1 + inflation_rate) ** (current_age - a))
        elif current_age < pension_start_age:
            annual_expenses_adjusted = annual_pre_retirement_expenses * ((1 + inflation_rate) ** (current_age - a))
        else:
            if current_age == pension_start_age:
                last_year_expenses = annual_pre_retirement_expenses * ((1 + inflation_rate) ** (pension_start_age - a - 1))
                adjusted_retirement_expenses = last_year_expenses * retirement_expenses_percentage
            annual_expenses_adjusted = adjusted_retirement_expenses * ((1 + inflation_rate) ** (current_age - pension_start_age))
        
        monthly_expenses_adjusted = annual_expenses_adjusted / 12
        
        annual_other_transactions = sum(amount for (amount, age) in transactions if age == current_age)
        
        asset_history.append((current_year, current_age, current_assets, monthly_expenses_adjusted))
        
        if current_age >= retirement_age:
            if current_age >= pension_start_age:
                current_assets = current_assets * (1 + annual_return_rate) - annual_expenses_adjusted + annual_pension + annual_other_transactions
            else:
                current_assets = current_assets * (1 + annual_return_rate) - annual_expenses_adjusted + annual_other_transactions
        else:
            current_assets = current_assets * (1 + annual_return_rate) + annual_other_transactions
        
        if current_assets <= 0:
            asset_history.append((current_year, current_age, current_assets, monthly_expenses_adjusted))
            return current_age, asset_history
        
        current_age += 1
        current_year += 1
    
    return None, asset_history

def plot_asset_history(asset_history):
    years = [entry[0] for entry in asset_history]
    ages = [entry[1] for entry in asset_history]
    assets = [entry[2] for entry in asset_history]
    monthly_expenses = [entry[3] for entry in asset_history]

    def format_func(value, tick_number):
        return f'{int(value / 10000)}'

    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Assets (in ten-thousand units)', color=color)
    ax1.plot(ages, assets, marker='o', color=color, label='Assets')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_func))

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Monthly Expenses (in ten-thousand units)', color=color)
    ax2.plot(ages, monthly_expenses, marker='s', color=color, label='Monthly Expenses')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.yaxis.set_major_formatter(FuncFormatter(format_func))

    plt.title('Asset Depletion and Monthly Expenses Over Time')
    plt.grid(True)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, ['Assets', 'Monthly Expenses'], loc='upper right')

    # 修正点2: 現在のfigureを取得し、クリア
    fig = plt.gcf()
    plt.close(fig)

    return fig

st.title('資産寿命シミュレーション')

st.sidebar.header('入力項目')
a = st.sidebar.number_input('現在の年齢', min_value=0, max_value=100, value=30)
b = st.sidebar.number_input('退職時の年齢', min_value=0, max_value=100, value=65)
c = st.sidebar.number_input('保有している金融資産', min_value=0, value=10000000)
pre_retirement_expenses = st.sidebar.number_input('毎月の生活費', min_value=0, value=250000)

retirement_expenses_percentage = st.sidebar.slider('年金受給開始後の生活費 (年金受給前の毎月の生活費に対する割合％)', 
                                                   min_value=0, max_value=200, value=90, step=1, 
                                                   format='%d%%') / 100

e = st.sidebar.slider('インフレ率', 
                      min_value=0.0, max_value=10.0, value=2.0, step=0.1, 
                      format='%.1f%%') / 100

f = st.sidebar.slider('金融資産の運用利回り率', 
                      min_value=0.0, max_value=10.0, value=2.0, step=0.1, 
                      format='%.1f%%') / 100

g = st.sidebar.number_input('年金受給開始年齢', min_value=b, max_value=100, value=65)
h = st.sidebar.number_input('毎月の年金受給額', min_value=0, value=200000)

st.sidebar.subheader('他の入出金イベント')
num_transactions = st.sidebar.number_input('入出金イベントの回数', min_value=0, max_value=10, value=0)
transactions = []
for i in range(num_transactions):
    col1, col2 = st.sidebar.columns(2)
    amount = col1.number_input(f'Amount for Transaction {i+1}', value=0)
    age = col2.number_input(f'Age for Transaction {i+1}', min_value=a, max_value=100, value=a)
    transactions.append((amount, age))

if st.sidebar.button('Calculate'):
    depletion_age, asset_history = calculate_asset_depletion(a, b, c, pre_retirement_expenses, retirement_expenses_percentage, e, f, g, h, transactions)
    
    if depletion_age:
        st.write(f"資産が枯渇する年齢: {depletion_age}歳")
    else:
        st.write("シミュレーションの期間内では資産は枯渇しません")
    
    fig = plot_asset_history(asset_history)
    # 修正点3: use_container_width=Trueを追加
    st.pyplot(fig, use_container_width=True)
    
    st.subheader('金融資産と毎月の生活費の推移')
    for year, age, assets, monthly_expenses in asset_history:
        st.write(f"西暦: {year}, 年齢: {age}, 金融資産: {assets:.2f}, 毎月の生活費: {monthly_expenses:.2f}")
