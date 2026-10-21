import streamlit as st

st.title("🤖 Mijn Gratis AI Assistent")
st.write("Welkom! Dit is de basis van jouw eigen AI-assistent.")

# Initialiseer de chatgeschiedenis
if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon eerdere berichten op het scherm
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Reageer op wat jij typt
if prompt := st.chat_input("Typ een bericht aan je assistent..."):
    # Toon jouw bericht
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Dit is nu nog een tijdelijk test-antwoord van de AI
    ai_response = f"Ik heb je bericht ontvangen: '{prompt}'. Binnenkort reageer ik hier als een échte AI!"
    
    # Toon het antwoord van de AI
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
