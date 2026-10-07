import streamlit as st

def show():
  st.title("商品登録")

  product_name = st.text_input("【商品名】")
  if product_name:
    st.session_state.product_name = product_name

  
  categories = ["ハンバーガー","サイドメニュー","ドリンク","デザート"]
  category = st.selectbox("【カテゴリ】", categories)
  st.session_state.category = category

  price = st.number_input("【販売価格】", min_value=1)
  if price:
    st.session_state.price = price

  status = ["販売中","停止中"]
  sales_status = st.selectbox("【ステータス】", status)
  if sales_status:
    st.session_state.status = sales_status

  st.divider()

  if st.button("確認"):
    if not product_name:
      st.error("商品名が入力されていません")
    else:
      if not price:
        st.error("販売価格が入力されていません")
      else:
        st.session_state.page = "product_confirm"
        st.rerun()

  if st.button("戻る"):
    st.session_state.pop("product_name", None)
    st.session_state.pop("category", None)
    st.session_state.pop("price", None)
    st.session_state.pop("status", None)
    st.session_state.page = "product_management"
    st.rerun()