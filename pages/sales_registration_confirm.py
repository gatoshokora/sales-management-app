import streamlit as st
import database
import pandas as pd
from datetime import datetime

def show():
  st.title("売り上げ確認")

  st.write("【会計内容の確認】")
  df = pd.DataFrame(
      st.session_state.display_data,
      columns=["商品名", "個数", "販売価格"]
    )

  st.table(df)

  st.divider()

  total = 0
  for select_data in st.session_state.select_data:
    total += select_data[2] * select_data[3]

  st.write("合計")

  st.write(f"{total}円")

  st.divider()

  if st.button("確定"):
    now = datetime.now()
    payment_id = database.add_payment(now)
    for select_data in st.session_state.select_data:   
      database.add_sales_detail(payment_id, select_data[0], select_data[2], select_data[3])

    st.session_state.pop("select_data", None)
    st.session_state.pop("display_data", None)
    st.session_state.page = "home"
    st.rerun()

  if st.button("戻る"):
    st.session_state.page = "sales_registration"
    st.rerun()

