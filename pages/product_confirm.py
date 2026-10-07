import streamlit as st
import database

def show():
  st.title("商品登録確認")

  st.write("【商品名】")
  with st.container(border=True):
    #border=True = 枠線を表示
    st.write(st.session_state.product_name)

  st.write("【カテゴリ】")
  with st.container(border=True):
    st.write(st.session_state.category)

  st.write("【販売価格】")
  with st.container(border=True):
    st.write(st.session_state.price)

  st.write("【ステータス】")
  with st.container(border=True):
    st.write(st.session_state.status)

  if st.button("確定"):
    database.add_product(st.session_state.product_name, st.session_state.category, st.session_state.price, st.session_state.status)
    st.session_state.pop("product_name", None)
    st.session_state.pop("category", None)
    st.session_state.pop("price", None)
    st.session_state.pop("status", None)
    st.session_state.page = "home"
    st.rerun()

  if st.button("戻る"):
    st.session_state.page = "product_registration"
    st.rerun()
