import streamlit as st
import database

def show():
  st.title("商品編集")

  data = database.get_product_data()
  product_name = []
  for product_data in data:
    product_name.append(product_data[1])
  select_name = st.selectbox("【編集する商品】", product_name)

  st.write("【商品名】")
  with st.container(border=True):
    st.write(select_name)

  for product_data in data:
    if select_name == product_data[1]:
      select_data = product_data

  st.session_state.id = select_data[0]
  st.session_state.name = select_data[1]

  category = st.text_input("【カテゴリ】", select_data[2])
  st.session_state.category = category

  price = st.number_input("【販売価格】", value=select_data[3], min_value=0)
  st.session_state.price = price

  status_list = ["販売中", "停止中"]
  status = st.selectbox("【ステータス】", status_list, index=status_list.index(select_data[4]))
  st.session_state.status = status

  if st.button("確認"):
    st.session_state.page = "product_edit_confirm"
    st.rerun()

  if st.button("戻る"):
    st.session_state.pop("id", None)
    st.session_state.pop("name", None)
    st.session_state.pop("category", None)
    st.session_state.pop("price", None)
    st.session_state.pop("status", None)
    st.session_state.page = "product_management"
    st.rerun()

