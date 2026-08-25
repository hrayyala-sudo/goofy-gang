import random
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="centered")

# --- INITIALIZE VARIABLES ---
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if "guess_tries" not in st.session_state:
    st.session_state.guess_tries = 10
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --- MAIN DASHBOARD AREA ---
st.title("🎉 Goofy Gang Dashboard")
st.write("Welcome back to the portal!")

# --- GAME SECTION ---
st.header("🎲 Secret Number Game")
st.write(f"Guess the number between 1 and 100. Tries left: **{st.session_state.guess_tries}**")

if st.session_state.guess_tries > 0:
    guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1, key="game_guess")
    
    if st.button("Submit Guess", use_container_width=True):
        st.session_state.guess_tries -= 1
        if guess == st.session_state.secret_number:
            st.success(f"🥳 Awesome job! You guessed the secret number {st.session_state.secret_number}!")
            if st.button("Play Again"):
                st.session_state.secret_number = random.randint(1, 100)
                st.session_state.guess_tries = 10
                st.rerun()
        elif guess < st.session_state.secret_number:
            st.warning("Too low! Try a higher number.")
        else:
            st.warning("Too high! Try a lower number.")
else:
    st.error(f"💥 Game Over! The correct number was {st.session_state.secret_number}.")
    if st.button("Reset Game", use_container_width=True):
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.guess_tries = 10
        st.rerun()

st.divider()

# --- CHATBOX SECTION ---
st.header("💬 Goofy Chat Box")
st.write("Leave a message for the gang below!")

# Message history box
chat_container = st.container(height=300)
with chat_container:
    if not st.session_state.chat_messages:
        st.info("No messages yet. Be the first to say hello!")
    for msg in st.session_state.chat_messages:
        with st.chat_message("user"):
            st.write(f"**{msg['user']}**: {msg['text']}")

# Message text entry box
if prompt := st.chat_input("Type a message to the group..."):
    st.session_state.chat_messages.append({
        "user": "Pranav",
        "text": prompt
    })
    st.rerun()
