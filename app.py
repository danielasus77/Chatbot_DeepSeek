import streamlit as st
import requests

st.set_page_config(page_title="Mi Chatbot DeepSeek", page_icon="🤖")
st.title("Mi Chatbot DeepSeek 🤖")

# 1. Obtener la llave de los Secrets
if "DEEPSEEK_API_KEY" in st.secrets:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
else:
    st.error("Falta la clave 'DEEPSEEK_API_KEY' en los Secrets.")
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
            # 2. Petición corregida
            response = requests.post(
                url="https://openrouter.ai",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                   "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
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
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception:
            st.error("Hubo un problema de conexión. Revisa tus Secrets.")
