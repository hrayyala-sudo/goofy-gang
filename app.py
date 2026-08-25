import random
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="centered")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "allowed_users" not in st.session_state:
    st.session_state.allowed_users = ["Calvin", "Austin", "George", "Isaac", "Isaiah", "Fox", "Chris", "Leo", "Carson", "Soren", "Edward", "Pranav"]
if "theme_color" not in st.session_state:
    st.session_state.theme_color = "Default"
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if "guess_tries" not in st.session_state:
    st.session_state.guess_tries = 10
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🤪 Goofy Gang Portal")
    st.subheader("Please Login")
    
    user_input = st.text_input("Enter your name:", placeholder="Type your name here...")
    
    if st.button("Login", use_container_width=True):
        if user_input.strip() in st.session_state.allowed_users:
            st.session_state.logged_in = True
            st.session_state.username = user_input.strip()
            st.rerun()
        else:
            st.error("Name not found in the Goofy Gang list. Please try again!")

# --- MAIN PORTAL AREA ---
else:
    # Sidebar header and logout options
    st.sidebar.title(f"👋 Welcome, {st.session_state.username}!")
    
    # Restored theme selector functionality
    st.session_state.theme_color = st.sidebar.selectbox("Choose Theme Color:", ["Default", "Blue", "Green", "Dark"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
        
    st.title("🎉 Goofy Gang Dashboard")
    st.write(f"Welcome back to the portal dashboard, **{st.session_state.username}**!")
    
    # --- GAME SECTION (TOP) ---
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

    # --- CHATBOX SECTION (BOTTOM) ---
    st.header("💬 Goofy Chat Box")
    st.write("Leave a message for the gang below!")
    
    # Message history window
    chat_container = st.container(height=300)
    with chat_container:
        if not st.session_state.chat_messages:
            st.info("No messages yet. Be the first to say hello!")
        for msg in st.session_state.chat_messages:
            with st.chat_message("user"):
                st.write(f"**{msg['user']}**: {msg['text']}")

    # Chat entry form input
    if prompt := st.chat_input("Type a message to the group..."):
        st.session_state.chat_messages.append({
            "user": st.session_state.username,
            "text": prompt
        })
        st.rerun()
