import streamlit as st
import pandas as pd

def main():
    st.title("Générateur de combinaisons d'attributs")
    st.write("Démarrage de l'application...")

    uploaded_file = st.file_uploader("Importer un fichier Excel", type=["xls", "xlsx"])
    
    if uploaded_file is not None:
        st.write("Fichier téléchargé.")
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Fichier Excel chargé avec succès.")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier Excel: {e}")

if __name__ == "__main__":
    main()
