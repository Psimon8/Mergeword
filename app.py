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

def generate_combinations(combinations, data):
    all_combinations = []
    for selected_attributes in combinations:
        attribute_values = [data[attr].dropna().tolist() for attr in selected_attributes]
        combs = list(product(*attribute_values))
        all_combinations.extend(combs)
    return all_combinations

def filter_combinations(combinations):
    filtered_combinations = []
    for comb in combinations:
        if len(set(comb)) == len(comb):  # Vérifie qu'il n'y a pas de valeurs dupliquées dans la combinaison
            filtered_combinations.append(comb)
    return filtered_combinations

def main():
    st.title("Générateur de combinaisons d'attributs")
    st.write("Démarrage de l'application...")

    uploaded_file = st.file_uploader("Importer un fichier Excel", type=["xls", "xlsx"])
    
    if uploaded_file is not None:
        st.write("Fichier téléchargé.")
        df = load_excel(uploaded_file)
        if df is not None:
            display_data(df)

            if 'combinations' not in st.session_state:
                st.session_state['combinations'] = [[]]

            if st.button("Ajouter une combinaison"):
                st.session_state['combinations'].append([])

            for i, combination in enumerate(st.session_state['combinations']):
                st.write(f"### Combinaison {i + 1}")
                cols = st.columns(len(combination) + 2)
                for j, attr in enumerate(combination):
                    with cols[j]:
                        st.selectbox(f"Attribut {j + 1}", df.columns, index=df.columns.get_loc(attr) if attr in df.columns else 0, key=f"comb_{i}_attr_{j}")
                        if st.button("Supprimer cet attribut", key=f"del_attr_{i}_{j}"):
                            st.session_state['combinations'][i].pop(j)
                            st.experimental_rerun()
                with cols[-2]:
                    st.title("")
                    if st.button("Ajouter un attribut", key=f"add_attr_{i}"):
                        combination.append(df.columns[0])
                with cols[-1]:
                    if st.button("Supprimer cette combinaison", key=f"del_comb_{i}"):
                        st.session_state['combinations'].pop(i)
                        st.experimental_rerun()

            if st.button("Générer les combinaisons"):
                combinations = generate_combinations(st.session_state['combinations'], df)
                filtered_combinations = filter_combinations(combinations)
                st.write("### Combinaisons générées :")
                for combination in filtered_combinations:
                    st.write(" ".join(combination))

                if st.button("Copier les combinaisons dans le presse-papier"):
                    combinations_str = "\n".join([" ".join(comb) for comb in filtered_combinations])
                    pyperclip.copy(combinations_str)
                    st.success("Les combinaisons ont été copiées dans le presse-papier.")

if __name__ == "__main__":
    main()
