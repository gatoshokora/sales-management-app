import streamlit as st

st.set_page_config(
  page_title="店舗向け売り上げ管理・分析アプリ",
  layout="centered"
)
def show():

  st.title("店舗向け売り上げ管理・分析アプリ")

  if st.button("売り上げ登録"):
    st.session_state.page = "sales_registration"
    st.rerun()

  if st.button("売り上げ一覧"):
    st.session_state.page = "sales_list"
    st.rerun()

  if st.button("商品管理"):
    st.session_state.page = "product_management"
    st.rerun()

  if st.button("売り上げ分析"):
    st.session_state.page = "sales_analysis"
    st.rerun()
  