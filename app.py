import streamlit as st

# App Configuration
st.set_page_config(
    page_title="Goofy Gang Portal",
    page_icon="🤪",
    layout="centered"
)

# Initialize Session State
if "feature_requests" not in st.session_state:
    st.session_state.feature_requests = []

if "username" not in st.session_state:
    st.session_state.username = "Guest"

# Sidebar for User Settings & Admin
st.sidebar.title("🛠️ Portal Controls")
username_input = st.sidebar.text_input("Enter your name:", value=st.session_state.username)
if username_input:
    st.session_state.username = username_input

# Main Portal Header
st.title("🤪 Goofy Gang Portal")
st.write(f"Welcome back, **{st.session_state.username}**! Ready for some fun?")

# Admin Section (Calvin Controls)
if st.session_state.username.lower() == "calvin":
    st.sidebar.success("👑 Admin Mode Active (Calvin)")
    admin_action = st.sidebar.selectbox("Admin Actions", ["View Stats", "Manage Users", "Clear Requests"])
    if admin_action == "Clear Requests" and st.sidebar.button("Clear All Feature Requests"):
        st.session_state.feature_requests = []
        st.sidebar.success("All requests cleared!")

# Portal Features / Games Section
st.divider()
st.subheader("🎮 Portal Hub")

tab1, tab2, tab3 = st.tabs(["Mini Games", "Gang Wall", "💡 Feature Requests"])

with tab1:
    st.markdown("### Choose a Game")
    game_choice = st.selectbox("Select a game to play:", ["Coin Flip", "Guess the Number", "Goofy Soundboard"])
    
    if game_choice == "Coin Flip":
        if st.button("Flip Coin"):
            import random
            result = random.choice(["Heads", "Tails"])
            st.info(f"The coin landed on: **{result}**")
            
    elif game_choice == "Guess_the_Number" or game_choice == "Guess the Number":
        st.write("Guess a number between 1 and 10!")
        guess = st.slider("Your Guess", 1, 10, 5)
        if st.button("Submit Guess"):
            import random
            secret = random.randint(1, 10)
            if guess == secret:
                st.success(f"🎉 Spot on! It was {secret}.")
            else:
                st.error(f"❌ Nope! The number was {secret}.")
                
    elif game_choice == "Goofy Soundboard":
        st.write("Click to play sound effects:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📢 Honk"):
                st.toast("HONK HONK! 🚗")
        with col2:
            if st.button("🤪 Boing"):
                st.toast("BOINGGG! 🛜")

with tab2:
    st.markdown("### 💬 Gang Wall")
    st.write("Leave a message for the rest of the gang:")
    msg = st.text_input("Say something goofy...")
    if st.button("Post Message"):
        if msg.strip():
            st.success(f"**{st.session_state.username}**: {msg}")
        else:
            st.warning("Type a message first!")

with tab3:
    st.markdown("### 💡 Feature Requests")
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
