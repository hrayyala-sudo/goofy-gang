import streamlit as st
import streamlit.components.v1 as components
import random

# App Configuration
st.set_page_config(
    page_title="Goofy Gang Portal",
    page_icon="🤪",
    layout="wide"
)

# Initialize Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "feature_requests" not in st.session_state:
    st.session_state.feature_requests = []

# Login Screen if not authenticated
if not st.session_state.logged_in:
    st.title("🤪 Goofy Gang Portal - Login")
    st.write("Please enter your name to enter the portal:")
    
    name_input = st.text_input("Username")
    if st.button("Log In"):
        if name_input.strip():
            st.session_state.username = name_input.strip()
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("Please enter a valid username.")
    st.stop()

# Sidebar Navigation
st.sidebar.title(f"👋 Hello, {st.session_state.username}")
if st.session_state.username.lower() == "calvin":
    st.sidebar.success("👑 Admin Mode Active (Calvin)")
    admin_action = st.sidebar.selectbox("Admin Actions", ["None", "Clear Chat", "Clear Requests"])
    if admin_action == "Clear Chat" and st.sidebar.button("Execute Clear Chat"):
        st.session_state.messages = []
        st.sidebar.success("Chat cleared!")
    elif admin_action == "Clear Requests" and st.sidebar.button("Execute Clear Requests"):
        st.session_state.feature_requests = []
        st.sidebar.success("Requests cleared!")

page = st.sidebar.radio("Navigation", ["Home Hub", "🕹️ Pac-Man", "🚀 Asteroid Dodge", "💬 Gang Chat", "💡 Feature Requests"])

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# Page Routing
if page == "Home Hub":
    st.title("🤪 Goofy Gang Portal")
    st.write(f"Welcome back, **{st.session_state.username}**! Select a section from the sidebar to start playing or chatting.")
    
    st.divider()
    st.subheader("Quick Launch")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Play Pac-Man"):
            st.info("Switch to Pac-Man in the sidebar!")
    with col2:
        if st.button("Play Asteroid Dodge"):
            st.info("Switch to Asteroid Dodge in the sidebar!")
    with col3:
        if st.button("Open Gang Chat"):
            st.info("Switch to Gang Chat in the sidebar!")
    with col4:
        if st.button("Feature Requests"):
            st.info("Switch to Feature Requests in the sidebar!")

elif page == "🕹️ Pac-Man":
    st.title("🕹️ Pac-Man Arcade")
    st.write("Classic arcade action right inside your portal!")
    
    pacman_html = """
    <div style="text-align: center; background: black; padding: 20px; border-radius: 10px; color: white;">
        <h3>Retro Arcade: Pac-Chomp</h3>
        <canvas id="gameCanvas" width="400" height="400" style="background: #111; border: 2px solid yellow;"></canvas>
        <p>Use Arrow Keys to move your character and collect the dots!</p>
        <script>
            const canvas = document.getElementById("gameCanvas");
            const ctx = canvas.getContext("2d");
            let x = 200, y = 200, dx = 0, dy = 0;
            let dotX = Math.random() * 350 + 25, dotY = Math.random() * 350 + 25;
            let score = 0;

            document.addEventListener("keydown", (e) => {
                if (e.key === "ArrowUp") { dx = 0; dy = -3; }
                if (e.key === "ArrowDown") { dx = 0; dy = 3; }
                if (e.key === "ArrowLeft") { dx = -3; dy = 0; }
                if (e.key === "ArrowRight") { dx = 3; dy = 0; }
            });

            function update() {
                x += dx; y += dy;
                if (x < 0) x = canvas.width;
                if (x > canvas.width) x = 0;
                if (y < 0) y = canvas.height;
                if (y > canvas.height) y = 0;

                let dist = Math.hypot(x - dotX, y - dotY);
                if (dist < 20) {
                    score += 10;
                    dotX = Math.random() * 350 + 25;
                    dotY = Math.random() * 350 + 25;
                }
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "pink";
                ctx.beginPath();
                ctx.arc(dotX, dotY, 6, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "yellow";
                ctx.beginPath();
                ctx.arc(x, y, 12, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "white";
                ctx.font = "16px Arial";
                ctx.fillText("Score: " + score, 10, 25);
            }

            setInterval(() => {
                update();
                draw();
            }, 1000 / 60);
        </script>
    </div>
    """
    components.html(pacman_html, height=520)

