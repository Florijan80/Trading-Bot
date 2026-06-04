import streamlit as st

st.set_page_config(page_title="Live Trgovanje", page_icon="🔴", layout="wide")

st.title("🔴 Live Signali in Trgovanje")
st.markdown("---")

st.info("Sistem je v pripravljenosti in v ozadju posluša. Tukaj se bodo v živo izpisovali TradingView signali ob vsakem premiku trga (vključno z zaznavo BTC volatilnosti ter klasičnimi divergencami, kot sta L-BDIV in S-BDIV).")

st.write("Trenutno čakamo na prve žive podatke iz Webhooka...")