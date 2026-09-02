# --- 5. MAIN HEADER WITH BIG BOSS TRIGGER ICON ---
st.markdown("""
<style>
    /* Make the button invisible so only the big emoji shows */
    div.big-boss-btn > button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 75px !important;
        cursor: pointer !important;
        padding: 0 !important;
        margin: 0 !important;
        line-height: 1 !important;
        outline: none !important;
    }
    div.big-boss-btn > button:hover,
    div.big-boss-btn > button:focus,
    div.big-boss-btn > button:active {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

title_col1, title_col2 = st.columns([0.12, 0.88])

with title_col1:
    st.markdown('<div class="big-boss-btn">', unsafe_allow_html=True)
    if st.button("🤪", key="big_header_boss_btn"):
        st.session_state["show_secret_game"] = not st.session_state["show_secret_game"]
    st.markdown('</div>', unsafe_allow_html=True)

with title_col2:
    st.title("Goofy Gang Dashboard")

st.markdown("---")
