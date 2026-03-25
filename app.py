import streamlit as st
import requests

st.title("Mi Chatbot DeepSeek 🤖")

# Usamos el secreto que configuraste en Streamlit
api_key = st.secrets["DEEPSEEK_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostramos el historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta..."):
    # Guardamos y mostramos lo que tú escribes
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Creamos un lugar para la respuesta de la IA
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                "https://openrouter.ai",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-r1:free", 
                    "messages": st.session_state.messages
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                # Sacamos la respuesta con seguridad
                full_response = data['choices'][0]['message']['content']
                st.markdown(full_response)
                # Solo guardamos en el historial si la respuesta fue exitosa
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"El servidor de IA está ocupado. Intenta de nuevo en un momento.")
                
        except Exception as e:
            st.error(f"Hubo un problema de conexión. Revisa si tu API Key es correcta.")

    with st.chat_message("assistant"):
        st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

