import streamlit as st
import pandas as pd
import plotly.express as px
import boto3 # type: ignore
import yaml
import base64
from pathlib import Path
import streamlit_authenticator as stauth

st.set_page_config(page_title="ZRExport", layout="wide")

LOGO_PATH = "logo.png"
def get_base64(image_path): return base64.b64encode(Path(image_path).read_bytes()).decode()
logo_b64 = get_base64(LOGO_PATH)

st.markdown(f"""
<div style='display:flex; justify-content:center; margin-top:2rem;'>
  <img src='data:image/png;base64,{logo_b64}' width='180'>
</div>
""", unsafe_allow_html=True)

with open("config.yaml") as f:
    config = yaml.safe_load(f)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config.get('preauthorized', {})
)

name, auth_status, username = authenticator.login("Se connecter", "main")

if auth_status:
    authenticator.logout("Déconnexion", "sidebar")
    st.sidebar.success(f"Bienvenue {name}")

    # Récupération du rôle utilisateur
    role = config["credentials"]["usernames"][username]["role"]

    # Choix du menu en fonction du rôle
    options = []
    if role in ["admin", "export_only"]:
        options.append("Export")
    if role in ["admin", "viewer"]:
        options.append("Tableau de bord")

    if not options:
        st.error("Vous n'avez accès à aucune fonctionnalité.")
    else:
        choice = st.sidebar.selectbox("Que voulez-vous faire ?", options)

        if choice == "Export":
            st.header("📁 Export de données")
            df = pd.read_csv("queries.csv", sep=';')
            st.dataframe(df)
            csv = df.to_csv(index=False).encode()
            st.download_button("Télécharger CSV", csv, file_name="export.csv")

        elif choice == "Tableau de bord":
            st.header("📊 Tableau de bord")
            df = pd.read_csv("base client.csv", sep=';')
            st.dataframe(df)
            if all(col in df.columns for col in ["Ville", "Population"]):
                fig = px.bar(df, x="Ville", y="Population", title="Population par ville")
                st.plotly_chart(fig, use_container_width=True)

elif auth_status is False:
    st.error("Identifiants incorrects")
else:
    st.warning("Veuillez vous connecter")
