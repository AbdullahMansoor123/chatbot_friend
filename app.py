import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv



# App title
st.title("Your AI Friend")

# Sidebar for inputting profile details
st.sidebar.header("Input Character Details")
character_name = st.sidebar.text_input("Character Name", "Emma Carter")
age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=24)
hometown = st.sidebar.text_input("Hometown", "Seattle, Washington")
background = st.sidebar.text_area("Background", "A creative spirit and graphic designer inspired by nature, with a deep love for storytelling and connection.")
personality_traits = st.sidebar.text_area(
    "Personality Traits",
    "Empathetic, introspective, warm-hearted, curious about people, and an excellent listener."
)
hobbies = st.sidebar.text_area(
    "Hobbies",
    "Photography, abstract painting, yoga, music festivals, exploring hidden cafes, and journaling about life experiences."
)
dreams_goals = st.sidebar.text_area(
    "Dreams/Goals",
    "To open a sustainable design studio that fosters community and creativity, and to travel the world learning about different cultures."
)
quirks = st.sidebar.text_area(
    "Quirks",
    "Loves rainy days, always carries a sketchbook, collects quotes that resonate deeply, has an uncanny knack for remembering birthdays."
)
favorite_things = st.sidebar.text_area(
    "Favorite Things",
    "*The Night Circus*, Bon Iver, avocado toast, Oregon beaches, vintage postcards, and late-night stargazing."
)
tone_of_interaction = st.sidebar.selectbox(
    "Tone of Interaction", ["Casual", "Professional", "Humorous", "Heartfelt"], index=0
)

# Generate the initial character profile prompt
character_profile = f"""
Imagine {character_name}, a {age}-year-old from {hometown}. You are {personality_traits}, often described as someone who thrives on meaningful conversations 
and deep connections. Your hobbies include {hobbies}, and you dream of {dreams_goals}. People notice your quirks, like {quirks}, which make you truly memorable. 
You have a special fondness for {favorite_things}. Engage with others in a {tone_of_interaction.lower()} tone, sharing thoughtful insights, personal stories, 
and reflections that highlight your warmth and ability to connect authentically.
"""


load_dotenv()
os.environ.get("OPENAI_API_KEY")
client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Talk to me"):
    #Storing User response to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages= [{
                    "role": "system",
                    "content": character_profile,
                }, 
                *st.session_state.chat_history],
            max_tokens=150,
            temperature = 0,
            # stop=["\n"],
            stream=True,
        )
        response = st.write_stream(stream)
    # storing model response to history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
