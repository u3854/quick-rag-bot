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
        response = st.write_stream(chat.stream_response(documents="""ffmpeg \-i original.mov \-filter:v alphaextract mask.mov
ffmpeg \-i original.mov \-i mask.mov \-filter\_complex "hstack" \-codec:v vp8 \-crf 10 output.webm

Movies are supported on the Web platform, but the list of supported codecs differs from browser to browser. For cross-browser compatibility (especially to support Safari), the most efficient combination is H.264 with MP3 (or AAC) in a MP4 file. However, Ren'Py does not support H.264 decoding (or AAC), so this combination can only work on the Web platform.

## Fullscreen Movies [link](#fullscreen-movies "Permalink to this heading")

The easiest and most efficient way to display a movie fullscreen is to use the [`renpy.movie_cutscene()`](#renpy.movie_cutscene "renpy.movie_cutscene") function. This function displays the movie fullscreen until it either ends, or the player clicks to dismiss it.

$ renpy.movie\_cutscene("On\_Your\_Mark.webm")

## Movie Displayables and Movie Sprites [link](#movie-displayables-and-movie-sprites "Permalink to this heading")

The Movie displayable can be used to display a movie anywhere Ren'Py can show a displayable. For example, a movie can be displayed as the background of a menu screen, or as a background.

The Movie displayable can also be used to define a movie sprite, which is a sprite that is backed by two movies. The primary movie provides the color of the sprite. A second movie, the mask movie, provides the alpha channel, with white being full opacity and black being full transparency.

Movies played by the Movie displayable loop automatically.

Here's an example of defining a movie sprite:

image eileen movie \= Movie(play\="eileen\_movie.webm", side\_mask\=True)""", chat_messages=context))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})