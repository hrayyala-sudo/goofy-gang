import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🎉", layout="wide")

# User Credentials & Allowed Users
ALLOWED_USERS = ["Pranav", "Calvin", "Austin", "Goofy Member"]
CORRECT_PASSWORD = "goofy123"

# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "nickname" not in st.session_state:
    st.session_state["nickname"] = ""

# --- 2. GLOBAL CHAT STORAGE ---
@st.cache_resource
def get_global_chat():
    return []

global_chat = get_global_chat()

# --- 3. ORIGINAL LOGIN GATEWAY ---
def show_login_screen():
    st.title("🔒 Goofy Gang Portal Login")
    st.write("Welcome back! Please sign in to access the portal.")
    
    col1, _ = st.columns([1, 2])
    with col1:
        selected_user = st.selectbox("Select your name:", ALLOWED_USERS)
        custom_nickname = st.text_input("Or type a custom nickname (optional):")
        password = st.text_input("Enter Password:", type="password")
        
        if st.button("Log In", use_container_width=True):
            if password == CORRECT_PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["nickname"] = custom_nickname.strip() if custom_nickname.strip() else selected_user
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Incorrect password! Try again.")

if not st.session_state["logged_in"]:
    show_login_screen()
    st.stop()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title(f"👋 Welcome, {st.session_state['nickname']}!")

st.sidebar.markdown("### 👤 Profile Settings")
new_nick = st.sidebar.text_input("Change Nickname:", value=st.session_state["nickname"])
if st.sidebar.button("Save New Nickname"):
    st.session_state["nickname"] = new_nick
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📍 Navigation Pages")
page = st.sidebar.radio(
    "Go to page:",
    ["📍 Dashboard / Global Chat", "🎲 Guessing Game", "❌ Tic-Tac-Toe", "🪨 Rock Paper Scissors", "🚀 Asteroid Dodge"]
)

st.sidebar.markdown("---")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.session_state["nickname"] = ""
    st.rerun()

# --- 5. MAIN DASHBOARD ---
st.title("🎉 Goofy Gang Dashboard")
st.markdown("---")

# --- PAGE 1: DASHBOARD & GLOBAL CHAT ---
if page == "📍 Dashboard / Global Chat":
    st.header("💬 Goofy Chatbox")
    st.write("Welcome to the main chat room! Messages update for everyone.")

    if st.button("🔄 Refresh Messages"):
        st.rerun()

    chat_container = st.container()
    with chat_container:
        if not global_chat:
            st.info("No messages yet! Be the first to speak.")
        for msg in global_chat:
            with st.chat_message("user" if msg["sender"] == st.session_state["nickname"] else "assistant"):
                st.markdown(f"**{msg['sender']}** *({msg['time']})*")
                st.write(msg["text"])

    user_msg = st.chat_input("Say something goofy...")
    if user_msg:
        time_str = datetime.now().strftime("%I:%M %p")
        global_chat.append({
            "sender": st.session_state["nickname"],
            "text": user_msg,
            "time": time_str
        })
        st.rerun()

# --- PAGE 2: GUESSING GAME ---
elif page == "🎲 Guessing Game":
    st.header("🎲 Number Guessing Game")
    st.write("Guess the secret number between 1 and 100!")

    if "secret_num" not in st.session_state:
        st.session_state["secret_num"] = random.randint(1, 100)
        st.session_state["guesses"] = 0

    guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)
    if st.button("Submit Guess"):
        st.session_state["guesses"] += 1
        if guess < st.session_state["secret_num"]:
            st.warning("Too low! Try again.")
        elif guess > st.session_state["secret_num"]:
            st.warning("Too high! Try again.")
        else:
            st.balloons()
            st.success(f"🎉 You got it in {st.session_state['guesses']} tries! The secret number was {st.session_state['secret_num']}.")

    if st.button("New Game"):
        st.session_state["secret_num"] = random.randint(1, 100)
        st.session_state["guesses"] = 0
        st.rerun()

# --- PAGE 3: TIC-TAC-TOE ---
elif page == "❌ Tic-Tac-Toe":
    st.header("❌ Tic-Tac-Toe")

    if "board" not in st.session_state:
        st.session_state["board"] = [""] * 9
        st.session_state["turn"] = "❌"

    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            btn_label = st.session_state["board"][i] if st.session_state["board"][i] != "" else " "
            if st.button(btn_label, key=f"ttt_{i}", use_container_width=True):
                if st.session_state["board"][i] == "":
                    st.session_state["board"][i] = st.session_state["turn"]
                    st.session_state["turn"] = "⭕" if st.session_state["turn"] == "❌" else "❌"
                    st.rerun()

    if st.button("Reset Game"):
        st.session_state["board"] = [""] * 9
        st.session_state["turn"] = "❌"
        st.rerun()

