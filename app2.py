import matplotlib
matplotlib.use('Agg')

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def calculate_asset_depletion(a, b, c, pre_retirement_expenses, retirement_expenses_percentage, e, f, g, h, i, j, k, m, transactions):
    # この関数の内容は前回と同じです
    # ...

def plot_asset_history(asset_history):
    years = [entry[0] for entry in asset_history]
    assets = [entry[2] for entry in asset_history]
    expenses = [entry[3] for entry in asset_history]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 資産のプロット
    ax1.plot(years, assets, 'b-', label='資産')
    ax1.set_xlabel('年')
    ax1.set_ylabel('資産 (円)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # 金額を日本円表示にフォーマット
    def millions(x, pos):
        return f'{x*1e-6:.0f}M'
    
    formatter = FuncFormatter(millions)
    ax1.yaxis.set_major_formatter(formatter)

    # 支出のプロット
    ax2 = ax1.twinx()
    ax2.plot(years, expenses, 'r-', label='月間支出')
    ax2.set_ylabel('月間支出 (円)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.yaxis.set_major_formatter(formatter)

    # 凡例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('資産と月間支出の推移')
    plt.grid(True)

    return fig

st.title('資産寿命シミュレーション')

# サイドバーの入力項目は前回と同じです
# ...

if st.sidebar.button('計算'):
    depletion_age, asset_history = calculate_asset_depletion(a, b, c, pre_retirement_expenses, retirement_expenses_percentage, e, f, g, h, i, j, k, m, transactions)
    
    if depletion_age is not None:
        years = int(depletion_age)
        months = int((depletion_age - years) * 12)
        st.write(f"資産が枯渇する年齢: {years}歳{months}ヶ月目")
    else:
        st.write("計算期間内で資産は枯渇しません。")
    
    fig = plot_asset_history(asset_history)
    st.pyplot(fig, use_container_width=True)
    
    st.subheader('資産履歴')
    for index, (year, age, assets, monthly_expenses) in enumerate(asset_history):
        years = int(age)
        months = int((age - years) * 12)
        
        if index == len(asset_history) - 1 and depletion_age is not None:
            # 資産が枯渇する最後の行
            st.write(f"年: {year}, 年齢: {years}歳{months}ヶ月目, 資産: {int(assets):,}円, 月間支出: {int(monthly_expenses):,}円")
        else:
            # その他の行（月の表示を省略）
            st.write(f"年: {year}, 年齢: {years}歳, 資産: {int(assets):,}円, 月間支出: {int(monthly_expenses):,}円")
