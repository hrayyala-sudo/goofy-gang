import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="wide")

# Inject Custom CSS specifically targeting our secret button key "secret_tetris_btn"
st.html("""
<style>
div[class*="st-key-secret_tetris_btn"] button {
    background-color: #ff4b4b !important;
    color: white !important;
    border-radius: 50% !important;
    font-size: 1.5rem !important;
    width: 50px !important;
    height: 50px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 0 10px rgba(255, 75, 75, 0.6) !important;
    transition: all 0.3s ease-in-out !important;
}
div[class*="st-key-secret_tetris_btn"] button:hover {
    transform: scale(1.15) rotate(15deg) !important;
    box-shadow: 0 0 18px rgba(255, 75, 75, 0.9) !important;
    background-color: #ff3333 !important;
}
</style>""")

# Allowed Users
ALLOWED_USERS = ["pranav", "calvin", "cal", "austin", "isaac", "george", "isaiah", "fox"]

# Initialize Base Session State
if "portal_password" not in st.session_state:
    st.session_state["portal_password"] = "goofy123"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "nickname" not in st.session_state:
    st.session_state["nickname"] = ""
if "show_secret_game" not in st.session_state:
    st.session_state["show_secret_game"] = False
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "💬 Goofy Chatbox"
if "feature_requests" not in st.session_state:
    st.session_state["feature_requests"] = []
if "banned_users" not in st.session_state:
    st.session_state["banned_users"] = []
if "polls" not in st.session_state:
    st.session_state["polls"] = []

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
            if clean_username in st.session_state["banned_users"]:
                st.error("🚫 You have been banned from the portal by an admin!")
            elif clean_username in ALLOWED_USERS and pass_input == st.session_state["portal_password"]:
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

pages_list = [
    "💬 Goofy Chatbox", 
    "🎲 Guessing Game", 
    "❌ Tic-Tac-Toe", 
    "🪨 Rock Paper Scissors", 
    "🚀 Asteroid Dodge", 
    "🟡 Pac-Man", 
    "💡 Feature Requests",
    "🎨 Goofy Sketchpad",
    "📊 Gang Polls",
    "📅 Gang Calendar"
]

if st.session_state["nickname"].strip().lower() in ["calvin", "cal"]:
    pages_list.append("👑 Admin Controls")

if st.session_state["active_page"] not in pages_list:
    st.session_state["active_page"] = pages_list[0]

st.sidebar.divider()
st.sidebar.markdown("**Pages**")

selected_page = st.sidebar.radio(
    "Navigation",
    pages_list,
    index=pages_list.index(st.session_state["active_page"]),
    label_visibility="collapsed"
)

if selected_page != st.session_state["active_page"]:
    st.session_state["active_page"] = selected_page
    st.rerun()

st.sidebar.divider()
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["nickname"] = ""
    st.rerun()

# --- 5. MAIN HEADER WITH DECORATED TETRIS TOGGLE ---
col_btn, col_title = st.columns([0.06, 0.94])
with col_btn:
    if st.button("🤪", help="Click to open/close Secret Tetris!", key="secret_tetris_btn"):
        st.session_state["show_secret_game"] = not st.session_state["show_secret_game"]
        st.rerun()
with col_title:
    st.markdown("<h1 style='margin: 0; padding-top: 5px; font-size: 2.25rem; font-weight: 700;'>Goofy Gang Dashboard</h1>", unsafe_allow_html=True)

st.markdown("---")

if "calendar_events" not in st.session_state:
    st.session_state["calendar_events"] = []

