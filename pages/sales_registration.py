import streamlit as st
import database
import pandas as pd

def show():
  st.title("売り上げ登録")

  data = database.get_product_data()

  product_name = []
  for product_data in data:
    product_name.append(product_data[1])

  select_name = st.selectbox("【商品名】", product_name)

  count = st.number_input("【個数】", min_value=1)

  for product_data in data:
    if select_name == product_data[1]:
      sales_price = product_data[3]
      sales_id = product_data[0]

  st.write("【販売価格】")
  st.write(f"{sales_price}円")
  

  if "select_data" not in st.session_state:
    st.session_state.select_data = []

  if st.button("商品を追加"):
    st.session_state.select_data.append([sales_id, select_name, count, sales_price])

  display_data = []
  if st.session_state.select_data:

    for data in st.session_state.select_data:
      display_data.append([data[1], f"x{data[2]}", f"{data[3]}円"])

    df = pd.DataFrame(
      display_data,
      columns=["商品名", "個数", "販売価格"]
    )

    st.table(df)
  st.session_state.display_data = display_data
  
  if st.button("確認"):
    if st.session_state.select_data:
      st.session_state.page = "sales_registration_confirm"
      st.rerun()

    else:
      st.error("売り上げ商品が選択されていません。")

  if st.button("戻る"):
    st.session_state.pop("select_data", None)
    st.session_state.pop("display_data", None)
    st.session_state.page = "home"
    st.rerun()