# --- PAGE 4: ROCK PAPER SCISSORS ---
elif page == "🪨 Rock Paper Scissors":
    st.header("🪨 Rock Paper Scissors")

    choices = ["🪨 Rock", "📄 Paper", "✂️ Scissors"]
    user_choice = st.radio("Choose your move:", choices)

    if st.button("Play Turn"):
        bot_choice = random.choice(choices)
        st.write(f"**Bot chose:** {bot_choice}")

        if user_choice == bot_choice:
            st.info("It's a tie!")
        elif (
            (user_choice == "🪨 Rock" and bot_choice == "✂️ Scissors")
            or (user_choice == "📄 Paper" and bot_choice == "🪨 Rock")
            or (user_choice == "✂️ Scissors" and bot_choice == "📄 Paper")
        ):
            st.success("🎉 You win!")
        else:
            st.error(" You lose! Try again.")

# --- PAGE 5: ANIMATED ASTEROID DODGE ---
elif page == "🚀 Asteroid Dodge":
    st.header("🚀 Asteroid Dodge (Arcade Edition)")
    st.write("Dodge the falling space debris in real-time!")

    asteroid_game_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          background-color: #0e1117;
          color: white;
          font-family: sans-serif;
          text-align: center;
          margin: 0;
          padding: 10px;
        }
        #gameCanvas {
          background-color: #161b22;
          border: 2px solid #30363d;
          border-radius: 8px;
          display: block;
          margin: 0 auto;
        }
        .info {
          margin-top: 8px;
          font-size: 14px;
          color: #8b949e;
        }
      </style>
    </head>
    <body>

      <canvas id="gameCanvas" width="600" height="400"></canvas>
      <div class="info">Click screen once, then use <b>Left / Right Arrows</b> or <b>A / D</b> to move. Press <b>R</b> to restart.</div>

      <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let score = 0;
        let gameOver = false;

        const player = {
          x: canvas.width / 2 - 15,
          y: canvas.height - 40,
          width: 30,
          height: 30,
          speed: 6
        };

        let asteroids = [];
        let spawnRate = 35;
        let frameCount = 0;

        const keys = {};

        document.addEventListener("keydown", (e) => {
          keys[e.key] = true;
          if (gameOver && (e.key === "r" || e.key === "R")) {
            resetGame();
          }
        });

        document.addEventListener("keyup", (e) => {
          keys[e.key] = false;
        });

        function spawnAsteroid() {
          const size = Math.random() * 20 + 15;
          const x = Math.random() * (canvas.width - size);
          const speed = Math.random() * 2 + 2 + (score / 100);
          asteroids.push({ x, y: -size, size, speed });
        }

        function resetGame() {
          score = 0;
          asteroids = [];
          player.x = canvas.width / 2 - 15;
          gameOver = false;
          loop();
        }

        function update() {
          if (gameOver) return;

          if (keys["ArrowLeft"] || keys["a"] || keys["A"]) {
            player.x -= player.speed;
          }
          if (keys["ArrowRight"] || keys["d"] || keys["D"]) {
            player.x += player.speed;
          }

          if (player.x < 0) player.x = 0;
          if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;

          frameCount++;
          if (frameCount % spawnRate === 0) {
            spawnAsteroid();
          }

          for (let i = 0; i < asteroids.length; i++) {
            let a = asteroids[i];
            a.y += a.speed;

            if (
              player.x < a.x + a.size &&
              player.x + player.width > a.x &&
              player.y < a.y + a.size &&
              player.y + player.height > a.y
            ) {
              gameOver = true;
            }

            if (a.y > canvas.height) {
              asteroids.splice(i, 1);
              i--;
              score += 10;
            }
          }
        }

        function draw() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Ship
          ctx.fillStyle = "#ff4b4b";
          ctx.beginPath();
          ctx.moveTo(player.x + player.width / 2, player.y);
          ctx.lineTo(player.x, player.y + player.height);
          ctx.lineTo(player.x + player.width, player.y + player.height);
          ctx.closePath();
          ctx.fill();

          // Asteroids
          ctx.fillStyle = "#8b949e";
          asteroids.forEach(a => {
            ctx.beginPath();
            ctx.arc(a.x + a.size / 2, a.y + a.size / 2, a.size / 2, 0, Math.PI * 2);
            ctx.fill();
          });

          // Score
          ctx.fillStyle = "#ffffff";
          ctx.font = "16px sans-serif";
          ctx.fillText("Score: " + score, 15, 25);

          if (gameOver) {
            ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#ff4b4b";
            ctx.font = "bold 28px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 10);

            ctx.fillStyle = "#ffffff";
            ctx.font = "16px sans-serif";
            ctx.fillText("Final Score: " + score, canvas.width / 2, canvas.height / 2 + 20);
            ctx.fillText("Press 'R' to Play Again", canvas.width / 2, canvas.height / 2 + 50);
            ctx.textAlign = "left";
          }
        }

        function loop() {
          update();
          draw();
          if (!gameOver) {
            requestAnimationFrame(loop);
          }
        }

        loop();
      </script>
    </body>
    </html>
    """
    components.html(asteroid_game_html, height=520)
