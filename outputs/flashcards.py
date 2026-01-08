import streamlit as st


def display_flashcards(flashcards):
    """
    Display flashcards as clickable dropdown questions.
    Each question expands to show its answer.
    """

    if not flashcards:
        st.info("No flashcards generated.")
        return

    for i, card in enumerate(flashcards, start=1):
        with st.expander(f"❓ Q{i}: {card['question']}"):
            st.markdown(f"**Answer:** {card['answer']}")
