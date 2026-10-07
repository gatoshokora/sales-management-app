import streamlit as st

def show():
  st.title("売り上げ分析")

  if st.button("【商品ごとの売り上げ】"):
    st.session_state.page = "sales_by_product"
    st.rerun()

  if st.button("【日別売り上げグラフ】"):
    st.session_state.page = "sales_by_date"
    st.rerun()

  st.divider()
  
  if st.button("戻る"):
    st.session_state.page = "home"
    st.rerun()