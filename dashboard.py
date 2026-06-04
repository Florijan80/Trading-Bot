import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Trading Bot Analytics", layout="wide")

texts = {
    'Slovenščina': {
        'title': "📈 Trading Bot - Analitika in Portfelj",
        'tab_hist': "📓 Zgodovinski Backtest",
        'tab_live': "🔴 Live Demo (Forward Test)",
        'capital': "Začetni kapital ($)",
        'current_eq': "Trenutni Kapital",
        'win_rate': "Win Rate (Zmage/Porazi)",
        'pnl_total': "Skupni PnL",
        'chart_cap': "📊 Razporeditev kapitala",
        'chart_pnl': "📈 Zgodovina dobička",
        'open_pos': "🟢 Trenutno Odprte Pozicije",
        'closed_pos': "📓 Zgodovina Zaprtih Pozicij",
        'no_data': "Trenutno ni podatkov za prikaz."
    },
    'English': {
        'title': "📈 Trading Bot - Analytics & Portfolio",
        'tab_hist': "📓 Historical Backtest",
        'tab_live': "🔴 Live Demo (Forward Test)",
        'capital': "Starting Capital ($)",
        'current_eq': "Current Equity",
        'win_rate': "Win Rate (Wins/Losses)",
        'pnl_total': "Total PnL",
        'chart_cap': "📊 Capital Distribution",
        'chart_pnl': "📈 Profit History",
        'open_pos': "🟢 Currently Open Positions",
        'closed_pos': "📓 Closed Trades History",
        'no_data': "No data available currently."
    },
    'Deutsch': {
        'title': "📈 Trading Bot - Analytik & Portfolio",
        'tab_hist': "📓 Historischer Backtest",
        'tab_live': "🔴 Live Demo (Forward Test)",
        'capital': "Startkapital ($)",
        'current_eq': "Aktuelles Eigenkapital",
        'win_rate': "Gewinnrate (Siege/Niederlagen)",
        'pnl_total': "Gesamt PnL",
        'chart_cap': "📊 Kapitalverteilung",
        'chart_pnl': "📈 Gewinnhistorie",
        'open_pos': "🟢 Aktuell offene Positionen",
        'closed_pos': "📓 Historie geschlossener Trades",
        'no_data': "Derzeit keine Daten verfügbar."
    }
}

st.sidebar.header("🌐 Nastavitve")
selected_lang = st.sidebar.selectbox("Izberi jezik", ['Slovenščina', 'English', 'Deutsch'])
t = texts[selected_lang]

st.sidebar.markdown("---")
# Ločen kapital za Live in Zgodovino
zacetni_kapital_hist = st.sidebar.number_input(f"{t['capital']} (Zgodovina)", value=10000.0, step=100.0)
zacetni_kapital_live = st.sidebar.number_input(f"{t['capital']} (Live Demo)", value=10000.0, step=100.0)

st.title(t['title'])

# Branje podatkov iz baze
try:
    conn = sqlite3.connect('trading_bot.db')
    df = pd.read_sql_query("SELECT * FROM trades", conn)
    conn.close()
    
    # Če stolpca še ni, zaščitimo aplikacijo pred sesutjem
    if 'tip_trejda' not in df.columns:
        df['tip_trejda'] = 'zgodovina'
except Exception as e:
    st.error(f"Napaka pri branju baze: {e}")
    df = pd.DataFrame()

# Ustvarimo zavihke na vrhu strani
tab1, tab2 = st.tabs([t['tab_hist'], t['tab_live']])

# Pomožna funkcija za izris vsebine zavihka
def prikazi_zavihek(df_filter, zacetni_kapital):
    if df_filter.empty:
        st.info(t['no_data'])
        return

    df_closed = df_filter[df_filter['status'] == 'closed'].copy()
    df_open = df_filter[df_filter['status'] == 'open'].copy()

    total_pnl = df_closed['pnl'].sum() if not df_closed.empty else 0
    current_equity = zacetni_kapital + total_pnl

    winning_trades = len(df_closed[df_closed['pnl'] > 0])
    total_closed = len(df_closed)
    win_rate = (winning_trades / total_closed * 100) if total_closed > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric(t['current_eq'], f"${current_equity:,.2f}", f"${total_pnl:,.2f}")
    col2.metric(t['pnl_total'], f"${total_pnl:,.2f}")
    col3.metric(t['win_rate'], f"{win_rate:.1f}%", f"{winning_trades} / {total_closed}")

    st.markdown("---")
    
    if not df_closed.empty:
        pnl_by_strategy = df_closed.groupby('strategy_name')['pnl'].sum().reset_index()
        fig_bar = px.bar(pnl_by_strategy, x='strategy_name', y='pnl', color='strategy_name', title=t['chart_pnl'])
        st.plotly_chart(fig_bar, width='stretch')

    st.subheader(t['open_pos'])
    if not df_open.empty:
        st.dataframe(df_open[['id', 'strategy_name', 'symbol', 'entry_price', 'capital_used', 'entry_time']], hide_index=True)
    else:
        st.write(t['no_data'])

    st.subheader(t['closed_pos'])
    if not df_closed.empty:
        def color_pnl(val):
            return f"color: {'green' if val > 0 else 'red'}"
        st.dataframe(df_closed[['id', 'strategy_name', 'symbol', 'entry_price', 'pnl', 'entry_time', 'exit_time']].style.map(color_pnl, subset=['pnl']), hide_index=True)
    else:
        st.write(t['no_data'])

