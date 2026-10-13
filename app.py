import streamlit as st
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("GEMINI_API_KEY is not set!")
    st.stop()

client = genai.Client(api_key=api_key)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Dungeon Master ⚔️",
    page_icon="⚔️",
    layout="centered"
)

# ── Configure Gemini ───────────────────────────────────────────────────────────
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
}
.hero h1 {
    font-family: 'Cinzel', serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #d4af37, #ff6b35, #d4af37);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
}
.hero p { color: #888; font-size: 0.95rem; font-style: italic; }

.dm-message {
    background: linear-gradient(135deg, #0d0a00, #1a1200);
    border: 1px solid #d4af3744;
    border-left: 3px solid #d4af37;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 12px 0;
    color: #f5e6c0;
    font-size: 0.95rem;
    line-height: 1.7;
}

.player-message {
    background: #0a0f1a;
    border: 1px solid #3b82f644;
    border-right: 3px solid #3b82f6;
    border-radius: 12px 0 0 12px;
    padding: 16px 20px;
    margin: 12px 0;
    color: #bfdbfe;
    font-size: 0.95rem;
    line-height: 1.7;
    text-align: right;
}

.dm-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #d4af37;
    margin-bottom: 6px;
}

.player-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 6px;
    text-align: right;
}

.stat-bar {
    background: #111;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
}
.stat-value {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #d4af37;
}
.stat-label {
    font-size: 0.65rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

.scenario-card {
    background: #0d0a00;
    border: 1px solid #d4af3733;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
}
.scenario-title {
    font-family: 'Cinzel', serif;
    color: #d4af37;
    font-size: 0.95rem;
    font-weight: 600;
}
.scenario-desc { color: #888; font-size: 0.8rem; margin-top: 4px; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────────────────────
DM_SYSTEM_PROMPT = """You are an expert, creative, and immersive Dungeon Master for a text-based RPG adventure. Your role is to:

1. Create vivid, atmospheric descriptions of locations, characters, and events
2. React dynamically to player choices — every decision matters and has consequences
3. Introduce interesting NPCs, plot twists, mysteries, and challenges
4. Track the story state and remember what happened earlier in the adventure
5. Offer 3-4 clear action choices at the end of each response, formatted as:
   **What do you do?**
   • [Action 1]
   • [Action 2]
   • [Action 3]
   • [Something else entirely...]

Keep responses engaging but concise (150-250 words). Use vivid sensory details. Build tension and atmosphere. Make the player feel like the hero of an epic story. Never break character."""

# ── Scenarios ──────────────────────────────────────────────────────────────────
SCENARIOS = [
    {
        "title": "⚔️ The Cursed Kingdom",
        "desc": "A dark curse has fallen over the land. You are the last hope.",
        "prompt": "Begin my adventure in a cursed medieval kingdom. I am a lone traveler who has just arrived at the gates of a once-great city, now shrouded in darkness. Set the scene dramatically."
    },
    {
        "title": "🚀 Stranded on Kepler-9",
        "desc": "Sci-fi survival on an alien planet with unknown life forms.",
        "prompt": "Begin my adventure on an alien planet. I am the sole survivor of a crashed spaceship on Kepler-9, an uncharted world. Set the scene with an eerie, mysterious atmosphere."
    },
    {
        "title": "🗺️ The Lost Temple",
        "desc": "An archaeologist hunts for a legendary artifact deep in the jungle.",
        "prompt": "Begin my adventure as an archaeologist deep in the Amazon jungle. I've just discovered the entrance to a lost temple that hasn't been seen in 500 years. Set the scene with mystery and danger."
    },
    {
        "title": "🧙 The Magic Academy",
        "desc": "A young mage uncovers a dark conspiracy at a school of magic.",
        "prompt": "Begin my adventure at a prestigious magic academy. I am a new student who has just discovered a secret door in the library that shouldn't exist. Set the scene with intrigue and wonder."
    },
    {
        "title": "🏴‍☠️ Pirates of the Shattered Sea",
        "desc": "Sail treacherous waters, hunt treasure, and outsmart rival pirates.",
        "prompt": "Begin my adventure as a pirate captain on the Shattered Sea. My crew has just spotted a ghost ship drifting without sails toward us. Set the scene with tension and mystery."
    },
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_dm_response(history: list, new_message: str) -> str:
    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    contents.append({"role": "user", "parts": [{"text": new_message}]})

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=contents,
        config={"system_instruction": DM_SYSTEM_PROMPT}
    )
    return response.text
    
    # Build Gemini chat history format
    gemini_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({
            "role": role,
            "parts": [msg["content"]]
        })

    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(new_message)
    return response.text


def init_session():
    defaults = {
        "stage": "setup",
        "messages": [],
        "game_started": False,
        "turn_count": 0,
        "scenario_title": ""
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── UI ─────────────────────────────────────────────────────────────────────────
init_session()

st.markdown("""
<div class='hero'>
    <h1>⚔️ AI Dungeon Master</h1>
    <p>Your choices shape the story. Every decision echoes through the realm.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Scenario selection ─────────────────────────────────────────────────────────
if not st.session_state.game_started:
    st.markdown("### 🗺️ Choose Your Adventure")
    st.caption("Pick a world to begin your journey — or write your own.")

    for scenario in SCENARIOS:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class='scenario-card'>
                <div class='scenario-title'>{scenario['title']}</div>
                <div class='scenario-desc'>{scenario['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write("")
            st.write("")
            if st.button("Begin", key=scenario['title']):
                st.session_state.scenario_title = scenario['title']
                with st.spinner("The Dungeon Master prepares your world... 🎲"):
                    opening = get_dm_response([], scenario['prompt'])
                st.session_state.messages = [
                    {"role": "user", "content": scenario['prompt']},
                    {"role": "assistant", "content": opening}
                ]
                st.session_state.game_started = True
                st.session_state.turn_count = 1
                st.rerun()

    st.markdown("---")
    st.markdown("### ✍️ Or write your own scenario")
    custom = st.text_area("Describe your world...", placeholder="e.g. I am a detective in 1920s Chicago who has just found a mysterious letter...", height=100)
    if st.button("Begin Custom Adventure →", type="primary"):
        if custom.strip():
            st.session_state.scenario_title = "Custom Adventure"
            with st.spinner("The Dungeon Master prepares your world... 🎲"):
                opening = get_dm_response([], f"Begin my adventure: {custom}. Set the scene dramatically and immersively.")
            st.session_state.messages = [
                {"role": "user", "content": custom},
                {"role": "assistant", "content": opening}
            ]
            st.session_state.game_started = True
            st.session_state.turn_count = 1
            st.rerun()
        else:
            st.warning("Please describe your scenario first.")

# ── Active game ────────────────────────────────────────────────────────────────
else:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='stat-bar'>
            <div class='stat-value'>{st.session_state.scenario_title.split()[0] if st.session_state.scenario_title else "⚔️"}</div>
            <div class='stat-label'>Adventure</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='stat-bar'>
            <div class='stat-value'>{st.session_state.turn_count}</div>
            <div class='stat-label'>Turns Played</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        if st.button("🔄 New Adventure", use_container_width=True):
            for key in ["messages", "game_started", "turn_count", "scenario_title"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.markdown("---")

    # Chat history
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown("<div class='dm-label'>🎲 Dungeon Master</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='dm-message'>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "user" and msg != st.session_state.messages[0]:
            st.markdown("<div class='player-label'>⚔️ You</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='player-message'>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### ⚔️ Your Action")
    player_input = st.text_area(
        "",
        placeholder="What do you do? Type your action or choice...",
        height=80,
        label_visibility="collapsed",
        key=f"input_{st.session_state.turn_count}"
    )

    if st.button("Take Action →", type="primary", use_container_width=True):
        if player_input.strip():
            # Build history excluding the opening prompt
            history = st.session_state.messages[:-1] if len(st.session_state.messages) > 1 else []

            with st.spinner("The story unfolds... 🎲"):
                dm_response = get_dm_response(
                    history,
                    player_input
                )

            st.session_state.messages.append({"role": "user", "content": player_input})
            st.session_state.messages.append({"role": "assistant", "content": dm_response})
            st.session_state.turn_count += 1
            st.rerun()
        else:
            st.warning("Type an action to continue the story!")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#333; font-size:0.8rem'>Built with Python · Google Gemini · Streamlit</p>", unsafe_allow_html=True)
