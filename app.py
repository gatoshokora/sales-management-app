import streamlit as st

from pages import home
from pages import product_management as pm
from pages import product_registration as pr
from pages import product_confirm as pc
from pages import product_edit as pe
from pages import product_edit_confirm as pec
from pages import sales_registration as sr
from pages import sales_registration_confirm as src
from pages import sales_list as sl
from pages import sales_detail as sd
from pages import sales_detail_edit as sde
from pages import sales_analysis as sa
from pages import sales_by_product as sbp
from pages import sales_by_date as sbd


if "page" not in st.session_state:
  st.session_state.page = "home"

if st.session_state.page == "home":
  home.show()

elif st.session_state.page == "product_management":
  pm.show()

elif st.session_state.page == "product_registration":
  pr.show()

elif st.session_state.page == "product_confirm":
  pc.show()

elif st.session_state.page == "product_edit":
  pe.show()

elif st.session_state.page == "product_edit_confirm":
  pec.show()

elif st.session_state.page == "sales_registration":
  sr.show()

elif st.session_state.page == "sales_registration_confirm":
  src.show()

elif st.session_state.page == "sales_list":
  sl.show()

elif st.session_state.page == "sales_detail":
  sd.show()

elif st.session_state.page == "sales_detail_edit":
  sde.show()

elif st.session_state.page == "sales_analysis":
  sa.show()

elif st.session_state.page == "sales_by_product":
  sbp.show()

elif st.session_state.page == "sales_by_date":
  sbd.show()