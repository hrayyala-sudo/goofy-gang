import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Streamlit Pokédex & Chat", page_icon="🔴", layout="wide")

# Initialize chat history session state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --- POKÉDEX LOGIC FUNCTIONS ---
@st.cache_data(show_spinner=False)
def fetch_pokemon_data(name_or_id):
    try:
        url = f"https://pokeapi.co{str(name_or_id).lower().strip()}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

@st.cache_data(show_spinner=False)
def get_pokemon_list(limit=151):
    try:
        url = f"https://pokeapi.co{limit}"
        response = requests.get(url)
        if response.status_code == 200:
            return [p['name'].title() for p in response.json()['results']]
    except Exception:
        pass
    return ["Pikachu"]

# --- APP HEADER ---
st.title("🔴 Streamlit Pokédex Portal")
st.write("Browse your favorite Pokémon and chat with the Goofy Gang dashboard.")

# --- SIDEBAR: SEARCH & NAVIGATION ---
st.sidebar.header("🔍 Search & Filter")
pokemon_list = get_pokemon_list()
selected_pokemon = st.sidebar.selectbox("Choose a Pokémon:", pokemon_list)
search_query = st.sidebar.text_input("Or type name/ID manually:")

lookup_target = search_query if search_query else selected_pokemon

# --- MAIN SECTION: POKÉDEX APPLICATION ---
if lookup_target:
    with st.spinner(f"Fetching data for {lookup_target}..."):
        data = fetch_pokemon_data(lookup_target)
        if data:
            col1, col2 = st.columns([1, 2])
            with col1:
                image_url = data['sprites']['other']['official-artwork']['front_default']
                if image_url:
                    st.image(image_url, use_column_width=True)
                else:
                    st.image(data['sprites']['front_default'], use_column_width=True)
                st.metric(label="Pokédex ID", value=f"#{data['id']:03d}")
                
            with col2:
                st.header(data['name'].title())
                types = [t['type']['name'].title() for t in data['types']]
                st.subheader("Type")
                st.write(" | ".join(types))
                
                col_weight, col_height = st.columns(2)
                with col_weight:
                    st.metric(label="Weight", value=f"{data['weight'] / 10} kg")
                with col_height:
                    st.metric(label="Height", value=f"{data['height'] / 10} m")
                    
                st.subheader("Base Stats")
                stats_dict = {s['stat']['name'].replace('-', ' ').title(): s['base_stat'] for s in data['stats']}
                for stat_name, stat_value in stats_dict.items():
                    st.write(f"**{stat_name}**: {stat_value}")
                    st.progress(min(stat_value / 255.0, 1.0))
                    
                st.subheader("Abilities")
                abilities = [a['ability']['name'].replace('-', ' ').title() for a in data['abilities']]
                st.write(", ".join(abilities))
        else:
            st.error(f"Could not find Pokémon: '{lookup_target}'. Please check the spelling or ID.")

st.divider()

# --- BOTTOM SECTION: INTEGRATED CHATBOX ---
st.header("💬 Goofy Chat Box")
st.write("Leave a message for the gang right below the tool!")

# Display message history log
chat_container = st.container(height=250)
with chat_container:
    if not st.session_state.chat_messages:
        st.info("No messages yet. Be the first to say hello!")
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(f"**{msg['user']}**: {msg['text']}")

# Live message input box
if prompt := st.chat_input("Type a message to the group..."):
    st.session_state.chat_messages.append({
        "role": "user",
        "user": "Pranav",
        "text": prompt
    })
    st.rerun()
