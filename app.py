import random
import streamlit as st

st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="centered")

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
if "ttt_board" not in st.session_state:
    st.session_state.ttt_board = [" "] * 9
if "ttt_player" not in st.session_state:
    st.session_state.ttt_player = "X"
if "ttt_winner" not in st.session_state:
    st.session_state.ttt_winner = None

color_map = {
    "Default": "#FFFFFF",
    "Cyan": "#00FFFF",
    "Green": "#00FF00",
    "Yellow": "#FFFF00"
}
selected_hex = color_map[st.session_state.theme_color]

st.markdown(
    f"""
    <style>
    html, body, [data-testid="stWidgetLabel"] p, .stMarkdown p {{
        color: {selected_hex} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if not st.session_state.logged_in:
    st.title("🤪 Goofy Gang Login Page")
    
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if pass_input == "5845" and user_input in st.session_state.allowed_users:
            st.session_state.logged_in = True
            st.session_state.username = user_input
            st.rerun()
        else:
            st.error("Access denied. Invalid username or password.")

else:
    st.title(f"👋 Welcome to the Portal, {st.session_state.username}!")
    
    menu = st.sidebar.radio(
        "=== Main Menu ===",
        ["Members List", "Games Hub", "Settings", "Account Actions", "About Creator", "Log Out"]
    )
    
    if menu == "Members List":
        st.header("--- All Members of Goofy Gang ---")
        for member in st.session_state.allowed_users:
            st.write(f"• {member}")
            
    elif menu == "Games Hub":
        st.header("🎮 Games Hub")
        game_choice = st.selectbox("Choose a game:", ["Select a game...", "Number Guessing", "Rock Paper Scissors", "Tic Tac Toe"])
        
        if game_choice == "Number Guessing":
            st.subheader("🔢 Number Guessing Game")
            st.write(f"I'm thinking of a number between 1 and 100. Tries left: **{st.session_state.guess_tries}**")
            
            guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1, key="num_guess")
            if st.button("Submit Guess"):
                if guess == st.session_state.secret_number:
                    st.success("🎉 Congratulations! You guessed the number.")
                    st.session_state.secret_number = random.randint(1, 100)
                    st.session_state.guess_tries = 10
                else:
                    st.session_state.guess_tries -= 1
                    if st.session_state.guess_tries <= 0:
                        st.error(f"Game Over! The number was {st.session_state.secret_number}.")
                        st.session_state.secret_number = random.randint(1, 100)
                        st.session_state.guess_tries = 10
                    elif guess < st.session_state.secret_number:
                        st.info("Too low! Try again.")
                    else:
                        st.info("Too high! Try again.")
                        
        elif game_choice == "Rock Paper Scissors":
            st.subheader("✊ Rock Paper Scissors")
            user_move = st.selectbox("Choose your move:", ["Rock", "Paper", "Scissors"])
            
            if st.button("Play"):
                ai_move = random.choice(["Rock", "Paper", "Scissors"])
                st.write(f"Computer chose: **{ai_move}**")
                
                if user_move == ai_move:
                    st.info("It's a tie!")
                elif (user_move == "Rock" and ai_move == "Scissors") or \
                     (user_move == "Paper" and ai_move == "Rock") or \
                     (user_move == "Scissors" and ai_move == "Paper"):
                    st.success("You win! 🏆")
                else:
                    st.error("You lose! 🤖")
                    
        elif game_choice == "Tic Tac Toe":
            st.subheader("❌ Tic Tac Toe ⭕")
            
            def check_ttt_winner(b):
                lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
                for combo in lines:
                    if b[combo] == b[combo] == b[combo] != " ":
                        return b[combo]
                if " " not in b:
                    return "Tie"
                return None

            cols = st.columns(3)
            for i in range(9):
                with cols[i % 3]:
                    button_label = st.session_state.ttt_board[i] if st.session_state.ttt_board[i] != " " else "—"
                    if st.button(button_label, key=f"ttt_{i}", disabled=st.session_state.ttt_winner is not None):
                        if st.session_state.ttt_board[i] == " ":
                            st.session_state.ttt_board[i] = st.session_state.ttt_player
                            winner = check_ttt_winner(st.session_state.ttt_board)
                            if winner:
                                st.session_state.ttt_winner = winner
                            else:
                                st.session_state.ttt_player = "O" if st.session_state.ttt_player == "X" else "X"
                            st.rerun()
            
            if st.session_state.ttt_winner:
                if st.session_state.ttt_winner == "Tie":
                    st.info("It's a tie game!")
                else:
                    st.success(f"Player {st.session_state.ttt_winner} wins!")
                if st.button("Reset Board"):
                    st.session_state.ttt_board = [" "] * 9
                    st.session_state.ttt_player = "X"
                    st.session_state.ttt_winner = None
                    st.rerun()
                    
    elif menu == "Settings":
        st.header("⚙️ Interface Settings")
        chosen_color = st.selectbox("Select Site Text Color:", ["Default", "Cyan", "Green", "Yellow"])
        if st.button("Apply Color Theme"):
            st.session_state.theme_color = chosen_color
            st.rerun()
            
    elif menu == "Account Actions":
        st.header("🛠️ Account Actions")
        old_user = st.text_input("Confirm old username:")
        new_user = st.text_input("Enter new username:")
        
        if st.button("Update Username"):
            if old_user == st.session_state.username:
                if new_user not in st.session_state.allowed_users:
                    idx = st.session_state.allowed_users.index(old_user)
                    st.session_state.allowed_users[idx] = new_user
                    st.session_state.username = new_user
                    st.success(f"Username successfully updated to {new_user}!")
                else:
                    st.error("That username already exists.")
            else:
                st.error("The old username does not match your active session profile.")
                
    elif menu == "About Creator":
        st.header("ℹ️ Information")
        st.write("In 2026, this program was designed by **Pranav** and is live at version **1.0**.")
        st.write("The Goofy Gang was established in 2025 by **Calvin**, who remains its primary administrator.")
        
    elif menu == "Log Out":
        st.write("Disconnecting session profile...")
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
