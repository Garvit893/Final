import streamlit as st
from groq import Groq
import os
import requests
from bs4 import BeautifulSoup

api_key = st.secrets["groq"]["api_key"]
client = Groq(api_key=api_key)

WIKI_PAGE_URL = "https://en.wikipedia.org/wiki/Adrian_Carton_de_Wiart"

def fetch_wikipedia_content(url):
    """Fetch content from a Wikipedia page and return the main text."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        content = " ".join([para.get_text() for para in paragraphs])
        return content
    except Exception as e:
        st.error(f"An error occurred while fetching the Wikipedia page: {e}")
        return ""

def query_groq_api(prompt):
    """Submit a query to the GROQ API and get the response."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-8b-8192"  
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    wiki_content = fetch_wikipedia_content(WIKI_PAGE_URL)
    
    st.markdown("""
    <style>
    .main {
        background-color: #f0f0f0;
        background-image: url('https://images3.alphacoders.com/210/210105.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        padding: 20px;
    }
    .stButton>button {
        background-color: #0f4172;
        color: #FFFFFF;
        padding: 20px 20px;
        border: 2px solid #FFFFFF;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        height: 40px;
        float: right;
    }
    .stButton>button:hover {
        background-color: #073c5b;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #073c5b;
        color: white;
        text-align: center;
        padding: 10px 0;
    }
    .user-message {
        background-color: #31a889;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        text-align: left;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
    }
    .bot-response {
        background-color: #0f4172;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        text-align: left;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
    }
    .input-row {
        display: flex;
        align-items: center;
        margin-top: 20px;
    }
    .input-row input {
        flex: 1;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main">', unsafe_allow_html=True)

    #st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Lieutenant_Colonel_Adrian_Carton_de_Wiart.jpg/220px-Lieutenant_Colonel_Adrian_Carton_de_Wiart.jpg", image-align:center; width=200)
    
    st.markdown(
    """
    <h1 style='text-align: center;color: #ffffff;'>Welcome To Adrian Carton Chatbot</h1>
    # <h1 style='text-align: center;'></h1>
    """,
    unsafe_allow_html=True
)
    st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Lieutenant_Colonel_Adrian_Carton_de_Wiart.jpg/220px-Lieutenant_Colonel_Adrian_Carton_de_Wiart.jpg' width='200'>
    </div>
    """,
    unsafe_allow_html=True
)

    if "history" not in st.session_state:
        st.session_state.history = []

    for entry in st.session_state.history:
        st.markdown(f"<div class='user-message'>You: {entry['user']}</div>", unsafe_allow_html=True)
        if 'bot' in entry:
            st.markdown(f"<div class='bot-response'>Bot: {entry['bot']}</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="input-row">', unsafe_allow_html=True)
        user_message = st.text_input("Ask a question:", key="user_message")
        if st.button("Send"):
            if user_message:
                st.session_state.history.append({"user": user_message})

                prompt = f"Based on the information from this Wikipedia page: {wiki_content}\n\nUser question: {user_message}"
                
                prompt = (
    "You are an intelligent AI assistant dedicated to providing accurate and helpful information about Adrian Carton de Wiart. "
    "Your role is to engage with users and answer their questions based on the information from the Wikipedia page. "
    "Please answer all questions related to content of the Wikipedia page. "
    "If a question is unrelated to this content, reply with 'I don't have knowledge to this question.' "
    "Always ensure your answers are informative and relevant to Adrian Carton de Wiart and Wikipedia page.\n\n"
    f"Context: {wiki_content}\n\n"
    f"User question: {user_message}"
)
                
                bot_reply = query_groq_api(prompt)
                if bot_reply:
                    st.session_state.history[-1]['bot'] = bot_reply
                    st.markdown(f"<div class='bot-response'>Bot: {bot_reply}</div>", unsafe_allow_html=True)
                else:
                    st.error("Failed to get a response from the API.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
