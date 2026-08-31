import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration & Setup
st.set_page_config(page_title="Goofy Gang Portal", page_icon="🎉", layout="wide")

# Initialize Session State Variables
if "nickname" not in st.session_state:
    st.session_state["nickname"] = "Pranav"
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# 2. Sidebar Navigation
st.sidebar.title(f"👋 Welcome, {st.session_state['nickname']}!")

# Profile Settings
st.sidebar.markdown("### 👤 Profile Settings")
new_nickname = st.sidebar.text_input("Change Nickname:", value=st.session_state["nickname"])
if st.sidebar.button("Save New Nickname"):
    st.session_state["nickname"] = new_nickname
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📍 Navigation Pages")

page = st.sidebar.radio(
    "Go to page:",
    ["🤖 Goofy Chatbox", "🎲 Guessing Game", "❌ Tic-Tac-Toe", "🪨 Rock Paper Scissors", "🚀 Asteroid Dodge"]
)

if st.sidebar.button("Logout"):
    st.session_state["nickname"] = "Guest"
    st.rerun()

# 3. Main Dashboard Header
st.title("🎉 Goofy Gang Dashboard")
st.markdown("---")

# 4. Page Logic

# --- PAGE 1: GOOFY CHATBOX ---
if page == "🤖 Goofy Chatbox":
    st.header("🤖 Goofy Chatbox")
    st.write("Chat with the Goofy Gang AI bot below!")

    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Say something goofy...")
    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        bot_response = f"🤪 **{st.session_state['nickname']}** said: '{user_input}'! That is totally goofy!"
        st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
        st.rerun()

# --- PAGE 2: GUESSING GAME ---
elif page == "🎲 Guessing Game":
    st.header("🎲 Number Guessing Game")
    st.write("Guess the secret number between 1 and 100!")

    import random

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
            st.success(f"🎉 You got it in {st.session_state['guesses']} tries! The number was {st.session_state['secret_num']}.")
            if st.button("Play Again"):
                del st.session_state["secret_num"]
                del st.session_state["guesses"]
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
            label = st.session_state["board"][i] if st.session_state["board"][i] != "" else " "
            if st.button(label, key=f"btn_{i}", use_container_width=True):
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
    import random

    choices = ["🪨 Rock", "📄 Paper", "✂️ Scissors"]
    user_choice = st.radio("Choose your weapon:", choices)

    if st.button("Play"):
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
            st.error(" You lost! Try again.")

# --- PAGE 5: ANIMATED ASTEROID DODGE ---
elif page == "🚀 Asteroid Dodge":
    st.header("🚀 Asteroid Dodge (Arcade Edition)")
    st.write("Dodge the falling asteroids in real-time!")

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
      <div class="info">Use <b>Left / Right Arrows</b> or <b>A / D</b> to move your ship. Press <b>R</b> to restart.</div>

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
    components.html(asteroid_game_html, height=500)
