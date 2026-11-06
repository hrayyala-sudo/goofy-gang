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
ALLOWED_USERS = ["pranav", "calvin", "austin", "isaac", "george", "isaiah", "fox"]

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
                st.error("🚫 You have been banned from the portal by Calvin!")
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

st.sidebar.divider()
st.sidebar.markdown("**Pages**")
pages_list = [
    "💬 Goofy Chatbox", 
    "🎲 Guessing Game", 
    "❌ Tic-Tac-Toe", 
    "🪨 Rock Paper Scissors", 
    "🚀 Asteroid Dodge", 
    "🟡 Pac-Man", 
    "💡 Feature Requests",
    "🎨 Goofy Sketchpad",
    "📊 Gang Polls"
]
if st.session_state["nickname"].strip().lower() == "calvin":
    pages_list.append("👑 Admin Controls")

if st.session_state["active_page"] not in pages_list:
    st.session_state["active_page"] = pages_list[0]

if "nav_radio" not in st.session_state or st.session_state["nav_radio"] not in pages_list:
    st.session_state["nav_radio"] = st.session_state["active_page"]

def on_nav_change():
    st.session_state["active_page"] = st.session_state["nav_radio"]

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

# --- 5. MAIN HEADER WITH DECORATED TETRIS TOGGLE ---
col_btn, col_title = st.columns([0.06, 0.94])
with col_btn:
    if st.button("🤪", help="Click to open/close Secret Tetris!", key="secret_tetris_btn"):
        st.session_state["show_secret_game"] = not st.session_state["show_secret_game"]
        st.rerun()
with col_title:
    st.markdown("<h1 style='margin: 0; padding-top: 5px; font-size: 2.25rem; font-weight: 700;'>Goofy Gang Dashboard</h1>", unsafe_allow_html=True)

st.markdown("---")

# --- SECRET TETRIS OVERLAY ---
if st.session_state["show_secret_game"]:
    st.info("🎮 **SECRET TETRIS UNLOCKED!** Enjoy stacking blocks right here.")
    
    tetris_html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { background-color: #0e1117; color: white; font-family: 'Courier New', Courier, monospace; text-align: center; margin: 0; padding: 10px; overflow: hidden; }
    .game-container { display: flex; justify-content: center; align-items: flex-start; gap: 20px; margin-top: 10px; }
    #tetrisCanvas { background-color: #000; border: 3px solid #ff4b4b; border-radius: 6px; box-shadow: 0 0 12px rgba(255, 75, 75, 0.4); width: 220px; height: 380px; display: block; }
    .sidebar-panel { background: #161b22; border: 2px solid #30363d; border-radius: 8px; padding: 12px; width: 130px; text-align: left; box-sizing: border-box; }
    .panel-title { font-size: 11px; color: #8b949e; text-transform: uppercase; margin-bottom: 3px; }
    .panel-value { font-size: 18px; font-weight: bold; color: #00ff00; margin-bottom: 12px; }
    #nextCanvas { background: #000; border: 1px solid #30363d; border-radius: 4px; display: block; width: 70px; height: 70px; }
    .controls-info { margin-top: 12px; font-size: 12px; color: #8b949e; font-family: sans-serif; }
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
    <b>Left/Right Arrow</b>: Move | <b>Up Arrow</b>: Rotate | <b>Down Arrow</b>: Drop | <b>Spacebar</b>: Hard Drop | <b>R</b>: Reset
  </div>

  <script>
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

    document.addEventListener("keydown", event => {
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
st.write(f"### Currently Viewing: {st.session_state['active_page']}")
