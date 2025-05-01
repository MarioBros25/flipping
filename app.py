
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Funzione per login semplice
def check_login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    return username == "Mariobros25" and password == "flipping2025"

# Caricamento dati
@st.cache_data
def load_data():
    try:
        return pd.read_csv("visite_salvate.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Zona", "Via", "Prezzo", "Mq", "Margine stimato", "Latitudine", "Longitudine", "Note"])

# Funzione per salvare nuova visita
def salva_visita(df, nuova_visita):
    df = df.append(nuova_visita, ignore_index=True)
    df.to_csv("visite_salvate.csv", index=False)
    return df

if check_login():
    st.title("CasaRevolution – Dashboard Operativa")

    df = load_data()

    # Mappa interattiva
    st.subheader("Mappa Opportunità")
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

    st.subheader("Inserisci una nuova visita")

    with st.form("nuova_visita"):
        zona = st.text_input("Zona")
        via = st.text_input("Via")
        prezzo = st.number_input("Prezzo richiesto", value=50000)
        mq = st.number_input("Superficie (mq)", value=80)
        lat = st.number_input("Latitudine", value=42.42)
        lon = st.number_input("Longitudine", value=12.11)
        note = st.text_area("Note")
        ristrutturazione = st.number_input("Costo ristrutturazione totale (€)", value=15000)
        stima_vendita = st.number_input("Valore stimato post-ristrutturazione (€)", value=prezzo + 30000)
        margine = stima_vendita - prezzo - ristrutturazione

        submitted = st.form_submit_button("Salva visita")

        if submitted:
            nuova = {
                "Zona": zona,
                "Via": via,
                "Prezzo": prezzo,
                "Mq": mq,
                "Margine stimato": margine,
                "Latitudine": lat,
                "Longitudine": lon,
                "Note": note
            }
            df = salva_visita(df, nuova)
            st.success(f"Visita salvata con margine stimato: €{margine}")

    st.subheader("Archivio visite salvate")
    st.dataframe(df.reset_index(drop=True))
else:
    st.warning("Inserisci username e password per accedere.")
