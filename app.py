import random
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="centered")

# --- DEFINE CENTRAL STORAGE STRUCTURES (ERROR-FREE CACHING) ---
if "master_password" not in st.session_state:
    st.session_state.master_password = "goofy123"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
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

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🤪 Goofy Gang Portal")
    st.subheader("Please Login")
    
    user_input = st.text_input("Enter your name:", placeholder="Type your name here...")
    password_input = st.text_input("Enter Portal Password:", type="password", placeholder="Enter secret password...")
    
    if st.button("Login", use_container_width=True):
        cleaned_name = user_input.strip()
        if cleaned_name in st.session_state.allowed_users and password_input == st.session_state.master_password:
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
    
    # NEW: Sidebar Clickable Dot Navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("📍 Navigation Pages")
    page_selection = st.sidebar.radio(
        "Go to page:",
        ["💬 Goofy Chatbox", "🎲 Guessing Game"]
    )
    
    # Calvin's Admin setup updates the state password instantly
    if st.session_state.username == "Calvin":
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔑 Admin Settings")
        new_pwd = st.sidebar.text_input("Change Global App Password:", value=st.session_state.master_password, type="password")
        if st.sidebar.button("Update Permanent Password", use_container_width=True):
            st.session_state.master_password = new_pwd
            st.sidebar.success("Password updated!")
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
    
    # --- RENDER THE PAGE CHOSEN VIA SIDEBAR DOTS ---
    if page_selection == "💬 Goofy Chatbox":
        st.header("💬 Goofy Chat Box")
        st.write("Leave a message for the gang!")
        
        chat_container = st.container(height=350)
        with chat_container:
            if not st.session_state.chat_messages:
                st.info("No messages saved yet. Type below to start the conversation!")
            for msg in st.session_state.chat_messages:
                with st.chat_message("user"):
                    st.write(f"**{msg['user']}**: {msg['text']}")

        if prompt := st.chat_input("Type a message to the group..."):
            st.session_state.chat_messages.append({"user": st.session_state.username, "text": prompt})
            st.rerun()

    elif page_selection == "🎲 Guessing Game":
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
            st.error(f"💥 Game Over! The correct number was {st.session_state.secret_number}.")
            if st.button("Reset Game", use_container_width=True):
                st.session_state.secret_number = random.randint(1, 100)
                st.session_state.guess_tries = 10
                st.rerun()
