import streamlit as st
import openai

# Configuración básica
st.set_page_config(page_title="🇨🇴 Asesor Turístico", page_icon="🏖️")

st.title("🇨🇴 Asesor Turístico Colombiano")
st.write("¡Hola, parce! Pregúntame sobre turismo en Colombia")

# Configurar OpenAI
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    api_ok = True
except:
    st.error("❌ Configura OPENAI_API_KEY en Secrets")
    api_ok = False

# Prompt del sistema
PROMPT = """
Eres un asesor turístico colombiano amigable. Usa expresiones como "parce", "bacano", "chévere". 
Ayuda con destinos, hoteles, comida y actividades en Colombia. 
Sé cálido y entusiasta, pero mantén respuestas concisas.
"""

# Inicializar chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input del usuario
if prompt := st.chat_input("Pregunta sobre Colombia..."):
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generar respuesta si API está configurada
    if api_ok:
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # Preparar mensajes para OpenAI
                    messages = [{"role": "system", "content": PROMPT}]
                    for msg in st.session_state.messages:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    # Llamar OpenAI
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        max_tokens=300,
                        temperature=0.7
                    )
                    
                    answer = response.choices[0].message.content
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                
                except Exception as e:
                    st.error(f"Error: {e}")

# Botón para limpiar chat
if st.button("🗑️ Limpiar Chat"):
    st.session_state.messages = []
    st.rerun()
