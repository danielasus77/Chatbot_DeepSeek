import streamlit as st
import requests

st.title("Mi Chatbot DeepSeek 🤖")
api_key = "TU_API_KEY_AQUÍ" # Pon tu llave real aquí

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        "https://openrouter.ai",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": "deepseek/deepseek-r1:free", "messages": st.session_state.messages}
    )

    full_response = response.json()['choices'][0]['message']['content']
    with st.chat_message("assistant"):
        st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

