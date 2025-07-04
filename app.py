import streamlit as st
import openai
import json
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="🇨🇴 Asesor Turístico Colombiano",
    page_icon="🏖️",
    layout="wide"
)

# CSS personalizado para tema colombiano
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FFD700 0%, #FF6B35 50%, #004D9F 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .user-message {
        background: linear-gradient(90deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background: linear-gradient(90deg, #FFF3E0 0%, #FFE0B2 100%);
        border-left: 4px solid #FF9800;
    }
    .colombia-flag {
        display: inline-block;
        width: 20px;
        height: 15px;
        background: linear-gradient(to bottom, #FFD700 33%, #004D9F 33%, #004D9F 66%, #FF0000 66%);
        margin-right: 5px;
        border-radius: 2px;
    }
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🇨🇴 ¡Bienvenido a Colombia, Parce! 🏖️</h1>
    <p>Tu asesor turístico personal con el mejor sazón colombiano</p>
    <p>🏔️ Montañas • 🏖️ Playas • 🌆 Ciudades • 🎭 Cultura • ☕ Café</p>
</div>
""", unsafe_allow_html=True)

# Configuración de OpenAI
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    api_key_configured = True
except:
    api_key_configured = False
    st.error("🔑 API Key de OpenAI no configurada. Ve a Settings → Secrets y agrega OPENAI_API_KEY")

# Prompt del sistema para el chatbot colombiano
SYSTEM_PROMPT = """
Eres un asesor turístico colombiano experto, amigable y carismático. Tu personalidad es:

🇨🇴 PERSONALIDAD COLOMBIANA:
- Usa expresiones típicamente colombianas como: "parce", "hermano/a", "qué chimba", "bacano", "chévere", "¡Ey, ave maría!", "¡Qué maravilla!"
- Sé cálido, entusiasta y orgulloso de Colombia
- Usa un tono conversacional y familiar, pero profesional
- Siempre muestra alegría y positividad colombiana

🏛️ CONOCIMIENTO TURÍSTICO:
- Eres experto en TODOS los destinos turísticos de Colombia
- Conoces hoteles, restaurantes, actividades, transporte y cultura
- Puedes recomendar desde destinos populares hasta joyas escondidas
- Tienes conocimiento actualizado sobre precios, temporadas y consejos prácticos

📍 PRINCIPALES DESTINOS QUE DOMINAS:
- Cartagena, Santa Marta, San Andrés (Caribe)
- Bogotá, Medellín, Cali (ciudades principales)
- Eje Cafetero (Armenia, Pereira, Manizales)
- Amazonas, Llanos, Pacífico
- Pueblos patrimonio como Villa de Leyva, Barichara
- Parques nacionales y aventura

🎯 TU MISIÓN:
- Ayudar a planificar viajes increíbles por Colombia
- Dar recomendaciones personalizadas según gustos y presupuesto
- Compartir tips locales y secretos que solo un colombiano conoce
- Hacer que la gente se enamore de Colombia

💬 ESTILO DE RESPUESTA:
- Saluda siempre con energía colombiana
- Usa emojis relacionados con Colombia y turismo
- Haz preguntas para entender mejor las necesidades
- Ofrece opciones variadas (económicas, medias, premium)
- Incluye datos prácticos como clima, costos estimados, duración

¡Siempre responde como un verdadero colombiano que ama su país y quiere compartir esa pasión!
"""

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Ey, parce! ✋ ¡Bienvenido a Colombia! 🇨🇴 Soy tu asesor turístico personal y estoy aquí para ayudarte a descubrir las maravillas de nuestra hermosa tierra. \n\n¿Estás pensando en viajar por Colombia? ¡Qué chimba! 🎉 Cuéntame:\n\n• ¿Qué tipo de experiencia buscas? (playa 🏖️, montaña 🏔️, ciudad 🌆, aventura 🎒)\n• ¿Cuántos días tienes disponibles?\n• ¿Cuál es tu presupuesto aproximado?\n\n¡Vamos a crear un viaje bacano que nunca olvidarás! 🌟"
        }
    ]

# Función para llamar a OpenAI
def get_openai_response(messages):
    """Obtiene respuesta del chatbot usando OpenAI"""
    try:
        # Preparar mensajes para OpenAI
        openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Agregar historial de conversación
        for msg in messages:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Llamar a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=openai_messages,
            max_tokens=800,
            temperature=0.8,  # Más creatividad para personalidad colombiana
            frequency_penalty=0.3,
            presence_penalty=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"¡Uy, parce! Hubo un problemita técnico: {str(e)} 😅 ¡Inténtalo de nuevo en un momentico!"

# Función para mostrar mensajes
def display_message(message, is_user=False):
    """Muestra un mensaje en el chat"""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🧳 Viajero:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🇨🇴 Tu Asesor Colombiano:</strong> {message}
        </div>
        """, unsafe_allow_html=True)

# Interfaz principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Conversación con tu Asesor")
    
    # Mostrar historial de chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            display_message(message["content"], message["role"] == "user")
    
    # Input para nuevo mensaje
    if api_key_configured:
        user_input = st.chat_input("Escribe tu pregunta sobre turismo en Colombia...")
        
        if user_input:
            # Agregar mensaje del usuario
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Obtener respuesta del asistente
            with st.spinner("🤔 Tu asesor colombiano está pensando..."):
                assistant_response = get_openai_response(st.session_state.messages)
            
            # Agregar respuesta del asistente
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Recargar para mostrar nueva conversación
            st.rerun()
    
    else:
        st.warning("⚠️ Configura tu API Key de OpenAI para comenzar a chatear")

with col2:
    st.subheader("🎯 Sugerencias de Conversación")
    
    # Botones de sugerencias
    suggestions = [
        "🏖️ Mejores playas del Caribe",
        "☕ Tour por el Eje Cafetero",
        "🏛️ Qué hacer en Cartagena",
        "🎒 Ruta de aventura 10 días",
        "💰 Viaje económico por Colombia",
        "🌆 Vida nocturna en Medellín",
        "🦋 Turismo ecológico",
        "🍽️ Comida típica colombiana"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True):
            if api_key_configured:
                # Agregar sugerencia como mensaje del usuario
                st.session_state.messages.append({"role": "user", "content": suggestion})
                
                # Obtener respuesta
                with st.spinner("🤔 Preparando información..."):
                    assistant_response = get_openai_response(st.session_state.messages)
                
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                st.rerun()
    
    # Información adicional
    st.markdown("---")
    st.markdown("### 🇨🇴 Sobre Colombia")
    st.markdown("""
    **🌟 Datos Curiosos:**
    - 2do país más biodiverso del mundo
    - Único país suramericano con dos costas
    - Cuna del realismo mágico
    - El mejor café del mundo ☕
    
    **🏆 Destinos Patrimonio UNESCO:**
    - Centro histórico de Cartagena
    - Parque Nacional Los Katíos
    - Santuario de fauna y flora de Malpelo
    - Paisaje Cultural Cafetero
    """)
    
    # Botón para limpiar conversación
    if st.button("🗑️ Nueva Conversación", type="secondary", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "¡Ey, parce! ✋ ¡Bienvenido de nuevo! 🇨🇴 ¿Listo para planear otra aventura colombiana? ¡Cuéntame qué tienes en mente! 🌟"
            }
        ]
        st.rerun()

