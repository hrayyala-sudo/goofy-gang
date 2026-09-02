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
