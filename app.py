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
if "boss_hits" not in st.session_state:
    st.session_state["boss_hits"] = 0

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

# --- SECRET GOOFY BOSS GAME OVERLAY (NATIVE STREAMLIT) ---
if st.session_state["show_secret_game"]:
    st.info("🎉 **SECRET UNLOCKED!** Smash the Goofy Boss 25 times to unlock Tetris!")
    
    max_hits = 25
    hits = st.session_state["boss_hits"]
    hp_percent = max(0, 100 - int((hits / max_hits) * 100))
    
    st.progress(hp_percent / 100, text=f"Boss HP: {hp_percent}%")
    st.write(f"### Hits: {hits} / {max_hits}")
    
    st.markdown("""
    <style>
    div.stButton > button[key="boss_clicker"] {
        font-size: 80px !important;
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        background-color: #161b22 !important;
        border: 3px dashed #ff4b4b !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🤪", key="boss_clicker", use_container_width=True):
            st.session_state["boss_hits"] += 1
            if st.session_state["boss_hits"] >= max_hits:
                st.session_state["tetris_unlocked"] = True
                st.session_state["show_secret_game"] = False
                st.session_state["active_page"] = "🔴 Tetris"
                st.session_state["nav_radio"] = "🔴 Tetris"
                st.session_state["boss_hits"] = 0
                st.balloons()
                st.rerun()
            else:
                st.rerun()

    if st.button("Reset Boss Progress"):
        st.session_state["boss_hits"] = 0
        st.rerun()

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
        pacman.nextDirX = -1; pacman.nextDirY = 0;
      } else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
        pacman.nextDirX = 1; pacman.nextDirY = 0;
      } else if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
        pacman.nextDirX = 0; pacman.nextDirY = -1;
      } else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") {
        pacman.nextDirX = 0; pacman.nextDirY = 1;
      }

      if ((gameOver || gameWon) && (e.key === "r" || e.key === "R")) {
        initGame();
      }
    });

    function isWallPixel(px, py) {
      let gx = Math.floor(px / tileSize);
      let gy = Math.floor(py / tileSize);
      if (gy === 6 && (gx < 0 || gx >= cols)) return false;
      if (gx < 0 || gx >= cols || gy < 0 || gy >= rows) return true;
      return map[gy][gx] === 1 || map[gy][gx] === 4;
    }

    function canMovePixel(x, y, dx, dy, radius) {
      let nextX = x + dx * speed;
      let nextY = y + dy * speed;

      return !(
        isWallPixel(nextX - radius, nextY - radius) ||
        isWallPixel(nextX + radius, nextY - radius) ||
        isWallPixel(nextX - radius, nextY + radius) ||
        isWallPixel(nextX + radius, nextY + radius)
      );
    }

    function checkDotsRemaining() {
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          if (map[r][c] === 0 || map[r][c] === 3) return true;
        }
      }
      return false;
    }

    function update() {
      if (gameOver || gameWon || countdownActive) return;

      if (mouthOpening) {
        mouthAngle += 0.02;
        if (mouthAngle >= 0.25) mouthOpening = false;
      } else {
        mouthAngle -= 0.02;
        if (mouthAngle <= 0.01) mouthOpening = true;
      }

      if (scaredTimer > 0) scaredTimer -= 0.02;

      let radius = 12;
      let gridX = Math.floor(pacman.x / tileSize) * tileSize + 15;
      let gridY = Math.floor(pacman.y / tileSize) * tileSize + 15;

      if (pacman.nextDirX !== 0 || pacman.nextDirY !== 0) {
        if (canMovePixel(pacman.x, pacman.y, pacman.nextDirX, pacman.nextDirY, radius)) {
          if (pacman.nextDirX !== 0 && Math.abs(pacman.y - gridY) < 8) {
            pacman.y = gridY;
            pacman.dirX = pacman.nextDirX;
            pacman.dirY = 0;
          } else if (pacman.nextDirY !== 0 && Math.abs(pacman.x - gridX) < 8) {
            pacman.x = gridX;
            pacman.dirX = 0;
            pacman.dirY = pacman.nextDirY;
          }
        }
      }

      if (canMovePixel(pacman.x, pacman.y, pacman.dirX, pacman.dirY, radius)) {
        pacman.x += pacman.dirX * speed;
        pacman.y += pacman.dirY * speed;

        if (pacman.dirX === 1) pacman.angle = 0;
        else if (pacman.dirX === -1) pacman.angle = Math.PI;
        else if (pacman.dirY === -1) pacman.angle = 1.5 * Math.PI;
        else if (pacman.dirY === 1) pacman.angle = 0.5 * Math.PI;

        if (pacman.x < 0) pacman.x = cols * tileSize - 15;
        else if (pacman.x > cols * tileSize) pacman.x = 15;
      }

      let tileGX = Math.floor(pacman.x / tileSize);
      let tileGY = Math.floor(pacman.y / tileSize);

      if (map[tileGY] && map[tileGY][tileGX] === 0) {
        map[tileGY][tileGX] = 2;
        score += 10;
        if (!checkDotsRemaining()) gameWon = true;
      } else if (map[tileGY] && map[tileGY][tileGX] === 3) {
        map[tileGY][tileGX] = 2;
        score += 50;
        scaredTimer = 8;
        if (!checkDotsRemaining()) gameWon = true;
      }

      ghosts.forEach(g => {
        let gGX = Math.floor(g.x / tileSize);
        let gGY = Math.floor(g.y / tileSize);
        let gCenterX = gGX * tileSize + 15;
        let gCenterY = gGY * tileSize + 15;

        if (Math.abs(g.x - gCenterX) < 2 && Math.abs(g.y - gCenterY) < 2) {
          g.x = gCenterX;
          g.y = gCenterY;

          let possibleDirs = [
            { x: 1, y: 0 }, { x: -1, y: 0 }, { x: 0, y: 1 }, { x: 0, y: -1 }
          ].filter(d => {
            if (d.x === -g.dirX && d.y === -g.dirY) return false;
            let nx = gGX + d.x, ny = gGY + d.y;
            if (ny === 6 && (nx < 0 || nx >= cols)) return true;
            return nx >= 0 && nx < cols && ny >= 0 && ny < rows && map[ny][nx] !== 1;
          });

          if (possibleDirs.length === 0) {
            possibleDirs = [{ x: -g.dirX, y: -g.dirY }];
          }

          let targetX = pacman.x, targetY = pacman.y;
          if (scaredTimer > 0) {
            targetX = cols * tileSize - pacman.x;
            targetY = rows * tileSize - pacman.y;
          } else if (g.type === "ambush") {
            targetX = pacman.x + pacman.dirX * 60;
            targetY = pacman.y + pacman.dirY * 60;
          } else if (g.type === "random") {
            targetX = Math.random() * canvas.width;
            targetY = Math.random() * canvas.height;
          }

          possibleDirs.sort((a, b) => {
            let distA = Math.hypot((g.x + a.x * tileSize) - targetX, (g.y + a.y * tileSize) - targetY);
            let distB = Math.hypot((g.x + b.x * tileSize) - targetX, (g.y + b.y * tileSize) - targetY);
            return distA - distB;
          });

          g.dirX = possibleDirs[0].x;
          g.dirY = possibleDirs[0].y;
        }

        let currentGhostSpeed = scaredTimer > 0 ? ghostSpeed * 0.6 : ghostSpeed;
        g.x += g.dirX * currentGhostSpeed;
        g.y += g.dirY * currentGhostSpeed;

        if (g.x < 0) g.x = cols * tileSize - 15;
        else if (g.x > cols * tileSize) g.x = 15;

        let distToPacman = Math.hypot(g.x - pacman.x, g.y - pacman.y);
        if (distToPacman < 18) {
          if (scaredTimer > 0) {
            score += 200;
            g.x = 9 * tileSize + 15;
            g.y = 6 * tileSize + 15;
          } else {
            gameOver = true;
          }
        }
      });
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          let cell = map[r][c];
          let px = c * tileSize, py = r * tileSize;

          if (cell === 1) {
            ctx.fillStyle = "#1919a6";
            ctx.fillRect(px + 2, py + 2, tileSize - 4, tileSize - 4);
          } else if (cell === 4) {
            ctx.fillStyle = "#ffb8ff";
            ctx.fillRect(px, py + tileSize/2 - 2, tileSize, 4);
          } else if (cell === 0) {
            ctx.fillStyle = "#ffb8ae";
            ctx.beginPath();
            ctx.arc(px + tileSize/2, py + tileSize/2, 3, 0, Math.PI * 2);
            ctx.fill();
          } else if (cell === 3) {
            ctx.fillStyle = (Math.floor(Date.now() / 250) % 2 === 0) ? "#ffffff" : "#ffb8ae";
            ctx.beginPath();
            ctx.arc(px + tileSize/2, py + tileSize/2, 7, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      ctx.fillStyle = "#ffff00";
      ctx.beginPath();
      ctx.arc(pacman.x, pacman.y, tileSize / 2 - 2, pacman.angle + mouthAngle * Math.PI, pacman.angle + (2 - mouthAngle) * Math.PI);
      ctx.lineTo(pacman.x, pacman.y);
      ctx.fill();

      ghosts.forEach(g => {
        if (scaredTimer > 0) {
          ctx.fillStyle = (scaredTimer < 2 && Math.floor(Date.now() / 150) % 2 === 0) ? "#ffffff" : "#2121ff";
        } else {
          ctx.fillStyle = g.color;
        }

        ctx.beginPath();
        ctx.arc(g.x, g.y - 2, tileSize / 2 - 2, Math.PI, 0, false);
        ctx.lineTo(g.x + tileSize / 2 - 2, g.y + tileSize / 2 - 2);
        ctx.lineTo(g.x, g.y + tileSize / 2 - 6);
        ctx.lineTo(g.x - tileSize / 2 + 2, g.y + tileSize / 2 - 2);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(g.x - 4, g.y - 3, 3, 0, Math.PI * 2);
        ctx.arc(g.x + 4, g.y - 3, 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = scaredTimer > 0 ? "#ffb8ae" : "#000000";
        ctx.beginPath();
        ctx.arc(g.x - 4 + g.dirX * 1.5, g.y - 3 + g.dirY * 1.5, 1.5, 0, Math.PI * 2);
        ctx.arc(g.x + 4 + g.dirX * 1.5, g.y - 3 + g.dirY * 1.5, 1.5, 0, Math.PI * 2);
        ctx.fill();
      });

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 16px 'Courier New', Courier, monospace";
      ctx.fillText("1UP SCORE", 20, 435);
      ctx.fillStyle = "#ffff00";
      ctx.fillText(score, 120, 435);

      if (scaredTimer > 0) {
        ctx.fillStyle = "#00ffff";
        ctx.fillText("POWER MODE!", 380, 435);
      }

      if (countdownActive) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.textAlign = "center";
        ctx.fillStyle = "#ffff00";
        ctx.font = "bold 55px 'Courier New', Courier, monospace";
        if (countdown > 0) {
          ctx.fillText(countdown, canvas.width / 2, canvas.height / 2 + 15);
        } else {
          ctx.fillStyle = "#00ff00";
          ctx.fillText("READY!", canvas.width / 2, canvas.height / 2 + 15);
        }
        ctx.textAlign = "left";
      }

      if (gameOver || gameWon) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.textAlign = "center";
        if (gameOver) {
          ctx.fillStyle = "#ff0000";
          ctx.font = "bold 34px 'Courier New', Courier, monospace";
          ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 10);
        } else {
          ctx.fillStyle = "#00ff00";
          ctx.font = "bold 34px 'Courier New', Courier, monospace";
          ctx.fillText("VICTORY!", canvas.width / 2, canvas.height / 2 - 10);
        }

        ctx.fillStyle = "#ffffff";
        ctx.font = "16px sans-serif";
        ctx.fillText("Final Score: " + score, canvas.width / 2, canvas.height / 2 + 30);
        ctx.fillText("Press 'R' to Play Again", canvas.width / 2, canvas.height / 2 + 65);
        ctx.textAlign = "left";
      }
    }

    function gameLoop() {
      update();
      draw();
      requestAnimationFrame(gameLoop);
    }

    initGame();
    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>"""
    components.html(pacman_html, height=520)

# --- PAGE 7: UNLOCKED TETRIS GAME ---
elif page in ["🧱 Tetris", "🔴 Tetris"]:
    st.header("🔴 Classic Arcade Tetris")
    st.write("Control falling blocks, complete horizontal lines, and set high scores!")

    tetris_html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background-color: #0e1117; color: white; font-family: 'Courier New', Courier, monospace; text-align: center; margin: 0; padding: 10px; }
    .game-container { display: flex; justify-content: center; align-items: flex-start; gap: 20px; margin-top: 10px; }
    #tetrisCanvas { background-color: #000; border: 3px solid #ff4b4b; border-radius: 6px; box-shadow: 0 0 12px rgba(255, 75, 75, 0.4); }
    .sidebar-panel { background: #161b22; border: 2px solid #30363d; border-radius: 8px; padding: 15px; width: 140px; text-align: left; }
    .panel-title { font-size: 14px; color: #8b949e; text-transform: uppercase; margin-bottom: 5px; }
    .panel-value { font-size: 22px; font-weight: bold; color: #00ff00; margin-bottom: 15px; }
    #nextCanvas { background: #000; border: 1px solid #30363d; border-radius: 4px; }
    .controls-info { margin-top: 15px; font-size: 13px; color: #8b949e; font-family: sans-serif; }
  </style>
</head>
<body>

  <div class="game-container">
    <canvas id="tetrisCanvas" width="240" height="400"></canvas>
    
    <div class="sidebar-panel">
      <div class="panel-title">SCORE</div>
      <div id="scoreVal" class="panel-value">0</div>

      <div class="panel-title">LINES</div>
      <div id="linesVal" class="panel-value">0</div>

      <div class="panel-title">LEVEL</div>
      <div id="levelVal" class="panel-value">1</div>

      <div class="panel-title">NEXT</div>
      <canvas id="nextCanvas" width="80" height="80"></canvas>
    </div>
  </div>

  <div class="controls-info">
    Click game area! <b>Left/Right Arrow</b>: Move | <b>Up Arrow</b>: Rotate | <b>Down Arrow</b>: Soft Drop | <b>Spacebar</b>: Hard Drop | <b>R</b>: Restart
  </div>

  <script>
    const canvas = document.getElementById("tetrisCanvas");
    const ctx = canvas.getContext("2d");
    const nextCanvas = document.getElementById("nextCanvas");
    const nextCtx = nextCanvas.getContext("2d");

    const ROWS = 20;
    const COLS = 12;
    const BLOCK_SIZE = 20;

    ctx.scale(BLOCK_SIZE, BLOCK_SIZE);
    nextCtx.scale(20, 20);

    let board = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
    let score = 0, lines = 0, level = 1;
    let gameOver = false;
    let dropCounter = 0, dropInterval = 1000, lastTime = 0;

    const COLORS = [
      null, "#00ffff", "#0000ff", "#ff7f00", "#ffff00", "#00ff00", "#800080", "#ff0000"
    ];

    const SHAPES = [
      [],
      [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
      [[2,0,0],[2,2,2],[0,0,0]],
      [[0,0,3],[3,3,3],[0,0,0]],
      [[4,4],[4,4]],
      [[0,5,5],[5,5,0],[0,0,0]],
      [[0,6,0],[6,6,6],[0,0,0]],
      [[7,7,0],[0,7,7],[0,0,0]]
    ];

    let player = { pos: { x: 0, y: 0 }, matrix: null };
    let nextPieceId = Math.floor(Math.random() * 7) + 1;

    function collide(arena, player) {
      const [m, o] = [player.matrix, player.pos];
      for (let r = 0; r < m.length; ++r) {
        for (let c = 0; c < m[r].length; ++c) {
          if (m[r][c] !== 0 && (arena[r + o.y] && arena[r + o.y][c + o.x]) !== 0) {
            return true;
          }
        }
      }
      return false;
    }

    function merge(arena, player) {
      player.matrix.forEach((row, r) => {
        row.forEach((value, c) => {
          if (value !== 0) {
            arena[r + player.pos.y][c + player.pos.x] = value;
          }
        });
      });
    }

    function arenaSweep() {
      let rowCount = 0;
      outer: for (let r = arena.length - 1; r > 0; --r) {
        for (let c = 0; c < arena[r].length; ++c) {
          if (arena[r][c] === 0) continue outer;
        }
        const row = arena.splice(r, 1)[0].fill(0);
        arena.unshift(row);
        ++r;
        rowCount++;
      }
      if (rowCount > 0) {
        lines += rowCount;
        score += rowCount * 100 * level;
        level = Math.floor(lines / 5) + 1;
        dropInterval = Math.max(100, 1000 - (level - 1) * 100);
        updateScoreBoard();
      }
    }

    function playerDrop() {
      player.pos.y++;
      if (collide(board, player)) {
        player.pos.y--;
        merge(board, player);
        playerReset();
        arenaSweep();
      }
      dropCounter = 0;
    }

    function playerMove(dir) {
      player.pos.x += dir;
      if (collide(board, player)) {
        player.pos.x -= dir;
      }
    }

    function playerReset() {
      const pieceId = nextPieceId;
      nextPieceId = Math.floor(Math.random() * 7) + 1;
      player.matrix = SHAPES[pieceId];
      player.pos.y = 0;
      player.pos.x = Math.floor((COLS - player.matrix[0].length) / 2);
      if (collide(board, player)) {
        gameOver = true;
      }
    }

    function playerRotate(dir) {
      const pos = player.pos.x;
      let offset = 1;
      rotate(player.matrix, dir);
      while (collide(board, player)) {
        player.pos.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > player.matrix[0].length) {
          rotate(player.matrix, -dir);
          player.pos.x = pos;
          return;
        }
      }
    }

    function rotate(matrix, dir) {
      for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
          [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
        }
      }
      if (dir > 0) {
        matrix.forEach(row => row.reverse());
      } else {
        matrix.reverse();
      }
    }

    function updateScoreBoard() {
      document.getElementById("scoreVal").innerText = score;
      document.getElementById("linesVal").innerText = lines;
      document.getElementById("levelVal").innerText = level;
      
      nextCtx.fillStyle = '#000';
      nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
      const nextM = SHAPES[nextPieceId];
      nextM.forEach((row, y) => {
        row.forEach((value, x) => {
          if (value !== 0) {
            nextCtx.fillStyle = COLORS[value];
            nextCtx.fillRect(x + 1, y + 1, 1, 1);
          }
        });
      });
    }

    function drawMatrix(matrix, offset, context = ctx) {
      matrix.forEach((row, y) => {
        row.forEach((value, x) => {
          if (value !== 0) {
            context.fillStyle = COLORS[value];
            context.fillRect(x + offset.x, y + offset.y, 1, 1);
          }
        });
      });
    }

    function draw() {
      ctx.fillStyle = '#000';
      ctx.fillRect(0, 0, COLS, ROWS);

      drawMatrix(board, { x: 0, y: 0 });
      drawMatrix(player.matrix, player.pos);

      if (gameOver) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(0, 0, COLS, ROWS);
        ctx.fillStyle = '#ff4b4b';
        ctx.font = '1px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText("GAME OVER", COLS / 2, ROWS / 2 - 1);
        ctx.fillStyle = '#ffffff';
        ctx.font = '0.6px sans-serif';
        ctx.fillText("Press 'R' to Restart", COLS / 2, ROWS / 2 + 1);
        ctx.textAlign = 'left';
      }
    }

    function update(time = 0) {
      if (gameOver) return;
      const deltaTime = time - lastTime;
      lastTime = time;
      dropCounter += deltaTime;
      if (dropCounter > dropInterval) {
        playerDrop();
      }
      draw();
      requestAnimationFrame(update);
    }

    document.addEventListener("keydown", event => {
      if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].includes(event.key)) {
        event.preventDefault();
      }
      if (gameOver) {
        if (event.key === 'r' || event.key === 'R') {
          board = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
          score = 0; lines = 0; level = 1; dropInterval = 1000;
          gameOver = false;
          playerReset();
          updateScoreBoard();
          update();
        }
        return;
      }
      if (event.key === 'ArrowLeft') playerMove(-1);
      else if (event.key === 'ArrowRight') playerMove(1);
      else if (event.key === 'ArrowDown') playerDrop();
      else if (event.key === 'ArrowUp') playerRotate(1);
      else if (event.key === ' ') {
        while (!collide(board, player)) {
          player.pos.y++;
        }
        player.pos.y--;
        merge(board, player);
        playerReset();
        arenaSweep();
        dropCounter = 0;
      }
    });

    playerReset();
    updateScoreBoard();
    update();
  </script>
</body>
</html>
"""
    components.html(tetris_html, height=550)
