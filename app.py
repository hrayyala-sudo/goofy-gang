import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🤪", layout="wide")

# Allowed Users & Password
ALLOWED_USERS = ["pranav", "calvin", "austin", "goofy member"]
CORRECT_PASSWORD = "goofy123"

# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "nickname" not in st.session_state:
    st.session_state["nickname"] = ""
if "show_secret_game" not in st.session_state:
    st.session_state["show_secret_game"] = False

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
    st.markdown("""
    <style>
        .element-container:has(div.secret-logo-wrapper) {
            position: absolute;
            top: 0;
            right: 10px;
            z-index: 999;
        }
        div.secret-logo-wrapper > button {
            background: none !important;
            border: none !important;
            box-shadow: none !important;
            font-size: 85px !important;
            cursor: pointer;
            padding: 0 !important;
            margin: 0 !important;
            line-height: 1 !important;
            transition: transform 0.2s ease;
        }
        div.secret-logo-wrapper > button:hover {
            transform: scale(1.1) rotate(5deg);
        }
        div.secret-logo-wrapper > button:active {
            transform: scale(0.95);
        }
    </style>
    """, unsafe_allow_html=True)

    header_col, logo_col = st.columns([5, 1])

    with header_col:
        st.header("💬 Goofy Chatbox")
        st.write("Welcome to the main chat room! Messages update for everyone.")

    with logo_col:
        st.markdown('<div class="secret-logo-wrapper">', unsafe_allow_html=True)
        if st.button("🤪", key="secret_chat_logo"):
            st.session_state["show_secret_game"] = not st.session_state["show_secret_game"]
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SECRET GOOFY BOSS GAME OVERLAY ---
    if st.session_state["show_secret_game"]:
        st.info("🎉 **SECRET UNLOCKED!** You tapped the giant Goofy Gang icon!")
        
        secret_game_html = """<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      background-color: #161b22;
      color: white;
      font-family: Arial, sans-serif;
      text-align: center;
      margin: 0;
      padding: 15px;
      border: 3px dashed #ff4b4b;
      border-radius: 12px;
    }
    .boss-target {
      font-size: 80px;
      cursor: pointer;
      user-select: none;
      display: inline-block;
      transition: transform 0.05s ease;
      margin: 15px 0;
    }
    .boss-target:active {
      transform: scale(1.3) rotate(15deg);
    }
    .health-bar-container {
      width: 80%;
      height: 24px;
      background-color: #30363d;
      border-radius: 12px;
      margin: 10px auto;
      overflow: hidden;
      border: 2px solid #ffffff;
    }
    .health-bar {
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, #ff4b4b, #ff8c00);
      transition: width 0.1s ease;
    }
    .stats {
      font-size: 18px;
      font-weight: bold;
    }
    .win-msg {
      color: #00ff00;
      font-size: 26px;
      font-weight: bold;
    }
    button {
      background-color: #238636;
      color: white;
      border: none;
      padding: 8px 16px;
      font-size: 14px;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 10px;
    }
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
        
        if (timeLeft <= 0) {
          endGame(false);
        }
      }, 1000);
    }

    function hitBoss() {
      if (!gameActive) return;
      
      hits++;
      const hpPercent = Math.max(0, 100 - (hits / maxHits * 100));
      document.getElementById("hpBar").style.width = hpPercent + "%";
      document.getElementById("scoreText").innerText = "Hits: " + hits + " / " + maxHits;

      if (hits >= maxHits) {
        endGame(true);
      }
    }

    function endGame(won) {
      gameActive = false;
      clearInterval(timer);
      const res = document.getElementById("resultText");
      const target = document.getElementById("target");

      if (won) {
        target.innerText = "😵‍💫";
        res.innerHTML = "<div class='win-msg'>🏆 YOU SMASHED THE GOOFY BOSS! 🏆</div><button onclick='resetGame()'>Play Again</button>";
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
            with st.chat_message("user" if msg["sender"].lower() == st.session_state["nickname"].lower() else "assistant"):
                st.markdown(f"**{msg['sender']}** *({msg
