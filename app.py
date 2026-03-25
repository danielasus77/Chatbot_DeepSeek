import streamlit as st
import requests

st.title("Mi Chatbot DeepSeek 🤖")

# Usar el secreto que configuraste en Streamlit Cloud
api_key = st.secrets["DEEPSEEK_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
        
        # Esto evita el error que ves en la imagen
        if response.status_code == 200:
            data = response.json()
            full_response = data['choices'][0]['message']['content']
            with st.chat_message("assistant"):
                st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.error(f"Error del servidor: {response.text}")
            
    except Exception as e:
        st.error(f"Hubo un problema de conexión: {e}")

    with st.chat_message("assistant"):
        st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

