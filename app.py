import streamlit as st
import requests

st.set_page_config(page_title="Mi Chatbot DeepSeek", page_icon="🤖")
st.title("Mi Chatbot DeepSeek 🤖")

# 1. Verificar la API Key en la caja fuerte de Streamlit
if "DEEPSEEK_API_KEY" in st.secrets:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
else:
    st.error("Error: No configuraste 'DEEPSEEK_API_KEY' en los Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Petición técnica a OpenRouter
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
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                full_response = data['choices'][0]['message']['content']
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Servidor ocupado (Error {response.status_code}). Intenta de nuevo.")
        except Exception:
            st.error("Problema de conexión. Verifica tu llave en los Secrets.")
