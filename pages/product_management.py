import streamlit as st

def show():
  st.title("商品管理")

  if st.button("商品登録"):
    st.session_state.page = "product_registration"
    st.rerun()

  if st.button("商品編集"):
    st.session_state.page = "product_edit"
    st.rerun()

  if st.button("戻る"):
    st.session_state.page = "home"
    st.rerun()