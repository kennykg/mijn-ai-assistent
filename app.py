import streamlit as st
import google.generativeai as genai

st.title("🤖 Mijn Gratis AI Assistent")
st.write("Vraag me alles! Ik werk nu live via Google Gemini.")

# Haal de API-sleutel veilig op uit de Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Oeps! Je API-sleutel is nog niet goed ingesteld in de Secrets.")
    st.stop()

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

    # Roep de echte AI van Google aan
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # We gebruiken het nieuwste, snelle en gratis model
            model = genai.GenerativeModel("gemini-3.8-flash")
            response = model.generate_content(prompt)
            ai_response = response.text
            message_placeholder.markdown(ai_response)
        except Exception as e:
            ai_response = f"Er ging iets mis met de verbinding: {e}"
            message_placeholder.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

