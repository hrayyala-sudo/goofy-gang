import random
import streamlit as st
import os

# Set page configuration
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="centered")

# --- FILES TO SAVE DATA PERMANENTLY ---
PASSWORD_FILE = "saved_password.txt"
CHAT_FILE = "saved_chat.txt"

# Helper functions to read/write files locally in the cloud directory
def load_saved_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            return f.read().strip()
    return "goofy123"  # Default password if file doesn't exist yet

def save_new_password(new_pwd):
    with open(PASSWORD_FILE, "w") as f:
        f.write(new_pwd.strip())

def load_saved_chat():
    messages = []
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "|||" in line:
                    user, text = line.strip().split("|||", 1)
                    messages.append({"user": user, "text": text})
    return messages

def append_saved_chat(user, text):
    with open(CHAT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user}|||{text}\n")

# --- INITIALIZE RUNTIME VARIABLES ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "allowed_users" not in st.session_state:
    st.session_state.allowed_users = ["Calvin", "Austin", "George", "Isaac", "Isaiah", "Fox", "Chris", "Leo", "Carson", "Soren", "Edward", "Pranav"]
if "text_color" not in st.session_state:
    st.session_state.text_color = "#31333F"
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if "guess_tries" not in st.session_state:
    st.session_state.guess_tries = 10

# Load values from persistent files
master_password = load_saved_password()

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🤪 Goofy Gang Portal")
    st.subheader("Please Login")
    
    user_input = st.text_input("Enter your name:", placeholder="Type your name here...")
    password_input = st.text_input("Enter Portal Password:", type="password", placeholder="Enter secret password...")
    
    if st.button("Login", use_container_width=True):
        cleaned_name = user_input.strip()
        if cleaned_name in st.session_state.allowed_users and password_input == master_password:
            st.session_state.logged_in = True
            st.session_state.username = cleaned_name
            st.success("Access Granted!")
            st.rerun()
        elif cleaned_name not in st.session_state.allowed_users:
            st.error("Name not found in the Goofy Gang list.")
        else:
            st.error("Incorrect password!")

# --- MAIN DASHBOARD INTERFACE ---
else:
    st.sidebar.title(f"👋 Welcome, {st.session_state.username}!")
    
    # Calvin's Admin tool updates the password file instantly
    if st.session_state.username == "Calvin":
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔑 Admin Settings")
        new_pwd = st.sidebar.text_input("Change Global App Password:", value=master_password, type="password")
        if st.sidebar.button("Update Permanent Password", use_container_width=True):
            save_new_password(new_pwd)
            st.sidebar.success("Password updated permanently!")
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 Customization")
    chosen_text_color = st.sidebar.color_picker("Pick App Text Color:", st.session_state.text_color)
    st.session_state.text_color = chosen_text_color
    
    st.markdown(
        f"""
        <style>
        .stApp, .stMarkdown p, h1, h2, h3, span {{
            color: {st.session_state.text_color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
        
    st.title("🎉 Goofy Gang Dashboard")
    st.write(f"Session authenticated for: **{st.session_state.username}**")
    
    # --- GAME SECTION ---
    st.header("🎲 Secret Number Game")
    st.write(f"Guess the number between 1 and 100. Tries left: **{st.session_state.guess_tries}**")
    
    if st.session_state.guess_tries > 0:
        guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1, key="game_guess")
        if st.button("Submit Guess", use_container_width=True):
            st.session_state.guess_tries -= 1
            if guess == st.session_state.secret_number:
                st.success(f"🥳 Awesome job! The number was {st.session_state.secret_number}!")
            elif guess < st.session_state.secret_number:
                st.warning("Too low!")
            else:
                st.warning("Too high!")
    else:
        st.error(f"💥 Game Over! The number was {st.session_state.secret_number}.")
        if st.button("Reset Game", use_container_width=True):
            st.session_state.secret_number = random.randint(1, 100)
            st.session_state.guess_tries = 10
            st.rerun()

    st.divider()

    # --- PERMANENT CHATBOX SECTION ---
    st.header("💬 Goofy Chat Box")
    
    # Load messages directly from the local file storage
    live_messages = load_saved_chat()
    
    chat_container = st.container(height=300)
    with chat_container:
        if not live_messages:
            st.info("No messages saved yet. Type below to start the conversation!")
        for msg in live_messages:
            with st.chat_message("user"):
                st.write(f"**{msg['user']}**: {msg['text']}")

    if prompt := st.chat_input("Type a message to the group..."):
        append_chat_message = append_saved_chat(st.session_state.username, prompt)
        st.rerun()
