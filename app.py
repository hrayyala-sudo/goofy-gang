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

# --- GAME SESSION STATES ---
# Secret Number Game
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if "guess_tries" not in st.session_state:
    st.session_state.guess_tries = 10

# Tic-Tac-Toe
if "ttt_board" not in st.session_state:
    st.session_state.ttt_board = [" "] * 9
if "ttt_turn" not in st.session_state:
    st.session_state.ttt_turn = "X"
if "ttt_winner" not in st.session_state:
    st.session_state.ttt_winner = None

# Rock Paper Scissors Trackers
if "rps_user_score" not in st.session_state:
    st.session_state.rps_user_score = 0
if "rps_ai_score" not in st.session_state:
    st.session_state.rps_ai_score = 0


# --- GLITCH-PROOF TIC-TAC-TOE HELPERS ---
def check_ttt_winner(b):
    # Checking Rows
    if b[0] == b[1] == b[2] != " ": return b[0]
    if b[3] == b[4] == b[5] != " ": return b[3]
    if b[6] == b[7] == b[8] != " ": return b[6]
    # Checking Columns
    if b[0] == b[3] == b[6] != " ": return b[0]
    if b[1] == b[4] == b[7] != " ": return b[1]
    if b[2] == b[5] == b[8] != " ": return b[2]
    # Checking Diagonals
    if b[0] == b[4] == b[8] != " ": return b[0]
    if b[2] == b[4] == b[6] != " ": return b[2]
    # Checking for Tie
    if " " not in b:
        return "Tie"
    return None


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
    # --- SIDEBAR CONTROL PANEL ---
    st.sidebar.title(f"👋 Welcome, {st.session_state.username}!")
    
    # Username Change Option
    st.sidebar.subheader("👤 Profile Settings")
    new_username_input = st.sidebar.text_input("Change Nickname:", value=st.session_state.username)
    if st.sidebar.button("Save New Nickname", use_container_width=True):
        if new_username_input.strip():
            st.session_state.username = new_username_input.strip()
            st.sidebar.success("Username updated!")
            st.rerun()

    # Sidebar Clickable Dot Navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("📍 Navigation Pages")
    page_selection = st.sidebar.radio(
        "Go to page:",
        ["💬 Goofy Chatbox", "🎲 Guessing Game", "❌ Tic-Tac-Toe", "🪨 Rock Paper Scissors"]
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
        .stApp, .stMarkdown p, h1, h2, h3, span, label {{
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
    
    # PAGE 1: CHATBOX
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

    # PAGE 2: GUESSING GAME
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

    # PAGE 3: TIC-TAC-TOE
    elif page_selection == "❌ Tic-Tac-Toe":
        st.header("❌ Tic-Tac-Toe")
        st.write(f"Current Turn: **{st.session_state.ttt_turn}**")
        
        # Display the grid using 3 layout columns
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                button_label = st.session_state.ttt_board[idx]
                
                # Make empty cells clickable, otherwise show letter
                if button_label == " " and st.session_state.ttt_winner is None:
                    if cols[col].button(" ", key=f"ttt_{idx}", use_container_width=True):
                        st.session_state.ttt_board[idx] = st.session_state.ttt_turn
                        winner = check_ttt_winner(st.session_state.ttt_board)
                        if winner:
                            st.session_state.ttt_winner = winner
                        else:
                            st.session_state.ttt_turn = "O" if st.session_state.ttt_turn == "X" else "X"
                        st.rerun()
                else:
                    cols[col].button(button_label, key=f"ttt_{idx}", disabled=True, use_container_width=True)
                    
        if st.session_state.ttt_winner:
            if st.session_state.ttt_winner == "Tie":
                st.info("🤝 It's a draw tie game!")
            else:
                st.success(f"🎉 Winner is Player: **{st.session_state.ttt_winner}**!")
                
            if st.button("Reset Grid", use_container_width=True):
                st.session_state.ttt_board = [" "] * 9
                st.session_state.ttt_turn = "X"
                st.session_state.ttt_winner = None
                st.rerun()

    # PAGE 4: ROCK PAPER SCISSORS
    elif page_selection == "🪨 Rock Paper Scissors":
        st.header("🪨 Rock Paper Scissors")
        st.write(f"🏆 Scoreboard — **You**: {st.session_state.rps_user_score} | **AI Bot**: {st.session_state.rps_ai_score}")
        
        choices = ["Rock", "Paper", "Scissors"]
        user_choice = st.selectbox("Pick your weapon:", choices)
        
        if st.button("Shoot!", use_container_width=True):
            ai_choice = random.choice(choices)
            st.info(f"🤖 AI bot chose: **{ai_choice}**")
            
            if user_choice == ai_choice:
                st.warning("👔 It's a tie match!")
            elif (user_choice == "Rock" and ai_choice == "Scissors") or \
                 (user_choice == "Paper" and ai_choice == "Rock") or \
                 (user_choice == "Scissors" and ai_choice == "Paper"):
                st.success("🔥 You win this round!")
                st.session_state.rps_user_score += 1
            else:
                st.error("💀 AI wins this round!")
                st.session_state.rps_ai_score += 1
                
