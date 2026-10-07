import streamlit as st
from datetime import date
import database
import pandas as pd

def show():
  st.title("【商品ごとの売り上げ】")

  col1, col2 = st.columns([1,3])

  with col1:
    st.markdown(
      "<div style='padding-top: 8px;'>期間：</div>",
      unsafe_allow_html=True
    )
    #unsafe_allow_html=True markdownの中にhtmlを使うことを許可する
    

  with col2:
    start_date = date(2026, 9, 1)
    today = date.today()
    current_date = start_date

    dates = []
    
    while current_date <= today:
      if current_date.month == 12:
        dates.append(current_date)
        current_date = date(
          current_date.year + 1,
          1,
          1
        )
        
      else:
        dates.append(current_date)
        current_date = date(
          current_date.year,
          current_date.month + 1,
          1
        )
    
    select_date = st.selectbox(
      "",
      dates,
      index=len(dates)-1,
      format_func= lambda x: x.strftime("%Y年%m月"),
      label_visibility="collapsed"
    )
    #label_visibility="collapsed" 空ラベルの余白をなくす

  select_date = select_date.strftime("%Y-%m")

  data = database.get_monthly_sales_data(select_date)

  df = pd.DataFrame(
    data,
    columns=["商品名", "売上個数", "売上金額"]
  )

  st.table(df)
  # print(select_date)
  if st.button("戻る"):
    st.session_state.page = "sales_analysis"
    st.rerun()
