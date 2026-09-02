import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="wide")

# Allowed Users & Password
ALLOWED_USERS = ["pranav", "calvin", "austin", "goofy member"]
CORRECT_PASSWORD = "goofy123"

# Initialize Base Session State
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "nickname" not in st.session_state:
    st.session_state["nickname"] = ""
if "show_secret_game" not in st.session_state:
    st.session_state["show_secret_game"] = False
if "tetris_unlocked" not in st.session_state:
    st.session_state["tetris_unlocked"] = False
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "💬 Goofy Chatbox"

# --- HANDLE SECRET GAME UNLOCK VIA QUERY PARAM ---
if st.query_params.get("boss_defeated") == "true":
    st.session_state["tetris_unlocked"] = True
    st.session_state["show_secret_game"] = False
    st.session_state["active_page"] = "🔴 Tetris"
    st.session_state["nav_radio"] = "🔴 Tetris"  # Force radio key sync
    st.query_params.clear()
    st.balloons()
    st.rerun()

# --- 2. GLOBAL CHAT STORAGE ---
@st.cache_resource
def get_global_chat():
    return []

global_chat = get_global_chat()

# --- 3. LOGIN SCREEN ---
def show_login_screen():
    _, center_col, _ = st.columns([1, 1, 1])
    with center_col:
        st.title("🤪 Goofy Gang Portal Login")
        st.caption("Please sign in to access the portal.")

        user_input = st.text_input("Enter Your Name:", key="login_name")
        pass_input = st.text_input("Enter Password:", type="password", key="login_pass")

        if st.button("Login", use_container_width=True):
            clean_username = user_input.strip().lower()
            if clean_username in ALLOWED_USERS and pass_input == CORRECT_PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["nickname"] = user_input.strip()
                st.success(f"Welcome, {user_input.strip()}!")
                st.rerun()
            elif clean_username not in ALLOWED_USERS:
                st.error("Name not recognized! Please enter an authorized name.")
            else:
                st.error("Incorrect password!")

# STOP RUNNING SCRIPT IF NOT LOGGED IN
if not st.session_state["logged_in"]:
    show_login_screen()
    st.stop()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.caption(f"Logged in as **{st.session_state['nickname']}**")

st.sidebar.markdown("**Profile Settings**")
new_nick = st.sidebar.text_input("Change Nickname:", value=st.session_state["nickname"], label_visibility="collapsed")
if st.sidebar.button("Save Nickname"):
    st.session_state["nickname"] = new_nick
    st.rerun()

st.sidebar.divider()
st.sidebar.markdown("**Pages**")

# Build dynamic navigation list
pages_list = ["💬 Goofy Chatbox", "🎲 Guessing Game", "❌ Tic-Tac-Toe", "🪨 Rock Paper Scissors", "🚀 Asteroid Dodge", "🟡 Pac-Man"]
if st.session_state["tetris_unlocked"]:
    pages_list.append("🔴 Tetris")

# Keep active page valid
if st.session_state["active_page"] not in pages_list:
    st.session_state["active_page"] = pages_list[0]

# Ensure the key for nav_radio is aligned with active_page
if "nav_radio" not in st.session_state or st.session_state["nav_radio"] not in pages_list:
    st.session_state["nav_radio"] = st.session_state["active_page"]

def on_nav_change():
    st.session_state["active_page"] = st.session_state["nav_radio"]

# Render navigation radio
page = st.sidebar.radio(
    "Navigation",
    pages_list,
    key="nav_radio",
    on_change=on_nav_change,
    label_visibility="collapsed"
)

st.sidebar.divider()
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["nickname"] = ""
    st.rerun()

# --- 5. MAIN HEADER WITH ENLARGED EMOJI BUTTON ---
st.markdown("""
<style>
div.stButton > button[kind="secondary"] {
    font-size: 38px !important;
    height: 65px !important;
    line-height: 1 !important;
    padding: 0px !important;
    background: transparent !important;
    border: none !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px dashed #ff4b4b !important;
}
</style>
""", unsafe_allow_html=True)

title_col1, title_col2 = st.columns([0.12, 0.88])

with title_col1:
    if st.button("🤪", key="boss_toggle_btn", help="Click to trigger the Secret Boss Fight!"):
        st.session_state["show_secret_game"] = not st.session_state["show_secret_game"]
        st.rerun()

with title_col2:
    st.title("Goofy Gang Dashboard")

st.markdown("---")

