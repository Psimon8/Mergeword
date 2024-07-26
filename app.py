import streamlit as st
import pandas as pd
from itertools import product
import pyperclip

def load_excel(file):
    return pd.read_excel(file)

def display_data(df):
    st.dataframe(df)

def generate_combinations(selected_attributes, data):
    attribute_values = [data[attr].dropna().tolist() for attr in selected_attributes]
    return list(product(*attribute_values))

def main():
    st.title("Générateur de combinaisons d'attributs")

    uploaded_file = st.file_uploader("Importer un fichier Excel", type=["xls", "xlsx"])
    
    if uploaded_file is not None:
        df = load_excel(uploaded_file)
        display_data(df)

        selected_attributes = []
        st.write("Sélectionnez les attributs à combiner :")
        for i, col in enumerate(df.columns):
            selected_attributes.append(st.selectbox(f"Attribut {i+1}", df.columns, index=i))

        if st.button("Ajouter un attribut"):
            selected_attributes.append(st.selectbox(f"Attribut {len(selected_attributes)+1}", df.columns, index=0))

        if selected_attributes:
            combinations = generate_combinations(selected_attributes, df)
            st.write("Combinaisons générées :")
            for combination in combinations:
                st.write(" ".join(combination))

            if st.button("Copier les combinaisons dans le presse-papier"):
                combinations_str = "\n".join([" ".join(comb) for comb in combinations])
                pyperclip.copy(combinations_str)
                st.success("Les combinaisons ont été copiées dans le presse-papier.")

if __name__ == "__main__":
    main()
