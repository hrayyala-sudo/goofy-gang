import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="wide")

# Allowed Users (Stored in lowercase for easy matching) & Password
ALLOWED_USERS = ["pranav", "calvin", "austin", "goofy member"]
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

# --- 3. CENTERED COMPACT LOGIN SYSTEM ---
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
                # Preserve user's typed name format for display
                st.session_state["nickname"] = user_input.strip()
                st.success(f"Welcome, {user_input.strip()}!")
                st.rerun()
            elif clean_username not in ALLOWED_USERS:
                st.error("Name not recognized! Please enter an authorized name.")
            else:
                st.error("Incorrect password!")

if not st.session_state["logged_in"]:
    show_login_screen()
    st.stop()

# --- 4. COMPACT SIDEBAR NAVIGATION ---
st.sidebar.caption(f"Logged in as **{st.session_state['nickname']}**")

st.sidebar.markdown("**Profile Settings**")
new_nick = st.sidebar.text_input("Change Nickname:", value=st.session_state["nickname"], label_visibility="collapsed")
if st.sidebar.button("Save Nickname"):
    st.session_state["nickname"] = new_nick
    st.rerun()

st.sidebar.divider()
st.sidebar.markdown("**Pages**")
page = st.sidebar.radio(
    "Navigation",
    ["💬 Goofy Chatbox", "🎲 Guessing Game", "❌ Tic-Tac-Toe", "🪨 Rock Paper Scissors", "🚀 Asteroid Dodge", "🟡 Pac-Man"],
    label_visibility="collapsed"
)

st.sidebar.divider()
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["nickname"] = ""
    st.rerun()

# --- 5. MAIN DASHBOARD ---
st.title("🤪 Goofy Gang Dashboard")
st.markdown("---")

# --- PAGE 1: GOOFY CHATBOX ---
if page == "💬 Goofy Chatbox":
    st.header("💬 Goofy Chatbox")
    st.write("Welcome to the main chat room! Messages update for everyone.")

    if st.button("🔄 Refresh Messages"):
        st.rerun()

    # --- CALVIN MODERATION CONTROLS (Case-Insensitive Check) ---
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
            with st.chat_message("user" if msg["sender"].lower() == st.session_state["nickname"].lower() else "assistant"):
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

    asteroid_game_html = """
    <!DOCTYPE html>
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
    </html>
    """
    components.html(asteroid_game_html, height=520)

