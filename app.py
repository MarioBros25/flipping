
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

def check_login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    return username == "Mariobros25" and password == "flipping2025"

@st.cache_data
def load_visite():
    try:
        return pd.read_csv("visite_salvate.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Zona", "Via", "Prezzo", "Mq", "Margine stimato", "Latitudine", "Longitudine", "Note"])

@st.cache_data
def load_aste():
    try:
        return pd.read_csv("aste.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Indirizzo", "Prezzo base (€)", "Offerta minima (€)", "Data asta", "Superficie (mq)", "Link", "Latitudine", "Longitudine"])

if check_login():
    st.title("CasaRevolution – Dashboard Operativa")

    menu = st.sidebar.radio("Sezione", ["📍 Visite", "🏛️ Aste immobiliari"])

    if menu == "📍 Visite":
        df = load_visite()

        st.subheader("Mappa Opportunità – Visite")
        mappa = folium.Map(location=[42.42, 12.11], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(mappa)

        for _, row in df.iterrows():
            popup = f"""<b>{row['Via']}</b><br>
            Prezzo: €{row['Prezzo']}<br>
            Superficie: {row['Mq']} mq<br>
            Margine stimato: €{row['Margine stimato']}<br>
            Note: {row['Note']}"""
            folium.Marker(
                location=[row["Latitudine"], row["Longitudine"]],
                popup=popup,
                icon=folium.Icon(color="green" if row["Margine stimato"] > 0 else "red")
            ).add_to(marker_cluster)

        folium_static(mappa)

        st.subheader("Archivio visite salvate")
        st.dataframe(df.reset_index(drop=True))

    elif menu == "🏛️ Aste immobiliari":
        df_aste = load_aste()

        st.subheader("Mappa Aste a Viterbo")
        mappa_aste = folium.Map(location=[42.42, 12.11], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(mappa_aste)

        for _, row in df_aste.iterrows():
            popup = f"""<b>{row['Indirizzo']}</b><br>
            Prezzo base: €{row['Prezzo base (€)']}<br>
            Data asta: {row['Data asta']}<br>
            <a href='{row['Link']}' target='_blank'>Vai all'annuncio</a>"""
            folium.Marker(
                location=[row["Latitudine"], row["Longitudine"]],
                popup=popup,
                icon=folium.Icon(color="blue")
            ).add_to(marker_cluster)

        folium_static(mappa_aste)

        st.subheader("Elenco Aste")
        st.dataframe(df_aste.reset_index(drop=True))
else:
    st.warning("Inserisci username e password per accedere.")