# Banner message when Tetris is unlocked
if st.session_state["tetris_unlocked"] and page == "🔴 Tetris":
    st.success("🏆 **BOSS DEFEATED!** Tetris is now unlocked in your sidebar!")

# --- SECRET GOOFY BOSS GAME OVERLAY ---
if st.session_state["show_secret_game"]:
    st.info("🎉 **SECRET UNLOCKED!** Defeat the Goofy Boss to unlock a permanent arcade game!")
    
    secret_game_html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background-color: #161b22; color: white; font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 15px; border: 3px dashed #ff4b4b; border-radius: 12px; }
    .boss-target { font-size: 80px; cursor: pointer; user-select: none; display: inline-block; transition: transform 0.05s ease; margin: 15px 0; }
    .boss-target:active { transform: scale(1.3) rotate(15deg); }
    .health-bar-container { width: 80%; height: 24px; background-color: #30363d; border-radius: 12px; margin: 10px auto; overflow: hidden; border: 2px solid #ffffff; }
    .health-bar { width: 100%; height: 100%; background: linear-gradient(90deg, #ff4b4b, #ff8c00); transition: width 0.1s ease; }
    .stats { font-size: 18px; font-weight: bold; }
    .win-msg { color: #00ff00; font-size: 26px; font-weight: bold; }
    button { background-color: #238636; color: white; border: none; padding: 8px 16px; font-size: 14px; border-radius: 6px; cursor: pointer; margin-top: 10px; }
  </style>
</head>
<body>
  <h3>💥 DEFEAT THE GOOFY BOSS!</h3>
  <p style="color: #8b949e; margin: 0;">Tap the emoji 25 times before time runs out!</p>

  <div class="health-bar-container">
    <div id="hpBar" class="health-bar"></div>
  </div>

  <div id="target" class="boss-target" onclick="hitBoss()">🤪</div>

  <div class="stats">
    <span id="scoreText">Hits: 0 / 25</span> | 
    <span id="timerText">Time Left: 10s</span>
  </div>

  <div id="resultText"></div>

  <script>
    let hits = 0;
    const maxHits = 25;
    let timeLeft = 10;
    let gameActive = true;
    let timer = null;

    function startTimer() {
      timer = setInterval(() => {
        if (!gameActive) return;
        timeLeft--;
        document.getElementById("timerText").innerText = "Time Left: " + timeLeft + "s";
        if (timeLeft <= 0) endGame(false);
      }, 1000);
    }

    function hitBoss() {
      if (!gameActive) return;
      hits++;
      const hpPercent = Math.max(0, 100 - (hits / maxHits * 100));
      document.getElementById("hpBar").style.width = hpPercent + "%";
      document.getElementById("scoreText").innerText = "Hits: " + hits + " / " + maxHits;
      if (hits >= maxHits) endGame(true);
    }

    function endGame(won) {
      gameActive = false;
      clearInterval(timer);
      const res = document.getElementById("resultText");
      const target = document.getElementById("target");

      if (won) {
        target.innerText = "😵‍💫";
        res.innerHTML = "<div class='win-msg'>🏆 YOU SMASHED THE GOOFY BOSS! Launching Tetris...</div>";
        setTimeout(() => {
          try {
            window.top.location.href = window.top.location.pathname + "?boss_defeated=true";
          } catch (e) {
            window.location.search = "?boss_defeated=true";
          }
        }, 500);
      } else {
        target.innerText = "🤡";
        res.innerHTML = "<div style='color: #ff4b4b; font-size: 20px; font-weight: bold;'>⏰ TIME EXPIRED! The Boss Escaped!</div><button onclick='resetGame()'>Try Again</button>";
      }
    }

    function resetGame() {
      hits = 0;
      timeLeft = 10;
      gameActive = true;
      document.getElementById("target").innerText = "🤪";
      document.getElementById("hpBar").style.width = "100%";
      document.getElementById("scoreText").innerText = "Hits: 0 / " + maxHits;
      document.getElementById("timerText").innerText = "Time Left: 10s";
      document.getElementById("resultText").innerHTML = "";
      clearInterval(timer);
      startTimer();
    }

    startTimer();
  </script>
</body>
</html>"""
    components.html(secret_game_html, height=290)

# --- PAGE 1: GOOFY CHATBOX ---
if page == "💬 Goofy Chatbox":
    st.header("💬 Goofy Chatbox")
    st.write("Welcome to the main chat room! Messages update for everyone.")

    if st.button("🔄 Refresh Messages"):
        st.rerun()

    # --- CALVIN MODERATION CONTROLS ---
    if st.session_state["nickname"].strip().lower() == "calvin":
        with st.expander("👑 Calvin's Admin Chat Controls", expanded=True):
            st.write("Manage chat messages below:")
            
            if global_chat:
                col_del_spec, col_del_all = st.columns([2, 1])
                
                with col_del_spec:
                    options = [f"[{i}] {m['sender']}: {m['text'][:30]}..." for i, m in enumerate(global_chat)]
                    selected_msg = st.selectbox("Select message to delete:", options, key="admin_del_select")
                    if st.button("Delete Selected Message"):
                        idx = int(selected_msg.split("]")[0].replace("[", ""))
                        del global_chat[idx]
                        st.success("Message deleted!")
                        st.rerun()

                with col_del_all:
                    st.write("")
                    st.write("")
                    if st.button("Delete ALL Messages", type="primary"):
                        global_chat.clear()
                        st.success("All chat messages cleared!")
                        st.rerun()
            else:
                st.caption("No active messages to moderate.")

    chat_container = st.container()
    with chat_container:
        if not global_chat:
            st.info("No messages yet! Be the first to speak.")
        for msg in global_chat:
            is_user = msg["sender"].lower() == st.session_state["nickname"].lower()
            with st.chat_message("user" if is_user else "assistant"):
                sender_name = msg["sender"]
                msg_time = msg["time"]
                st.markdown(f"**{sender_name}** *({msg_time})*")
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
            st.success(f"You got it in {st.session_state['guesses']} tries! The secret number was {st.session_state['secret_num']}.")

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
            st.success("You win!")
        else:
            st.error("You lose! Try again.")

# --- PAGE 5: ANIMATED ASTEROID DODGE ---
elif page == "🚀 Asteroid Dodge":
    st.header("🚀 Asteroid Dodge (Arcade Edition)")
    st.write("Dodge the falling space debris in real-time!")

    asteroid_game_html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background-color: #0e1117; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 10px; }
    #gameCanvas { background-color: #161b22; border: 2px solid #30363d; border-radius: 8px; display: block; margin: 0 auto; }
    .info { margin-top: 8px; font-size: 14px; color: #8b949e; }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="600" height="400"></canvas>
  <div class="info">Click screen once, then use <b>Left / Right Arrow Keys</b> or <b>A / D</b> to move side to side. Press <b>R</b> to restart.</div>
  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    let score = 0, gameOver = false;
    const player = { x: canvas.width / 2 - 15, y: canvas.height - 40, width: 30, height: 30, speed: 6 };
    let asteroids = [], spawnRate = 35, frameCount = 0, keys = {};

    document.addEventListener("keydown", (e) => {
      if (["ArrowLeft", "ArrowRight"].includes(e.key)) e.preventDefault();
      keys[e.key] = true;
      if (gameOver && (e.key === "r" || e.key === "R")) resetGame();
    });
    document.addEventListener("keyup", (e) => { keys[e.key] = false; });

    function spawnAsteroid() {
      const size = Math.random() * 20 + 15;
      const x = Math.random() * (canvas.width - size);
      const speed = Math.random() * 2 + 2 + (score / 100);
      asteroids.push({ x, y: -size, size, speed });
    }

    function resetGame() {
      score = 0; asteroids = []; player.x = canvas.width / 2 - 15; player.y = canvas.height - 40; gameOver = false; loop();
    }

    function update() {
      if (gameOver) return;
      if (keys["ArrowLeft"] || keys["a"] || keys["A"]) player.x -= player.speed;
      if (keys["ArrowRight"] || keys["d"] || keys["D"]) player.x += player.speed;
      if (player.x < 0) player.x = 0;
      if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;

      frameCount++;
      if (frameCount % spawnRate === 0) spawnAsteroid();

      for (let i = 0; i < asteroids.length; i++) {
        let a = asteroids[i]; a.y += a.speed;
        if (player.x < a.x + a.size && player.x + player.width > a.x && player.y < a.y + a.size && player.y + player.height > a.y) gameOver = true;
        if (a.y > canvas.height) { asteroids.splice(i, 1); i--; score += 10; }
      }
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#ff4b4b";
      ctx.beginPath();
      ctx.moveTo(player.x + player.width / 2, player.y);
      ctx.lineTo(player.x, player.y + player.height);
      ctx.lineTo(player.x + player.width, player.y + player.height);
      ctx.closePath(); ctx.fill();

      ctx.fillStyle = "#8b949e";
      asteroids.forEach(a => {
        ctx.beginPath(); ctx.arc(a.x + a.size / 2, a.y + a.size / 2, a.size / 2, 0, Math.PI * 2); ctx.fill();
      });

      ctx.fillStyle = "#ffffff"; ctx.font = "16px sans-serif"; ctx.fillText("Score: " + score, 15, 25);

      if (gameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.75)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ff4b4b"; ctx.font = "bold 28px sans-serif"; ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 10);
        ctx.fillStyle = "#ffffff"; ctx.font = "16px sans-serif";
        ctx.fillText("Final Score: " + score, canvas.width / 2, canvas.height / 2 + 20);
        ctx.fillText("Press 'R' to Play Again", canvas.width / 2, canvas.height / 2 + 50);
        ctx.textAlign = "left";
      }
    }

    function loop() { update(); draw(); if (!gameOver) requestAnimationFrame(loop); }
    loop();
  </script>
</body>
</html>"""
    components.html(asteroid_game_html, height=520)

# --- PAGE 6: PAC-MAN ARCADE ---
elif page == "🟡 Pac-Man":
    st.header("🟡 Pac-Man Ultra-Smooth Arcade Edition")
    st.write("Chomp dots, grab Power Pellets, turn the tables on ghosts, and escape through the side tunnels!")

    pacman_html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background-color: #0e1117; color: white; font-family: 'Courier New', Courier, monospace; text-align: center; margin: 0; padding: 10px; }
    #pacmanCanvas { background-color: #000000; border: 4px solid #1919a6; border-radius: 8px; display: block; margin: 0 auto; box-shadow: 0 0 15px #1919a6; }
    .info { margin-top: 10px; font-size: 14px; color: #8b949e; font-family: sans-serif; }
  </style>
</head>
<body>

  <canvas id="pacmanCanvas" width="570" height="450"></canvas>
  <div class="info">Click screen, then use <b>Arrow Keys</b> or <b>WASD</b> to steer. Grab <b>Power Pellets</b> to eat ghosts! Press <b>R</b> to restart.</div>

  <script>
    const canvas = document.getElementById("pacmanCanvas");
    const ctx = canvas.getContext("2d");

    const tileSize = 30;
    const rows = 15;
    const cols = 19;

    const initialMap = [
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,3,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3,1],
      [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
      [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,1,1,0,1,0,1,1,4,1,1,0,1,0,1,1,0,1],
      [2,0,2,2,0,1,0,1,2,2,2,1,0,1,0,2,2,0,2],
      [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
      [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
      [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
      [1,0,0,1,0,0,0,0,0,2,0,0,0,0,0,1,0,0,1],
      [1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1],
      [1,3,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,3,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ];

    let map = [];
    let score = 0;
    let gameOver = false;
    let gameWon = false;
    let scaredTimer = 0;
    let mouthAngle = 0.2;
    let mouthOpening = true;

    let countdown = 3;
    let countdownActive = true;

    const speed = 2.5; 
    const ghostSpeed = 2.0;

    let pacman = { x: 9 * tileSize + 15, y: 10 * tileSize + 15, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, angle: 0 };
    let ghosts = [];

    function startCountdown() {
      countdown = 3;
      countdownActive = true;
      let interval = setInterval(() => {
        countdown--;
        if (countdown < 0) {
          countdownActive = false;
          clearInterval(interval);
        }
      }, 1000);
    }

    function initGame() {
      score = 0;
      gameOver = false;
      gameWon = false;
      scaredTimer = 0;
      map = JSON.parse(JSON.stringify(initialMap));
      pacman = { x: 9 * tileSize + 15, y: 10 * tileSize + 15, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, angle: 0 };
      
      ghosts = [
        { name: "Blinky", x: 9 * tileSize + 15, y: 5 * tileSize + 15, color: "#ff0000", dirX: 1, dirY: 0, type: "chase" },
        { name: "Pinky", x: 8 * tileSize + 15, y: 6 * tileSize + 15, color: "#ffb8ff", dirX: -1, dirY: 0, type: "ambush" },
        { name: "Inky", x: 9 * tileSize + 15, y: 6 * tileSize + 15, color: "#00ffff", dirX: 0, dirY: -1, type: "random" },
        { name: "Clyde", x: 10 * tileSize + 15, y: 6 * tileSize + 15, color: "#ffb852", dirX: 0, dirY: -1, type: "shy" }
      ];

      startCountdown();
    }

    document.addEventListener("keydown", (e) => {
      if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) e.preventDefault();

      if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
        pacman.nextDirX = -1; pacman
