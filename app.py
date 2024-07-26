import streamlit as st
import pandas as pd
from itertools import product
import pyperclip

def load_excel(file):
    try:
        df = pd.read_excel(file)
        st.write("Fichier Excel chargé avec succès.")
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier Excel: {e}")
        return None

def display_data(df):
    st.dataframe(df)

def generate_combinations(selected_attributes, data):
    attribute_values = [data[attr].dropna().tolist() for attr in selected_attributes]
    combinations = list(product(*attribute_values))
    return combinations

def main():
    st.title("Générateur de combinaisons d'attributs")
    st.write("Démarrage de l'application...")

    uploaded_file = st.file_uploader("Importer un fichier Excel", type=["xls", "xlsx"])
    
    if uploaded_file is not None:
        st.write("Fichier téléchargé.")
        df = load_excel(uploaded_file)
        if df is not None:
            display_data(df)

            st.write("Sélectionnez les attributs à combiner :")
            selected_attributes = []
            for i, col in enumerate(df.columns):
                selected_attributes.append(st.selectbox(f"Attribut {i+1}", df.columns, index=i))

            if st.button("Ajouter un attribut"):
                selected_attributes.append(st.selectbox(f"Attribut {len(selected_attributes)+1}", df.columns, index=0))

            st.write("### Attributs sélectionnés :")
            for i, attr in enumerate(selected_attributes):
                st.write(f"Attribut {i+1}: {attr}")

            if st.button("Générer les combinaisons"):
                combinations = generate_combinations(selected_attributes, df)
                st.write("### Combinaisons générées :")
                for combination in combinations:
                    st.write(" ".join(combination))

                if st.button("Copier les combinaisons dans le presse-papier"):
                    combinations_str = "\n".join([" ".join(comb) for comb in combinations])
                    pyperclip.copy(combinations_str)
                    st.success("Les combinaisons ont été copiées dans le presse-papier.")

if __name__ == "__main__":
    main()