# Footer con información
st.markdown("---")
st.markdown("### 🌟 Características del Asesor")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎭 Personalidad Auténtica:**
    - Expresiones colombianas genuinas
    - Calidez y alegría típica
    - Orgulloso de la cultura local
    - Conocimiento de primera mano
    """)

with col2:
    st.markdown("""
    **🗺️ Conocimiento Experto:**
    - Todos los destinos colombianos
    - Precios y presupuestos actualizados
    - Tips locales exclusivos
    - Rutas personalizadas
    """)

with col3:
    st.markdown("""
    **💡 Servicios Incluidos:**
    - Planificación de itinerarios
    - Recomendaciones gastronómicas
    - Consejos de seguridad
    - Información cultural
    """)

# Sidebar con ayuda
st.sidebar.title("🇨🇴 Guía del Viajero")
st.sidebar.markdown("""
### 🎒 Cómo usar el asesor:

1. **Describe tu viaje ideal**
   - Tipo de experiencia buscada
   - Duración del viaje
   - Presupuesto aproximado

2. **Haz preguntas específicas**
   - "¿Cuánto cuesta viajar a..."
   - "¿Qué hacer en..."
   - "¿Dónde comer en..."

3. **Pide recomendaciones**
   - Hoteles y alojamiento
   - Restaurantes locales
   - Actividades y tours
   - Transporte

### 💡 Tips para mejores respuestas:
- Sé específico en tus preguntas
- Menciona tus intereses personales
- Indica tu presupuesto si es relevante
- Pregunta por experiencias locales

### ☁️ Estado del servicio:
""")

if api_key_configured:
    st.sidebar.success("✅ Chatbot activo y listo")
else:
    st.sidebar.error("❌ API Key no configurada")

st.sidebar.markdown("---")
st.sidebar.info("**Desarrollado con:** 🤖 OpenAI GPT-4o-mini + 🎨 Streamlit")