# --- SECRET TETRIS OVERLAY ---
if st.session_state["show_secret_game"]:
    st.info("🎮 **SECRET TETRIS UNLOCKED!** Click inside the game box once to enable controls.")
    
    tetris_html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background-color: #0e1117; color: white; font-family: 'Courier New', Courier, monospace; text-align: center; margin: 0; padding: 10px; overflow: hidden; outline: none; }
    .game-container { display: flex; justify-content: center; align-items: flex-start; gap: 20px; margin-top: 10px; }
    #tetrisCanvas { background-color: #000; border: 3px solid #ff4b4b; border-radius: 6px; box-shadow: 0 0 12px rgba(255, 75, 75, 0.4); width: 220px; height: 380px; display: block; cursor: pointer; }
    .sidebar-panel { background: #161b22; border: 2px solid #30363d; border-radius: 8px; padding: 12px; width: 130px; text-align: left; box-sizing: border-box; }
    .panel-title { font-size: 11px; color: #8b949e; text-transform: uppercase; margin-bottom: 3px; }
    .panel-value { font-size: 18px; font-weight: bold; color: #00ff00; margin-bottom: 12px; }
    #nextCanvas { background: #000; border: 1px solid #30363d; border-radius: 4px; display: block; width: 70px; height: 70px; }
    .controls-info { margin-top: 12px; font-size: 12px; color: #8b949e; font-family: sans-serif; }
  </style>
</head>
<body tabindex="0" id="bodyRoot">

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
    👉 <b>Click game to focus!</b> | <b>Left/Right</b>: Move | <b>Up</b>: Rotate | <b>Down</b>: Drop | <b>Space</b>: Hard Drop | <b>R</b>: Reset
  </div>

  <script>
    const root = document.getElementById("bodyRoot");
    root.focus();
    root.addEventListener("click", () => root.focus());

    const canvas = document.getElementById("tetrisCanvas");
    const ctx = canvas.getContext("2d");
    const nextCanvas = document.getElementById("nextCanvas");
    const nextCtx = nextCanvas.getContext("2d");

    const ROWS = 20;
    const COLS = 12;
    ctx.scale(20, 20);
    nextCtx.scale(20, 20);

    let board = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
    let score = 0, lines = 0, level = 1;
    let gameOver = false;
    let dropCounter = 0, dropInterval = 1000, lastTime = 0;

    const COLORS = [null, "#00ffff", "#0000ff", "#ff7f00", "#ffff00", "#00ff00", "#800080", "#ff0000"];
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
          if (value !== 0) arena[r + player.pos.y][c + player.pos.x] = value;
        });
      });
    }

    function arenaSweep() {
      let rowCount = 0;
      outer: for (let r = board.length - 1; r >= 0; --r) {
        for (let c = 0; c < board[r].length; ++c) {
          if (board[r][c] === 0) continue outer;
        }
        const row = board.splice(r, 1)[0].fill(0);
        board.unshift(row);
        ++r;
        rowCount++;
      }
      if (rowCount > 0) {
        lines += rowCount;
        score += rowCount * 100 * level;
        level = Math.floor(lines / 10) + 1;
        dropInterval = Math.max(100, 1000 - (level - 1) * 100);
        updateScore();
      }
    }

    function rotate(matrix, dir) {
      for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
          [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
        }
      }
      if (dir > 0) matrix.forEach(row => row.reverse());
      else matrix.reverse();
    }

    function playerDrop() {
      player.pos.y++;
      if (collide(board, player)) {
        player.pos.y--;
        merge(board, player);
        arenaSweep();
        playerReset();
      }
      dropCounter = 0;
    }

    function playerMove(dir) {
      player.pos.x += dir;
      if (collide(board, player)) player.pos.x -= dir;
    }

    function playerReset() {
      player.matrix = SHAPES[nextPieceId];
      nextPieceId = Math.floor(Math.random() * 7) + 1;
      player.pos.y = 0;
      player.pos.x = Math.floor(board[0].length / 2) - Math.floor(player.matrix[0].length / 2);
      if (collide(board, player)) {
        gameOver = true;
      }
      drawNext();
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

    function drawMatrix(matrix, offset, context) {
      matrix.forEach((row, r) => {
        row.forEach((value, c) => {
          if (value !== 0) {
            context.fillStyle = COLORS[value];
            context.fillRect(c + offset.x, r + offset.y, 1, 1);
          }
        });
      });
    }

    function draw() {
      ctx.fillStyle = "#000";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      drawMatrix(board, { x: 0, y: 0 }, ctx);
      drawMatrix(player.matrix, player.pos, ctx);
      if (gameOver) {
        ctx.fillStyle = "rgba(0,0,0,0.75)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ff4b4b";
        ctx.font = "1.5px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", COLS / 2, ROWS / 2);
      }
    }

    function drawNext() {
      nextCtx.fillStyle = "#000";
      nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
      const m = SHAPES[nextPieceId];
      const ox = (4 - m[0].length) / 2;
      const oy = (4 - m.length) / 2;
      drawMatrix(m, { x: ox, y: oy }, nextCtx);
    }

    function updateScore() {
      document.getElementById("scoreVal").innerText = score;
      document.getElementById("linesVal").innerText = lines;
      document.getElementById("levelVal").innerText = level;
    }

    function update(time = 0) {
      if (gameOver) { draw(); return; }
      const deltaTime = time - lastTime;
      lastTime = time;
      dropCounter += deltaTime;
      if (dropCounter > dropInterval) playerDrop();
      draw();
      requestAnimationFrame(update);
    }

    function resetGame() {
      board = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
      score = 0; lines = 0; level = 1; dropInterval = 1000; gameOver = false;
      updateScore();
      playerReset();
      update();
    }

    window.addEventListener("keydown", event => {
      if (["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(event.key)) {
        event.preventDefault();
      }
      if (gameOver && event.key.toLowerCase() === 'r') { resetGame(); return; }
      if (gameOver) return;
      if (event.key === "ArrowLeft") playerMove(-1);
      else if (event.key === "ArrowRight") playerMove(1);
      else if (event.key === "ArrowDown") playerDrop();
      else if (event.key === "ArrowUp") playerRotate(1);
      else if (event.key === " ") {
        while (!collide(board, player)) { player.pos.y++; }
        player.pos.y--;
        merge(board, player);
        arenaSweep();
        playerReset();
      } else if (event.key.toLowerCase() === 'r') {
        resetGame();
      }
    });

    resetGame();
  </script>
</body>
</html>
"""
    components.html(tetris_html, height=460)

# --- 6. PAGE ROUTER ---
active_page = st.session_state["active_page"]

if active_page == "💬 Goofy Chatbox":
    st.subheader("💬 Global Goofy Chatbox")
    st.caption("Chat live with everyone currently logged into the portal!")

    chat_container = st.container(height=400)
    with chat_container:
        if not global_chat:
            st.info("No messages yet. Say something goofy to start the conversation!")
        for msg in global_chat:
            st.markdown(f"**{msg['sender']}** `{msg['time']}`: {msg['text']}")

    with st.form(key="chat_form", clear_on_submit=True):
        user_message = st.text_input("Type a message...", placeholder="Type here...")
        submit_chat = st.form_submit_button("Send")
        if submit_chat and user_message.strip():
            timestamp = datetime.now().strftime("%H:%M:%S")
            global_chat.append({
                "sender": st.session_state["nickname"],
                "text": user_message.strip(),
                "time": timestamp
            })
            st.rerun()

elif active_page == "🎲 Guessing Game":
    st.subheader("🎲 Number Guessing Game")
    st.write("Guess a number between 1 and 50!")
    if "secret_number" not in st.session_state:
        st.session_state["secret_number"] = random.randint(1, 50)
    
    guess = st.number_input("Enter your guess:", min_value=1, max_value=50, step=1)
    if st.button("Submit Guess"):
        if guess == st.session_state["secret_number"]:
            st.success("🎉 Correct! You guessed the secret number!")
            st.session_state["secret_number"] = random.randint(1, 50)
        elif guess < st.session_state["secret_number"]:
            st.warning("📈 Too low! Try a higher number.")
        else:
            st.warning("📉 Too high! Try a lower number.")

elif active_page == "❌ Tic-Tac-Toe":
    st.subheader("❌ Tic-Tac-Toe")
    if "ttt_board" not in st.session_state:
        st.session_state["ttt_board"] = [""] * 9
        st.session_state["ttt_turn"] = "❌"

    def check_winner(b):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for x,y,z in wins:
            if b[x] and b[x] == b[y] == b[z]:
                return b[x]
        if "" not in b:
            return "Tie"
        return None

    winner = check_winner(st.session_state["ttt_board"])
    if winner:
        if winner == "Tie":
            st.info("It's a tie!")
        else:
            st.success(f"Player {winner} wins!")
        if st.button("Reset Game"):
            st.session_state["ttt_board"] = [""] * 9
            st.session_state["ttt_turn"] = "❌"
            st.rerun()
    else:
        st.write(f"Current Turn: **{st.session_state['ttt_turn']}**")
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                idx = row * 3 + col
                with cols[col]:
                    if st.button(st.session_state["ttt_board"][idx] or " ", key=f"ttt_{idx}", use_container_width=True):
                        if not st.session_state["ttt_board"][idx]:
                            st.session_state["ttt_board"][idx] = st.session_state["ttt_turn"]
                            st.session_state["ttt_turn"] = "⭕" if st.session_state["ttt_turn"] == "❌" else "❌"
                            st.rerun()

elif active_page == "🪨 Rock Paper Scissors":
    st.subheader("🪨 Rock Paper Scissors")
    choice = st.radio("Make your move:", ["Rock", "Paper", "Scissors"], horizontal=True)
    if st.button("Shoot!"):
        comp_choice = random.choice(["Rock", "Paper", "Scissors"])
        st.write(f"Computer chose: **{comp_choice}**")
        if choice == comp_choice:
            st.info("It's a tie!")
        elif (choice == "Rock" and comp_choice == "Scissors") or \
             (choice == "Paper" and comp_choice == "Rock") or \
             (choice == "Scissors" and comp_choice == "Paper"):
            st.success("🎉 You win!")
        else:
            st.error("💀 You lose!")

elif active_page == "🚀 Asteroid Dodge":
    st.subheader("🚀 Asteroid Dodge Mini-Game")
    st.write("Click inside the game area first to grab focus, then use left/right arrows to dodge!")
    asteroid_html = """
    <div tabindex="0" id="dodgeRoot" style="background: #000; color: #00ff00; padding: 20px; text-align: center; border: 2px solid #ff4b4b; border-radius: 8px; font-family: monospace; outline: none; cursor: pointer;">
        <h3>🚀 Asteroid Dodge Simulator (Click to Play)</h3>
        <canvas id="dodgeCanvas" width="400" height="200" style="background:#111; border: 1px solid #444;"></canvas>
        <script>
            const dRoot = document.getElementById("dodgeRoot");
            dRoot.focus();
            dRoot.addEventListener("click", () => dRoot.focus());

            const canvas = document.getElementById("dodgeCanvas");
            const ctx = canvas.getContext("2d");
            let shipX = 180;
            let asteroidX = Math.random() * 360;
            let asteroidY = 0;
            let score = 0;
            let active = true;

            window.addEventListener("keydown", e => {
                if(["ArrowLeft","ArrowRight"].includes(e.key)) e.preventDefault();
                if(e.key === "ArrowLeft" && shipX > 0) shipX -= 15;
                if(e.key === "ArrowRight" && shipX < 370) shipX += 15;
            });

            function loop() {
                if(!active) return;
                ctx.fillStyle = "#111";
                ctx.fillRect(0, 0, 400, 200);
                
                ctx.fillStyle = "#00ff00";
                ctx.fillRect(shipX, 170, 30, 20);

                ctx.fillStyle = "#ff4b4b";
                ctx.fillRect(asteroidX, asteroidY, 20, 20);
                asteroidY += 4;

                if(asteroidY > 200) {
                    asteroidY = 0;
                    asteroidX = Math.random() * 370;
                    score += 10;
                }

                if(asteroidY >= 150 && asteroidY <= 190 && asteroidX >= shipX - 15 && asteroidX <= shipX + 25) {
                    ctx.fillStyle = "#fff";
                    ctx.font = "20px monospace";
                    ctx.fillText("CRASH! Score: " + score, 80, 100);
                    active = false;
                    return;
                }

                ctx.fillStyle = "#fff";
                ctx.font = "12px monospace";
                ctx.fillText("Score: " + score, 10, 20);

                requestAnimationFrame(loop);
            }
            loop();
        </script>
    </div>
    """
    components.html(asteroid_html, height=300)

elif active_page == "🟡 Pac-Man":
    st.subheader("🟡 Arcade Pac-Man (4 Ghosts)")
    st.write("Click inside the arcade frame to focus, then use the **Arrow Keys** to chomp dots and avoid all 4 ghosts (**Blinky**, **Pinky**, **Inky**, and **Clyde**)!")
    
    pacman_html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background-color: #000; color: #fff; font-family: 'Courier New', Courier, monospace; text-align: center; margin: 0; padding: 10px; outline: none; }
    #pacContainer { display: inline-block; background: #000; border: 3px solid yellow; border-radius: 8px; padding: 10px; box-shadow: 0 0 15px rgba(255, 255, 0, 0.4); cursor: pointer; outline: none; }
    #pacCanvas { background-color: #000; display: block; margin: 0 auto; }
    .score-board { font-size: 16px; font-weight: bold; color: yellow; margin-bottom: 8px; }
    .instructions { font-size: 12px; color: #8b949e; margin-top: 8px; font-family: sans-serif; }
  </style>
</head>
<body tabindex="0" id="pacBody">
  <div id="pacContainer">
    <div class="score-board">SCORE: <span id="pScore">0</span> | LIVES: <span id="pLives">3</span></div>
    <canvas id="pacCanvas" width="448" height="496"></canvas>
    <div class="instructions">👉 <b>Click to focus!</b> | <b>Arrow Keys</b>: Move | <b>R</b>: Restart</div>
  </div>

  <script>
    const pBody = document.getElementById("pacBody");
    pBody.focus();
    pBody.addEventListener("click", () => pBody.focus());

    const canvas = document.getElementById("pacCanvas");
    const ctx = canvas.getContext("2d");

    const tileSize = 16;
    let score = 0;
    let lives = 3;
    let gameOver = false;

    // Authentic Classic Arcade Layout Mockup (1 = Wall, 0 = Dot, 2 = Path/House)
    const originalMap = [
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
      [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
      [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
      [1,1,1,1,1,1,0,1,1,1,1,1,2,1,1,2,1,1,1,1,1,0,1,1,1,1,1,1],
      [2,2,2,2,2,1,0,1,1,2,2,2,2,2,2,2,2,2,2,1,1,0,1,2,2,2,2,2],
      [1,1,1,1,1,1,0,1,1,2,1,1,1,2,2,1,1,1,2,1,1,0,1,1,1,1,1,1],
      [2,2,2,2,2,2,0,2,2,2,1,2,2,2,2,2,2,1,2,2,2,0,2,2,2,2,2,2],
      [1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1],
      [2,2,2,2,2,1,0,1,1,2,2,2,2,2,2,2,2,2,2,1,1,0,1,2,2,2,2,2],
      [1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
      [1,0,0,0,1,1,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,1,1,0,0,0,1],
      [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
      [1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
      [1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ];
    let map = JSON.parse(JSON.stringify(originalMap));

    let pacman = { x: 13 * tileSize, y: 16 * tileSize, speed: 2, dir: 0, nextDir: 0 };
    
    // 4 Ghosts: Blinky (Red), Pinky (Pink), Inky (Cyan), Clyde (Orange)
    let ghosts = [
      { x: 13 * tileSize, y: 8 * tileSize, speed: 1.5, color: '#ff0000', dx: 0, dy: -1.5 },
      { x: 12 * tileSize, y: 10 * tileSize, speed: 1.5, color: '#ffb8ff', dx: 1.5, dy: 0 },
      { x: 14 * tileSize, y: 10 * tileSize, speed: 1.5, color: '#00ffff', dx: -1.5, dy: 0 },
      { x: 13 * tileSize, y: 10 * tileSize, speed: 1.5, color: '#ffb852', dx: 0, dy: 1.5 }
    ];

    window.addEventListener("keydown", e => {
      if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(e.key)) e.preventDefault();
      if(gameOver && e.key.toLowerCase() === 'r') { resetGame(); return; }
      if(e.key === "ArrowUp") pacman.nextDir = 1;
      if(e.key === "ArrowDown") pacman.nextDir = 2;
      if(e.key === "ArrowLeft") pacman.nextDir = 3;
      if(e.key === "ArrowRight") pacman.nextDir = 4;
    });

    function getVelocity(dir) {
      if (dir === 1) return {dx: 0, dy: -pacman.speed};
      if (dir === 2) return {dx: 0, dy: pacman.speed};
      if (dir === 3) return {dx: -pacman.speed, dy: 0};
      if (dir === 4) return {dx: pacman.speed, dy: 0};
      return {dx: 0, dy: 0};
    }

    function checkWall(x, y) {
      const buffer = 3;
      let points = [
        {x: x + buffer, y: y + buffer},
        {x: x + tileSize - buffer, y: y + buffer},
        {x: x + buffer, y: y + tileSize - buffer},
        {x: x + tileSize - buffer, y: y + tileSize - buffer}
      ];
      for (let p of points) {
        let r = Math.floor(p.y / tileSize);
        let c = Math.floor(p.x / tileSize);
        if (r < 0 || r >= map.length || c < 0 || c >= map[0].length) return true;
        if (map[r][c] === 1) return true;
      }
      return false;
    }

    function update() {
      if (gameOver) return;

      // Pac-Man movement
      if (pacman.nextDir !== 0 && pacman.x % tileSize === 0 && pacman.y % tileSize === 0) {
        let nextV = getVelocity(pacman.nextDir);
        if (!checkWall(pacman.x + nextV.dx, pacman.y + nextV.dy)) {
          pacman.dir = pacman.nextDir;
        }
      }

      let v = getVelocity(pacman.dir);
      let nx = pacman.x + v.dx;
      let ny = pacman.y + v.dy;

      // Screen wrap tunnel
      if (nx < -tileSize/2) nx = map[0].length * tileSize - tileSize/2;
      if (nx > map[0].length * tileSize - tileSize/2) nx = -tileSize/2;

      if (!checkWall(nx, ny)) {
        pacman.x = nx;
        pacman.y = ny;
      } else {
        pacman.dir = 0;
      }

      // Eat dots
      let row = Math.floor((pacman.y + tileSize/2) / tileSize);
      let col = Math.floor((pacman.x + tileSize/2) / tileSize);
      if (map[row] && map[row][col] === 0) {
        map[row][col] = 2;
        score += 10;
        document.getElementById("pScore").innerText = score;
      }

      // Ghost movement & collision
      ghosts.forEach(g => {
        g.x += g.dx;
        g.y += g.dy;
        if (checkWall(g.x, g.y)) {
          g.dx = -g.dx;
          g.dy = -g.dy;
          g.x += g.dx * 2;
          g.y += g.dy * 2;
        }

        // Check collision with Pac-Man
        let dist = Math.hypot((pacman.x + tileSize/2) - (g.x + tileSize/2), (pacman.y + tileSize/2) - (g.y + tileSize/2));
        if (dist < tileSize * 0.75) {
          lives--;
          document.getElementById("pLives").innerText = lives;
          if (lives <= 0) {
            gameOver = true;
          } else {
            pacman.x = 13 * tileSize;
            pacman.y = 16 * tileSize;
            pacman.dir = 0;
            pacman.nextDir = 0;
          }
        }
      });
    }

    function draw() {
      ctx.fillStyle = "#000";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw map
      for (let r = 0; r < map.length; r++) {
        for (let c = 0; c < map[r].length; c++) {
          if (map[r][c] === 1) {
            ctx.fillStyle = "#1919a6";
            ctx.fillRect(c * tileSize, r * tileSize, tileSize, tileSize);
          } else if (map[r][c] === 0) {
            ctx.fillStyle = "#ffb8ae";
            ctx.beginPath();
            ctx.arc(c * tileSize + tileSize/2, r * tileSize + tileSize/2, 3, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      // Draw Pac-Man
      ctx.fillStyle = "yellow";
      ctx.beginPath();
      let angle = 0.2;
      if (pacman.dir === 1) angle = 1.7;
      if (pacman.dir === 2) angle = 0.7;
      if (pacman.dir === 3) angle = 1.2;
      if (pacman.dir === 4) angle = 0.2;
      ctx.arc(pacman.x + tileSize/2, pacman.y + tileSize/2, tileSize/2 - 1, angle * Math.PI, (angle + 1.6) * Math.PI);
      ctx.lineTo(pacman.x + tileSize/2, pacman.y + tileSize/2);
      ctx.fill();

      // Draw Ghosts
      ghosts.forEach(g => {
        ctx.fillStyle = g.color;
        ctx.beginPath();
        ctx.arc(g.x + tileSize/2, g.y + tileSize/2 - 1, tileSize/2 - 1, Math.PI, 0, false);
        ctx.lineTo(g.x + tileSize - 2, g.y + tileSize);
        ctx.lineTo(g.x + 2, g.y + tileSize);
        ctx.fill();
      });

      if (gameOver) {
        ctx.fillStyle = "rgba(0,0,0,0.8)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ff4b4b";
        ctx.font = "24px 'Courier New'";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width/2, canvas.height/2 - 10);
        ctx.font = "14px sans-serif";
        ctx.fillStyle = "#fff";
        ctx.fillText("Press R to Restart", canvas.width/2, canvas.height/2 + 20);
      }
    }

    function resetGame() {
      map = JSON.parse(JSON.stringify(originalMap));
      score = 0;
      lives = 3;
      gameOver = false;
      document.getElementById("pScore").innerText = score;
      document.getElementById("pLives").innerText = lives;
      pacman.x = 13 * tileSize;
      pacman.y = 16 * tileSize;
      pacman.dir = 0;
      pacman.nextDir = 0;
    }

    function loop() {
      update();
      draw();
      requestAnimationFrame(loop);
    }

    loop();
  </script>
</body>
</html>
"""
    components.html(pacman_html, height=550)

elif active_page == "💡 Feature Requests":
    st.subheader("💡 Portal Feature Requests")
    with st.form("feature_form", clear_on_submit=True):
        req = st.text_input("What feature should we add next?")
        if st.form_submit_button("Submit Request"):
            if req.strip():
                st.session_state["feature_requests"].append({"user": st.session_state["nickname"], "text": req.strip()})
                st.success("Feature request submitted successfully!")
                st.rerun()

    st.write("### Submitted Ideas:")
    if not st.session_state["feature_requests"]:
        st.info("No feature requests yet. Be the first to suggest one!")
    else:
        for fr in st.session_state["feature_requests"]:
            st.markdown(f"- **{fr['user']}**: {fr['text']}")

elif active_page == "🎨 Goofy Sketchpad":
    st.subheader("🎨 Goofy Sketchpad")
    st.write("Draw something goofy and leave your mark on the portal!")
    
    sketch_html = """
    <div style="text-align: center;">
        <canvas id="drawCanvas" width="400" height="250" style="background: white; border: 2px solid #ccc; cursor: crosshair;"></canvas>
        <br>
        <button onclick="clearCanvas()" style="margin-top: 10px; padding: 6px 12px; background: #ff4b4b; color: white; border: none; border-radius: 4px; cursor: pointer;">Clear Canvas</button>
        <script>
            const dCanvas = document.getElementById("drawCanvas");
            const dCtx = dCanvas.getContext("2d");
            let painting = false;
            dCtx.lineWidth = 3;
            dCtx.lineCap = "round";
            dCtx.strokeStyle = "#ff4b4b";

            dCanvas.addEventListener("mousedown", e => { painting = true; draw(e); });
            dCanvas.addEventListener("mouseup", () => { painting = false; dCtx.beginPath(); });
            dCanvas.addEventListener("mousemove", draw);

            function draw(e) {
                if(!painting) return;
                const rect = dCanvas.getBoundingClientRect();
                dCtx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
                dCtx.stroke();
                dCtx.beginPath();
                dCtx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
            }

            function clearCanvas() {
                dCtx.clearRect(0, 0, dCanvas.width, dCanvas.height);
            }
        </script>
    </div>
    """
    components.html(sketch_html, height=330)

elif active_page == "📊 Gang Polls":
    st.subheader("📊 Gang Polls")
    with st.form("poll_form", clear_on_submit=True):
        p_q = st.text_input("Poll Question:")
        opt1 = st.text_input("Option A:")
        opt2 = st.text_input("Option B:")
        if st.form_submit_button("Create Poll"):
            if p_q and opt1 and opt2:
                st.session_state["polls"].append({
                    "question": p_q,
                    "options": {opt1: 0, opt2: 0},
                    "voted": []
                })
                st.success("Poll created!")
                st.rerun()

    st.write("### Active Polls:")
    if not st.session_state["polls"]:
        st.info("No active polls right now. Create one above!")
    else:
        for idx, poll in enumerate(st.session_state["polls"]):
            st.markdown(f"**Q: {poll['question']}**")
            if st.session_state["nickname"] in poll["voted"]:
                st.info("You already voted in this poll!")
                for opt, count in poll["options"].items():
                    st.write(f"- {opt}: **{count} votes**")
            else:
                chosen = st.radio("Choose option:", list(poll["options"].keys()), key=f"poll_choice_{idx}")
                if st.button("Cast Vote", key=f"vote_btn_{idx}"):
                    poll["options"][chosen] += 1
                    poll["voted"].append(st.session_state["nickname"])
                    st.success("Vote recorded!")
                    st.rerun()
            st.divider()

elif active_page == "📅 Gang Calendar":
    st.subheader("📅 Gang Calendar & Schedule")
    st.caption("Coordinate hangouts, events, and important dates with the crew!")

    with st.form("calendar_form", clear_on_submit=True):
        event_title = st.text_input("Event Name:")
        event_date = st.date_input("Event Date:")
        event_desc = st.text_area("Details / Description:")
        if st.form_submit_button("Add Event"):
            if event_title.strip():
                st.session_state["calendar_events"].append({
                    "title": event_title.strip(),
                    "date": str(event_date),
                    "desc": event_desc.strip(),
                    "creator": st.session_state["nickname"]
                })
                st.success("Event added successfully!")
                st.rerun()

    st.write("### Upcoming Gang Events:")
    if not st.session_state["calendar_events"]:
        st.info("No events scheduled yet. Add one above!")
    else:
        sorted_events = sorted(st.session_state["calendar_events"], key=lambda x: x["date"])
        for ev in sorted_events:
            with st.container(border=True):
                st.markdown(f"#### 🗓️ {ev['title']}")
                st.write(f"**Date:** `{ev['date']}` | **Added by:** {ev['creator']}")
                if ev['desc']:
                    st.write(ev['desc'])

elif active_page == "👑 Admin Controls":
    st.subheader("👑 Admin Controls (Calvin & Cal Only)")
    st.write("Manage portal access and user status.")
    
    target_user = st.selectbox("Select Member:", [u for u in ALLOWED_USERS if u not in ["calvin", "cal"]])
    if target_user in st.session_state["banned_users"]:
        st.warning(f"Status for **{target_user}**: Banned 🚫")
        if st.button(f"Unban {target_user}"):
            st.session_state["banned_users"].remove(target_user)
            st.success(f"Unbanned {target_user} successfully!")
            st.rerun()
    else:
        st.success(f"Status for **{target_user}**: Active ✅")
        if st.button(f"Ban {target_user}"):
            st.session_state["banned_users"].append(target_user)
            st.error(f"Banned {target_user} from the portal!")
            st.rerun()

    st.write("### Current Banned List:")
    st.write(st.session_state["banned_users"] if st.session_state["banned_users"] else "None")
