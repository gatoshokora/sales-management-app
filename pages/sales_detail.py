import streamlit as st
import database
import pandas as pd


@st.dialog("会計の削除")
def delete_dialog():
  st.write("本当にこの会計を削除しますか？")

  if st.button("削除"):
    database.delete_payment(st.session_state.payment_id)
    st.session_state.pop("payment_id", None)
    st.session_state.page = "home"
    st.rerun()

  if st.button("キャンセル"):
    st.rerun()

def show():
  st.title("会計詳細")

  data = (database.get_sales_data(st.session_state.payment_id))

  sales_data = []
  total_price = 0
  for product_data in data:
    total = product_data[3] * product_data[4]
    products = f"{product_data[2]}x{product_data[3]}"
    sales_data.append([products, f"{total}円"])
    total_price += total

  st.write("")
  col1, col2 = st.columns([1,3])

  with col1:
    st.write("時刻")

  with col2:
    st.write(data[0][1])

  df = pd.DataFrame(
    sales_data,
    columns=["商品x個数", "金額"]
  )

  st.dataframe(
    df[["商品x個数", "金額"]],
    hide_index=True
  )

  st.divider()

  st.write("合計")

  st.write(f"{total_price}円")

  if st.button("編集"):
    st.session_state.page = "sales_detail_edit"
    st.rerun()

  if st.button("削除"):
    delete_dialog()

  if st.button("戻る"):
    st.session_state.page = "sales_list"
    st.rerun()
