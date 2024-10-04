# File: merge_words_app.py

import streamlit as st
from itertools import product
import pandas as pd
from io import BytesIO

# Function to merge words from dynamic lists with spaces
def merge_words(lists):
    return [" ".join(words) for words in product(*lists)]

# Function to create a downloadable Excel file
def create_excel_download(data):
    output = BytesIO()
    df = pd.DataFrame(data, columns=["Combination"])
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def main():
    st.title("Merge Words Tool with Dynamic Columns")
    st.write("Enter words in each box to create combinations with spaces as separators.")

    # Dynamic list to store text inputs for each column
    input_lists = []

    # Initial columns setup
    num_columns = st.session_state.get('num_columns', 3)
    
    for i in range(num_columns):
        input_list = st.text_area(f"List {i+1}", placeholder="Enter words here, one per line").splitlines()
        input_lists.append(input_list)
    
    # Add new column button
    if st.button("Add Another List"):
        st.session_state.num_columns = num_columns + 1

    # Calculate the estimated number of combinations
    estimated_combinations = 1
    for lst in input_lists:
        estimated_combinations *= len(lst) or 1  # Handle empty lists

    st.write(f"Estimated combinations: {estimated_combinations}")

    # Initialize list for storing results
    generated_combinations = []
    output_text = ""
    
    # Buttons for merging, copying to clipboard, and downloading
    copy_button, merge_button, download_button = st.columns([1, 2, 1])

    # Merge button functionality
    if merge_button.button("Merge"):
        if any(len(lst) == 0 for lst in input_lists[:2]):  # Require at least two lists with entries
            st.warning("Please enter words in at least List 1 and List 2.")
        else:
            generated_combinations = merge_words(input_lists)
            output_text = "\n".join(generated_combinations)
            st.write("Generated combinations:")

    # Display generated combinations as text output
    st.text_area("Merged Combinations", value=output_text, height=200)

    # Copy to clipboard using JavaScript
    if generated_combinations:
        st.markdown("""
            <button onclick="copyToClipboard()">Copy to Clipboard</button>
            <script>
            function copyToClipboard() {
                var textArea = document.createElement("textarea");
                textArea.value = `""" + output_text + """`;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand("copy");
                document.body.removeChild(textArea);
                alert("Copied to clipboard!");
            }
            </script>
            """, unsafe_allow_html=True)

    # Download as XLSX functionality
    if generated_combinations:
        excel_data = create_excel_download([(combo,) for combo in generated_combinations])
        download_button.download_button(
            label="Download as XLSX",
            data=excel_data,
            file_name="merged_combinations.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
