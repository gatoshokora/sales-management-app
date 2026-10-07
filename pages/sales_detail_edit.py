import streamlit as st
import database

def show():
  st.title("会計編集")

  data = database.get_sales_data(st.session_state.payment_id)

  products = []
  for product in data:
    products.append(product[2])
  
  select_product = st.selectbox("【商品】", products)

  for product_data in data:
    if product_data[2] == select_product:
      sales_id = product_data[5]
      count = product_data[3]
      price = product_data[4]

  change_count = st.number_input("【個数】", min_value=1, value=count)

  st.write("【価格】")
  st.write(price)

  if "sales_data" not in st.session_state:
    st.session_state.sales_data = []

  if st.button("変更"):
    found = False
    for sales_data in st.session_state.sales_data:
      if sales_data[0] == sales_id:
        sales_data[2] = change_count
        found = True
    if not found:
      st.session_state.sales_data.append([sales_id, select_product, change_count, price])

  st.divider()

  if st.session_state.sales_data:
    st.write("【変更内容】")
    total_price = 0
    for data in st.session_state.sales_data:
      product_total = data[2] * data[3]
      total_price += product_total
      st.write(f"{data[1]} x {data[2]} → {product_total}円")

    st.divider()

    st.write("合計")
    st.write(total_price)

  if st.button("会計を確定"):
    if st.session_state.sales_data:
      for data in st.session_state.sales_data:
        database.sales_data_update(data[0], data[2])
      st.session_state.pop("sales_data", None)
      st.session_state.pop("payment_id", None)
      st.session_state.page = "home"
      st.rerun()
    else:
      st.warning("変更内容がありません")

  if st.button("戻る"):
    st.session_state.pop("sales_data", None)
    st.session_state.page = "sales_detail"
    st.rerun()
    
