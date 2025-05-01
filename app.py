
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
def load_data():
    return pd.read_csv("dati_demo.csv")

if check_login():
    st.title("CasaRevolution – Dashboard Immobiliare")
    df = load_data()

    st.sidebar.header("Filtri")
    quartieri = st.sidebar.multiselect("Zona", options=df["Zona"].unique(), default=list(df["Zona"].unique()))
    df = df[df["Zona"].isin(quartieri)]

    st.subheader("Mappa Opportunità")
    mappa = folium.Map(location=[42.42, 12.11], zoom_start=10)
    marker_cluster = MarkerCluster().add_to(mappa)

    for _, row in df.iterrows():
        popup = f"""<b>{row['Via']}</b><br>
        Prezzo: €{row['Prezzo']}<br>
        Superficie: {row['Mq']} mq<br>
        Margine stimato: €{row['Margine stimato']}"""
        folium.Marker(
            location=[row["Latitudine"], row["Longitudine"]],
            popup=popup,
            icon=folium.Icon(color="green" if row["Margine stimato"] > 0 else "red")
        ).add_to(marker_cluster)

    folium_static(mappa)

    st.subheader("Dettaglio Immobili")
    st.dataframe(df.reset_index(drop=True))
else:
    st.warning("Inserisci username e password per accedere.")
