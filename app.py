import streamlit as st
import requests

st.set_page_config(page_title="Mi Chatbot DeepSeek", page_icon="🤖")
st.title("Mi Chatbot DeepSeek 🤖")

# ESTA LÍNEA ES LA CLAVE:
# No pongas tu sk-or-v1... aquí. Déjalo exactamente así:
api_key = st.secrets["DEEPSEEK_API_KEY"]

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
                full_response = data['choices'][0]['message']['content']
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Error {response.status_code}. El servidor está saturado.")
        except Exception as e:
            st.error("Hubo un problema de conexión.")