# --- PAGE 6: AUTHENTIC PAC-MAN ARCADE ---
elif page == "🟡 Pac-Man":
    st.header("🟡 Pac-Man Authentic Arcade Edition")
    st.write("Chomp dots, grab Power Pellets, turn the tables on ghosts, and escape through the side tunnels!")

    pacman_html = """
    <!DOCTYPE html>
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

        // Map Legend: 1=Wall, 0=Dot, 3=Power Pellet, 2=Path/Empty, 4=Ghost Gate
        const initialMap = [
          [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
          [1,3,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3,1],
          [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
          [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
          [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,1,1,0,1,0,1,1,4,1,1,0,1,0,1,1,0,1],
          [2,0,2,2,0,1,0,1,2,2,2,1,0,1,0,2,2,0,2], // Side Tunnel Row
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

        // Countdown variables
        let countdown = 3;
        let countdownActive = true;

        let pacman = { x: 9, y: 10, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, angle: 0 };
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
          pacman = { x: 9, y: 10, dirX: 0, dirY: 0, nextDirX: 0, nextDirY: 0, angle: 0 };
          
          ghosts = [
            { name: "Blinky", x: 9, y: 5, color: "#ff0000", dirX: 1, dirY: 0, type: "chase" },
            { name: "Pinky", x: 8, y: 6, color: "#ffb8ff", dirX: -1, dirY: 0, type: "ambush" },
            { name: "Inky", x: 9, y: 6, color: "#00ffff", dirX: 0, dirY: -1, type: "random" },
            { name: "Clyde", x: 10, y: 6, color: "#ffb852", dirX: 0, dirY: -1, type: "shy" }
          ];

          startCountdown();
        }

        document.addEventListener("keydown", (e) => {
          if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) e.preventDefault();

          if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
            pacman.nextDirX = -1; pacman.nextDirY = 0; pacman.angle = Math.PI;
          } else if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
            pacman.nextDirX = 1; pacman.nextDirY = 0; pacman.angle = 0;
          } else if (e.key === "ArrowUp" || e.key === "w" || e.key === "W") {
            pacman.nextDirX = 0; pacman.nextDirY = -1; pacman.angle = 1.5 * Math.PI;
          } else if (e.key === "ArrowDown" || e.key === "s" || e.key === "S") {
            pacman.nextDirX = 0; pacman.nextDirY = 1; pacman.angle = 0.5 * Math.PI;
          }

          if ((gameOver || gameWon) && (e.key === "r" || e.key === "R")) {
            initGame();
          }
        });

        function isWall(gx, gy) {
          if (gy === 6 && (gx < 0 || gx >= cols)) return false; // Tunnel
          if (gx < 0 || gx >= cols || gy < 0 || gy >= rows) return true;
          return map[gy][gx] === 1 || map[gy][gx] === 4;
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

          // Mouth Animation
          if (mouthOpening) {
            mouthAngle += 0.04;
            if (mouthAngle >= 0.25) mouthOpening = false;
          } else {
            mouthAngle -= 0.04;
            if (mouthAngle <= 0.02) mouthOpening = true;
          }

          if (scaredTimer > 0) scaredTimer--;

          // Turn Pac-Man
          if (!isWall(pacman.x + pacman.nextDirX, pacman.y + pacman.nextDirY)) {
            pacman.dirX = pacman.nextDirX;
            pacman.dirY = pacman.nextDirY;
          }

          // Move Pac-Man
          if (!isWall(pacman.x + pacman.dirX, pacman.y + pacman.dirY)) {
            pacman.x += pacman.dirX;
            pacman.y += pacman.dirY;

            if (pacman.x < 0) pacman.x = cols - 1;
            else if (pacman.x >= cols) pacman.x = 0;
          }

          // Eat Dot
          if (map[pacman.y] && map[pacman.y][pacman.x] === 0) {
            map[pacman.y][pacman.x] = 2;
            score += 10;
            if (!checkDotsRemaining()) gameWon = true;
          } 
          // Eat Power Pellet
          else if (map[pacman.y] && map[pacman.y][pacman.x] === 3) {
            map[pacman.y][pacman.x] = 2;
            score += 50;
            scaredTimer = 40;
            if (!checkDotsRemaining()) gameWon = true;
          }

          // Ghosts AI
          ghosts.forEach(g => {
            let possibleDirs = [
              { x: 1, y: 0 }, { x: -1, y: 0 }, { x: 0, y: 1 }, { x: 0, y: -1 }
            ].filter(d => {
              let nx = g.x + d.x, ny = g.y + d.y;
              if (ny === 6 && (nx < 0 || nx >= cols)) return true;
              return nx >= 0 && nx < cols && ny >= 0 && ny < rows && map[ny][nx] !== 1;
            });

            if (possibleDirs.length > 0) {
              let targetX = pacman.x, targetY = pacman.y;

              if (scaredTimer > 0) {
                targetX = cols - pacman.x;
                targetY = rows - pacman.y;
              } else if (g.type === "ambush") {
                targetX = pacman.x + pacman.dirX * 3;
                targetY = pacman.y + pacman.dirY * 3;
              } else if (g.type === "random") {
                targetX = Math.floor(Math.random() * cols);
                targetY = Math.floor(Math.random() * rows);
              }

              possibleDirs.sort((a, b) => {
                let distA = Math.hypot((g.x + a.x) - targetX, (g.y + a.y) - targetY);
                let distB = Math.hypot((g.x + b.x) - targetX, (g.y + b.y) - targetY);
                return distA - distB;
              });

              let chosen = possibleDirs[0];
              g.dirX = chosen.x; g.dirY = chosen.y;
              g.x += g.dirX; g.y += g.dirY;

              if (g.x < 0) g.x = cols - 1;
              else if (g.x >= cols) g.x = 0;
            }

            if (g.x === pacman.x && g.y === pacman.y) {
              if (scaredTimer > 0) {
                score += 200;
                g.x = 9; g.y = 6;
              } else {
                gameOver = true;
              }
            }
          });
        }

        function draw() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Draw Map
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

          // Draw Pac-Man
          let pxX = pacman.x * tileSize + tileSize / 2;
          let pxY = pacman.y * tileSize + tileSize / 2;
          ctx.fillStyle = "#ffff00";
          ctx.beginPath();
          ctx.arc(pxX, pxY, tileSize / 2 - 2, pacman.angle + mouthAngle * Math.PI, pacman.angle + (2 - mouthAngle) * Math.PI);
          ctx.lineTo(pxX, pxY);
          ctx.fill();

          // Draw Ghosts
          ghosts.forEach(g => {
            let gx = g.x * tileSize + tileSize / 2;
            let gy = g.y * tileSize + tileSize / 2;

            if (scaredTimer > 0) {
              ctx.fillStyle = (scaredTimer < 10 && scaredTimer % 2 === 0) ? "#ffffff" : "#2121ff";
            } else {
              ctx.fillStyle = g.color;
            }

            ctx.beginPath();
            ctx.arc(gx, gy - 2, tileSize / 2 - 2, Math.PI, 0, false);
            ctx.lineTo(gx + tileSize / 2 - 2, gy + tileSize / 2 - 2);
            ctx.lineTo(gx, gy + tileSize / 2 - 6);
            ctx.lineTo(gx - tileSize / 2 + 2, gy + tileSize / 2 - 2);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(gx - 4, gy - 3, 3, 0, Math.PI * 2);
            ctx.arc(gx + 4, gy - 3, 3, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = scaredTimer > 0 ? "#ffb8ae" : "#000000";
            ctx.beginPath();
            ctx.arc(gx - 4 + g.dirX, gy - 3 + g.dirY, 1.5, 0, Math.PI * 2);
            ctx.arc(gx + 4 + g.dirX, gy - 3 + g.dirY, 1.5, 0, Math.PI * 2);
            ctx.fill();
          });

          // Draw Score Overlay
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 16px 'Courier New', Courier, monospace";
          ctx.fillText("1UP SCORE", 20, 435);
          ctx.fillStyle = "#ffff00";
          ctx.fillText(score, 120, 435);

          if (scaredTimer > 0) {
            ctx.fillStyle = "#00ffff";
            ctx.fillText("POWER MODE!", 380, 435);
          }

          // Countdown Overlay
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

          // Game Over / Win Screens
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

        function loop() {
          update();
          draw();
        }

        initGame();
        setInterval(loop, 130);
      </script>
    </body>
    </html>
    """
    components.html(pacman_html, height=520)
