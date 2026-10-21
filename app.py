import streamlit as st
import google.generativeai as genai
import requests
import json
from datetime import datetime

st.title("🤖 Mijn Gratis AI Assistent")
st.write(f"Vraag me alles! Vandaag is het: {datetime.now().strftime('%A %d %B %Y')}")

# Haal de API-sleutels veilig op uit de Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    make_url = st.secrets.get("MAKE_WEBHOOK_URL", "")
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Oeps! Je API-sleutel is nog niet goed ingesteld in de Secrets.")
    st.stop()

# Handige functie om data naar Make.com te sturen
def plan_agenda_afspraak(titel, datum_tijd, beschrijving=""):
    """Stuurt een agenda-afspraak door naar Make.com"""
    if not make_url:
        return "Fout: Geen MAKE_WEBHOOK_URL ingesteld in Secrets."
    
    payload = {
        "titel": titel,
        "datum_tijd": datum_tijd,
        "beschrijving": beschrijving
    }
    try:
        response = requests.post(make_url, json=payload)
        if response.status_code == 200:
            return f"✅ Ik heb de afspraak '{titel}' voor {datum_tijd} succesvol in je agenda gezet!"
        return f"❌ Make.com gaf een foutmelding: {response.status_code}"
    except Exception as e:
        return f"❌ Kon geen verbinding maken met Make: {e}"

# Initialiseer de chatgeschiedenis
if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon eerdere berichten op het scherm
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Reageer op wat jij typt
if prompt := st.chat_input("Typ een bericht aan je assistent..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # We vertellen de AI via de System Instruction exact hoe hij moet reageren bij een afspraak
            system_instruction = (
                "Je bent een persoonlijke assistent die afspraken inplant. "
                "HET IS NU HET JAAR 2026. Als de gebruiker een datum noemt zoals '26 oktober', bedoelt hij ALTIJD 26 oktober 2026. "
                "Als de gebruiker een afspraak, herinnering of planning noemt met een datum en tijd, "
                "moet je ALTIJD reageren door DIRECT te beginnen met de tekst: [AGENDA_ACTIE] "
                "gevolgd door de details in JSON formaat op de volgende regel. Geef GEEN normale tekst vooraf. "
                "Zorg dat het JSON formaat er exact zo uitziet (let op dat het jaartal 2026 is):\n"
                "{\n\"titel\": \"Naam van de afspraak\",\n\"datum_tijd\": \"2026-10-26T11:00:00\",\n\"beschrijving\": \"\"\n}"
            )

            
            model = genai.GenerativeModel("gemini-2.5-pro", system_instruction=system_instruction)


            response = model.generate_content(prompt)
            ai_response = response.text

            # Controleer of de AI een agenda-actie wil uitvoeren
            if "[AGENDA_ACTIE]" in ai_response:
                try:
                    # Haal de JSON data uit het antwoord
                    json_str = ai_response.split("[AGENDA_ACTIE]")[1].strip()
                    data = json.loads(json_str)
                    
                    # Voer de functie uit om naar Make te sturen
                    resultaat = plan_agenda_afspraak(data["titel"], data["datum_tijd"], data.get("beschrijving", ""))
                    message_placeholder.markdown(resultaat)
                    ai_response = resultaat
                except Exception as e:
                    message_placeholder.markdown(f"Ik begreep de agendagegevens niet helemaal goed: {e}")
            else:
                message_placeholder.markdown(ai_response)
                
        except Exception as e:
            ai_response = f"Er ging iets mis met de verbinding: {e}"
            message_placeholder.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

