import streamlit as st
from datetime import date, timedelta
import database
import pandas as pd

def show():
  st.title("日別売り上げグラフ")

  col1, col2 = st.columns([1,3])
  
  with col1:
    st.markdown(
      "<div style='padding-top: 8px;'>期間：</div>",
      unsafe_allow_html=True
    )
    #unsafe_allow_html=True markdownの中にhtmlを使うことを許可する
    

  with col2:
    start_date = date(2026, 9, 1)
    today = date.today()
    current_date = start_date

    dates = []
    
    while current_date <= today:
      if current_date.month == 12:
        dates.append(current_date)
        current_date = date(
          current_date.year + 1,
          1,
          1
        )
        
      else:
        dates.append(current_date)
        current_date = date(
          current_date.year,
          current_date.month + 1,
          1
        )
    
    select_date = st.selectbox(
      "",
      dates,
      index=len(dates)-1,
      format_func= lambda x: x.strftime("%Y年%m月"),
      label_visibility="collapsed"
    )

  #選択した月の分の日付一覧を作成
  selected_month_start = select_date
  if select_date.month == 12:
    end_date = date(
      select_date.year + 1,
      1,
      1
    )
  else:
    end_date = date(
      select_date.year,
      select_date.month + 1,
      1
    )

  daily_current_date = selected_month_start
  daily_dates = []
  while daily_current_date < end_date:
    daily_dates.append(daily_current_date)
    daily_current_date += timedelta(days=1)


  select_date = select_date.strftime("%Y-%m")

  data = database.get_days_sales_data(select_date)

  #日付の型を変更
  data_dates = []
  for d in data:
    day = date.fromisoformat(d[0])
    data_dates.append((day, d[1]))

  
  month_data = []
  for daily in daily_dates:
    sales = False
    for dates in data_dates:
      if daily == dates[0]:
        month_data.append([daily, dates[1]])
        sales = True
    if not sales:
      month_data.append([daily, 0])

  df = pd.DataFrame(
    month_data,
    columns=["日付", "合計金額"]
  )  

  df["日付"] = df["日付"].apply(lambda x: x.strftime("%m/%d"))

  st.line_chart(
    df,
    x="日付",
    y="合計金額"
    )

  if st.button("戻る"):
    st.session_state.page = "home"
    st.rerun()
