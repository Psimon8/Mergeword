# File: merge_words_app.py

import streamlit as st
from itertools import product
import pyperclip

def merge_words(list1, list2, list3=None):
    if list3:
        merged = [f"{a} {b} {c}" for a, b, c in product(list1, list2, list3)]
    else:
        merged = [f"{a} {b}" for a, b in product(list1, list2)]
    return merged

def main():
    st.title("Merge Words Tool")
    st.write("Enter words in the lists below to create combinations with spaces as separators.")

    # Create three columns for the input lists
    col1, col2, col3 = st.columns(3)

    with col1:
        words1 = st.text_area("List 1", placeholder="Enter words here, one per line").splitlines()
    with col2:
        words2 = st.text_area("List 2", placeholder="Enter words here, one per line").splitlines()
    with col3:
        words3 = st.text_area("List 3 (optional)", placeholder="Enter words here, one per line").splitlines()

    # Determine if the third list is used
    if not words3:
        words3 = None

    # Calculate the estimated number of combinations
    estimated_combinations = len(words1) * len(words2) * (len(words3) if words3 else 1)
    st.write(f"Estimated combinations: {estimated_combinations}")

    # Buttons for merging and copying to clipboard
    copy_button, merge_button = st.columns([1, 3])
    generated_combinations = []

    if merge_button.button("Merge"):
        if not all([words1, words2]):
            st.warning("Please enter words in at least List 1 and List 2.")
        else:
            generated_combinations = merge_words(words1, words2, words3)
            st.write("Generated combinations:")

    # Display generated combinations as text output
    output_text = "\n".join(generated_combinations)
    st.text_area("Merged Combinations", value=output_text, height=200)

    # Copy to clipboard functionality
    if copy_button.button("Copy to Clipboard"):
        if generated_combinations:
            pyperclip.copy(output_text)
            st.success("Combinations copied to clipboard!")

if __name__ == "__main__":
    main()
