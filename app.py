import streamlit as st
import requests

st.set_page_config(page_title="Mi Chatbot DeepSeek", page_icon="🤖")
st.title("Mi Chatbot DeepSeek 🤖")

# 1. Verificación de la API Key en Secrets
if "DEEPSEEK_API_KEY" in st.secrets:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
else:
    st.error("Error: No encontré la clave 'DEEPSEEK_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 2. Inicializar el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Respuesta del asistente
    with st.chat_message("assistant"):
        try:
            # Petición a OpenRouter (URL completa y correcta)
            response = requests.post(
                url="https://openrouter.ai",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-r1:free", 
                    "messages": st.session_state.messages
                },
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                # Extraer el contenido con el índice [0]
                full_response = data['choices'][0]['message']['content']
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"El servidor respondió con error {response.status_code}. Intenta de nuevo.")
                
        except Exception as e:
            st.error("Hubo un problema de conexión. Verifica tu API Key o intenta más tarde.")


