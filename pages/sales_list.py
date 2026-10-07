import streamlit as st
import database
from datetime import date, timedelta
#date 日付
#timedelta 「1日後」「2日後」など、日付の差
import pandas as pd


def show():
  st.title("売り上げ一覧")

  start_date = date(2026, 9, 1)
  today = date.today()

  dates = []
  current_date = start_date

  while current_date <= today:
    dates.append(current_date.strftime("%Y-%m-%d"))
    current_date += timedelta(days=1)
    #strftime 日付を文字列に変換

  selected_date = st.selectbox(
    "日付",
    dates,
    index=len(dates)-1,
    format_func=lambda x: x.replace("-", "/")
  )
  #format_func 選択肢の「表示の仕方」を指定 → 中身は変わっていない（日付）
  #lambda x  「渡されてきた値をxとして、この後の処理をする」

  payment_ids = database.get_payment_data(selected_date)
  sales_data = []
  for payment_id in payment_ids:
    sales_data.append(database.get_sales_data(payment_id[0]))

  #payment_idごとの売り上げ商品
  products_list = []
  for product_list in sales_data:
    products = []
    total = 0
    for product in product_list:
      products.append(f"{product[2]}x{product[3]}")
      total += product[3] * product[4]
    products = "、".join(products)
    products_list.append([product_list[0][0], product_list[0][1], products, total])
  #join リストを1つの文字列にする

  df = pd.DataFrame(
    products_list,
    columns=["payment_id", "時刻", "商品x個数", "合計金額"]
  )

  event = st.dataframe(
    df[["時刻","商品x個数","合計金額"]],
    on_select="rerun",
    selection_mode="single-row"
  )
#dfの中身を表として表示する
#on_select="rerun" 行を選択したらどうするか streamlitをもう一度実行する
#selection_mode="single-row 選択できる範囲を指定 一回につき一行選択できる
#event= 表で何が選択されたかをeventに受けとれる
#event.selection.rowsを見ると、選択された行番号が分かる

  #行番号を取得
  if event.selection.rows:
    selected_row = event.selection.rows[0]

    #行をdfから取り出す
    selected_data = df.iloc[selected_row]

    #payment_idだけを取り出す
    payment_id = int(selected_data["payment_id"])

    if st.button("詳細を見る"):
      st.session_state.payment_id = payment_id
      st.session_state.page = "sales_detail"
      st.rerun()

  if st.button("戻る"):
    st.session_state.pop("payment_id", None)
    st.session_state.page = "home"
    st.rerun()


