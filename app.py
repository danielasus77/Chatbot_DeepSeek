import streamlit as st
import requests

st.title("Mi Chatbot DeepSeek 🤖")

# Usamos el secreto configurado en Streamlit
if "DEEPSEEK_API_KEY" in st.secrets:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
else:
    st.error("Falta la API Key en los Secrets de Streamlit.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
                },
                timeout=10 # Evita que se quede esperando por siempre
            )
            
            if response.status_code == 200:
                data = response.json()
                # El [0] es vital aquí:
                full_response = data['choices'][0]['message']['content']
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"El servidor está saturado. Código: {response.status_code}")
                
        except Exception as e:
            st.error("Hubo un problema de conexión. Intenta de nuevo en unos segundos.")
}

