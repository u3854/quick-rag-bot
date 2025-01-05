import streamlit as st
from rag_bot.assistant.main import ChatBot

chat = ChatBot(platform="groq", model="mixtral-8x7b-32768", temperature=0.5)



def get_messages(messages):
    """
    Get the last user and assistant chat messages from the chat history.
    """
    return [(x["role"], x["content"]) for x in messages[-3:]]



######### PAGE CONFIG #########
st.set_page_config(
    page_title="RAG Bot",
    page_icon="🐒",
    layout="centered",
    initial_sidebar_state="auto"
)


######### CHAT BOX #########

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# chat interface
chat_interface = st.container(border=False)
message_container = chat_interface.container(border=True, height=480)
input_container = chat_interface.container()


with message_container:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if query := input_container.chat_input("Type a query..."):

    with message_container.chat_message("user"):
        st.markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display assistant response in chat message container
    with message_container.chat_message("assistant"):
        context = get_messages(st.session_state.messages)
        print("---> context:", context)
        response = st.write_stream(chat.stream_response(documents="", chat_messages=context))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})