from langchain_groq import ChatGroq


def chat_groq(
        model="mixtral-8x7b-32768", 
        temperature=0.5,
        ) -> ChatGroq:

    return ChatGroq(model=model, temperature=temperature, streaming=True)


