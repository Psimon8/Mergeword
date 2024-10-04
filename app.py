# File: merge_words_app.py

import streamlit as st
from itertools import product

def merge_words(list1, list2, list3, separator):
    merged = [f"{a}{separator}{b}{separator}{c}" for a, b, c in product(list1, list2, list3)]
    return merged

def main():
    st.title("Merge Words Tool")
    st.write("Enter words in each box to create combinations. Useful for SEO, PPC, and link-building.")

    # Input boxes for three lists
    words1 = st.text_area("Enter words for List 1 (one per line)").splitlines()
    words2 = st.text_area("Enter words for List 2 (one per line)").splitlines()
    words3 = st.text_area("Enter words for List 3 (one per line)").splitlines()

    # Separator options
    separator_option = st.selectbox("Choose a separator", ["None", "Space", "Hyphen", "Plus", "Custom"])
    custom_separator = ""
    if separator_option == "Space":
        separator = " "
    elif separator_option == "Hyphen":
        separator = "-"
    elif separator_option == "Plus":
        separator = "+"
    elif separator_option == "Custom":
        custom_separator = st.text_input("Enter custom separator")
        separator = custom_separator
    else:
        separator = ""

    # Button to generate merged words
    if st.button("Merge"):
        if not all([words1, words2, words3]):
            st.warning("Please enter words in all three lists.")
        else:
            results = merge_words(words1, words2, words3, separator)
            st.write("Generated combinations:")
            st.write(results)

if __name__ == "__main__":
    main()
