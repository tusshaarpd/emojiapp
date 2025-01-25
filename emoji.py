import streamlit as st
import requests

# API Base URL
API_BASE_URL = "https://emojihub.yurace.pro/api/all"

# Function to fetch emoji data from the API
@st.cache_data
def fetch_emojis():
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching emojis: {e}")
        return []

# Function to find the closest matching emoji
def find_emoji_by_reaction(reaction, emojis):
    for emoji in emojis:
        if reaction.lower() in emoji['name'].lower():
            return emoji
    return None

# Streamlit App
st.title("Emoji Reaction App")
st.caption("Enter your emotion or reaction, and get the perfect emoji!")

# Input: User's reaction
reaction = st.text_input("Enter your reaction (e.g., happy, sad, hugging, etc.):", placeholder="Type your reaction here...")

# Fetch all emojis
with st.spinner("Fetching emojis..."):
    emoji_data = fetch_emojis()

# Handle the user's input
if st.button("Get Emoji"):
    if reaction.strip():
        emoji = find_emoji_by_reaction(reaction, emoji_data)
        if emoji:
            st.subheader(f"Emoji for '{reaction}':")
            st.write(f"**{emoji['name']}** ({', '.join(emoji['unicode'])})")
            st.markdown(f"<p style='font-size: 50px;'>{emoji['htmlCode'][0]}</p>", unsafe_allow_html=True)
        else:
            st.warning("No matching emoji found. Try a different reaction!")
    else:
        st.error("Please enter a reaction to get an emoji.")

# Footer
st.write("Powered by [EmojiHub API](https://emojihub.yurace.pro/)")