elif page == "🚀 Asteroid Dodge":
    st.title("🚀 Asteroid Dodge")
    st.write("Pilot your ship and avoid incoming space debris!")
    
    asteroid_html = """
    <div style="text-align: center; background: #0b0b1a; padding: 20px; border-radius: 10px; color: white;">
        <h3>Space Survival</h3>
        <canvas id="spaceCanvas" width="450" height="350" style="background: #000; border: 2px solid cyan;"></canvas>
        <p>Move Mouse or Left/Right Arrow Keys to dodge asteroids!</p>
        <script>
            const sCanvas = document.getElementById("spaceCanvas");
            const sCtx = sCanvas.getContext("2d");
            let shipX = 225;
            let asteroids = [];
            let survivalScore = 0;
            let isGameOver = false;

            document.addEventListener("keydown", (e) => {
                if (e.key === "ArrowLeft" && shipX > 20) shipX -= 20;
                if (e.key === "ArrowRight" && shipX < sCanvas.width - 20) shipX += 20;
            });

            sCanvas.addEventListener("mousemove", (e) => {
                let rect = sCanvas.getBoundingClientRect();
                shipX = e.clientX - rect.left;
            });

            function spawnAsteroid() {
                asteroids.push({
                    x: Math.random() * sCanvas.width,
                    y: -20,
                    size: Math.random() * 15 + 10,
                    speed: Math.random() * 3 + 2
                });
            }

            setInterval(spawnAsteroid, 800);

            function updateSpace() {
                if (isGameOver) return;
                survivalScore++;
                for (let i = asteroids.length - 1; i >= 0; i--) {
                    asteroids[i].y += asteroids[i].speed;
                    let d = Math.hypot(shipX - asteroids[i].x, (sCanvas.height - 30) - asteroids[i].y);
                    if (d < asteroids[i].size + 10) {
                        isGameOver = true;
                    }
                    if (asteroids[i].y > sCanvas.height) {
                        asteroids.splice(i, 1);
                    }
                }
            }

            function drawSpace() {
                sCtx.clearRect(0, 0, sCanvas.width, sCanvas.height);
                sCtx.fillStyle = "cyan";
                sCtx.beginPath();
                sCtx.moveTo(shipX, sCanvas.height - 40);
                sCtx.lineTo(shipX - 15, sCanvas.height - 10);
                sCtx.lineTo(shipX + 15, sCanvas.height - 10);
                sCtx.fill();

                sCtx.fillStyle = "gray";
                for (let ast of asteroids) {
                    sCtx.beginPath();
                    sCtx.arc(ast.x, ast.y, ast.size, 0, Math.PI * 2);
                    sCtx.fill();
                }

                sCtx.fillStyle = "white";
                sCtx.font = "16px Arial";
                sCtx.fillText("Score: " + survivalScore, 15, 25);

                if (isGameOver) {
                    sCtx.fillStyle = "red";
                    sCtx.font = "30px Arial";
                    sCtx.fillText("GAME OVER", sCanvas.width / 2 - 90, sCanvas.height / 2);
                }
            }

            setInterval(() => {
                updateSpace();
                drawSpace();
            }, 1000 / 60);
        </script>
    </div>
    """
    components.html(asteroid_html, height=480)

elif page == "💬 Gang Chat":
    st.title("💬 Gang Chatbox")
    st.write("Chat live with everyone in the portal using the modern chat interface below!")

    # Display chat history using native Streamlit chat UI
    for message in st.session_state.messages:
        with st.chat_message(message["user"]):
            st.markdown(message["text"])

    # Accept user input via chat box at the bottom
    if prompt := st.chat_input("Say something goofy to the gang..."):
        st.session_state.messages.append({"user": st.session_state.username, "text": prompt})
        with st.chat_message(st.session_state.username):
            st.markdown(prompt)

elif page == "💡 Feature Requests":
    st.title("💡 Feature Requests")
    st.write("Got an idea for a new game or feature? Submit it below for Calvin and the team to review!")
    
    feature_input = st.text_input("Suggest a new game or feature:")
    if st.button("Submit Request"):
        if feature_input.strip():
            st.session_state.feature_requests.append({
                "user": st.session_state.username,
                "text": feature_input
            })
            st.success("Feature request logged successfully!")
        else:
            st.warning("Please type a description first.")

    if st.session_state.feature_requests:
        st.markdown("#### Submitted Feature Ideas")
        for idx, req in enumerate(st.session_state.feature_requests, 1):
            st.markdown(f"{idx}. **{req['user']}**: {req['text']}")
