import streamlit as st
import pandas as pd
from itertools import product
import pyperclip
import sqlite3

st.set_page_config(
    layout="wide",
    page_title="Merge Word",
    page_icon="🌶"
)

# Initialize SQLite database
conn = sqlite3.connect('combinations.db')
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS combinations (
        id INTEGER PRIMARY KEY,
        combination TEXT
    )
''')
conn.commit()

@st.cache_data  # Cache le résultat pour accélérer les chargements futurs
def load_excel(file):
    try:
        df = pd.read_excel(file)
        st.success("Fichier Excel chargé avec succès.")
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier Excel: {e}")
        return None

def display_data(df):
    st.dataframe(df)

@st.cache_data  # Cache le résultat pour accélérer les calculs futurs
def generate_combinations(combinations, data):
    all_combinations = []
    total = len(combinations)
    progress_bar = st.progress(0)

    for i, selected_attributes in enumerate(combinations):
        attribute_values = [data[attr].dropna().tolist() for attr in selected_attributes if attr in data.columns]
        if attribute_values:
            combs = list(product(*attribute_values))
            all_combinations.extend(combs)
        progress_bar.progress((i + 1) / total)

    return all_combinations

def filter_combinations(combinations):
    filtered_combinations = []
    for comb in combinations:
        if len(set(comb)) == len(comb):  # Vérifie qu'il n'y a pas de valeurs dupliquées dans la combinaison
            filtered_combinations.append(comb)
    return filtered_combinations

def load_combinations():
    c.execute('SELECT * FROM combinations')
    rows = c.fetchall()
    return [eval(row[1]) for row in rows]  # Use eval to convert string representation back to list

def save_combinations(combinations):
    c.execute('DELETE FROM combinations')
    for comb in combinations:
        c.execute('INSERT INTO combinations (combination) VALUES (?)', (str(comb),))
    conn.commit()

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
                st.session_state['combinations'] = load_combinations()
                if not st.session_state['combinations']:
                    st.session_state['combinations'] = [[df.columns[0], df.columns[1]] if len(df.columns) > 1 else [df.columns[0]]]

            for i, combination in enumerate(st.session_state['combinations']):
                st.write(f"### Combinaison {i + 1}")
                cols = st.columns(6)
                for j in range(5):  # Toujours afficher 5 colonnes pour les attributs
                    with cols[j]:
                        if j < len(combination):
                            selected_attr = st.selectbox(f"Attribut {j + 1}", df.columns, index=df.columns.get_loc(combination[j]) if combination[j] in df.columns else 0, key=f"comb_{i}_attr_{j}")
                            if selected_attr != combination[j]:
                                st.session_state['combinations'][i][j] = selected_attr
                                save_combinations(st.session_state['combinations'])
                        else:
                            st.write("")  # Placeholder pour aligner les colonnes
                with cols[5]:
                    if len(combination) < 5:
                        if st.button("Ajouter un attribut", key=f"add_attr_{i}"):
                            st.session_state['combinations'][i].append(df.columns[0])
                            save_combinations(st.session_state['combinations'])
                    st.write("")
                    if st.button("Supprimer cette combinaison", key=f"del_comb_{i}"):
                        st.session_state['combinations'].pop(i)
                        save_combinations(st.session_state['combinations'])

            st.write("### Actions")
            if st.button("Ajouter une combinaison", key="add_comb"):
                st.session_state['combinations'].append([df.columns[0], df.columns[1]] if len(df.columns) > 1 else [df.columns[0]])
                save_combinations(st.session_state['combinations'])

            if st.button("Générer les combinaisons", key="gen_combinations"):
                with st.spinner("Génération des combinaisons en cours..."):  # Affiche une barre de progression pendant la génération
                    combinations_data = generate_combinations(st.session_state['combinations'], df)
                    filtered_combinations = filter_combinations(combinations_data)
                st.success("Génération des combinaisons terminée.")
                st.write("### Combinaisons générées :")
                if filtered_combinations:
                    for combination in filtered_combinations:
                        st.write(" ".join(combination))
                else:
                    st.warning("Aucune combinaison générée. Vérifiez que les attributs sont correctement sélectionnés.")

                if st.button("Copier les combinaisons dans le presse-papier", key="copy_combinations"):
                    combinations_str = "\n".join([" ".join(comb) for comb in filtered_combinations])
                    pyperclip.copy(combinations_str)
                    st.success("Les combinaisons ont été copiées dans le presse-papier.")

if __name__ == "__main__":
    main()
