
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

        # Parametri personalizzabili
        euro_mq_vendita = st.sidebar.number_input("€/mq stimato per rivendita", value=1300)
        costo_ristrutturazione_mq = st.sidebar.number_input("€/mq costo ristrutturazione", value=300)
        euro_mq_vendita = 1300
        costo_ristrutturazione_mq = 300

        df_aste["Valore stimato (€)"] = df_aste["Superficie (mq)"] * euro_mq_vendita
        df_aste["Ristrutturazione (€)"] = df_aste["Superficie (mq)"] * costo_ristrutturazione_mq
        df_aste["Margine netto (€)"] = df_aste["Valore stimato (€)"] - df_aste["Prezzo base (€)"] - df_aste["Ristrutturazione (€)"]

        # Filtro margine
        margine_minimo = st.sidebar.slider("Margine minimo desiderato (€)", min_value=0, max_value=200000, value=10000, step=500)
        df_aste = df_aste[df_aste["Margine netto (€)"] >= margine_minimo]

        # Parametri personalizzabili
        euro_mq_vendita = st.sidebar.number_input("€/mq stimato per rivendita", value=1300)
        costo_ristrutturazione_mq = st.sidebar.number_input("€/mq costo ristrutturazione", value=300)
        euro_mq_vendita = 1300
        costo_ristrutturazione_mq = 300

        df_aste["Valore stimato (€)"] = df_aste["Superficie (mq)"] * euro_mq_vendita
        df_aste["Ristrutturazione (€)"] = df_aste["Superficie (mq)"] * costo_ristrutturazione_mq
        df_aste["Margine netto (€)"] = df_aste["Valore stimato (€)"] - df_aste["Prezzo base (€)"] - df_aste["Ristrutturazione (€)"]

        st.subheader("Mappa Aste a Viterbo")
        mappa_aste = folium.Map(location=[42.42, 12.11], zoom_start=10)
        marker_cluster = MarkerCluster().add_to(mappa_aste)

        for _, row in df_aste.iterrows():
            popup = f"""<b>{row['Indirizzo']}</b><br>
            Prezzo base: €{row['Prezzo base (€)']}<br>
            Data asta: {row['Data asta']}<br>
            Superficie: {row['Superficie (mq)']} mq<br>
            Valore stimato: €{row['Valore stimato (€)']}<br>
            Ristrutturazione: €{row['Ristrutturazione (€)']}<br>
            Margine netto: €{row['Margine netto (€)']}<br>
            <a href='{row['Link']}' target='_blank'>Vai all'annuncio</a>"""
            folium.Marker(
                location=[row["Latitudine"], row["Longitudine"]],
                popup=popup,
                icon=folium.Icon(color="blue")
            ).add_to(marker_cluster)

        folium_static(mappa_aste)

        st.subheader("Elenco Aste con Margine Stimato")
        st.dataframe(df_aste.reset_index(drop=True))
else:
    st.warning("Inserisci username e password per accedere.")
