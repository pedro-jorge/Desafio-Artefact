import streamlit as st

from src.agent import Agent

def main():
    agent = Agent()
    
    st.set_page_config(
        page_title="Chatbot Empório da Música",
        layout="wide",
    )
    st.title("Chatbot Empório da Música")
    
    st.session_state.setdefault("messages", [])
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    question = st.chat_input("Faça uma pergunta sobre o Empório da Música")
    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Consultando as informações da loja..."):
                response = agent.ask(question)["messages"][-1].content
        st.markdown(response)
    
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

if __name__ == "__main__":
    main()
        