# ⚔️ AI Dungeon Master

A text-based RPG where Claude AI acts as your Dungeon Master — creating immersive stories, reacting to your choices, and building a dynamic narrative that remembers everything.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Claude](https://img.shields.io/badge/Claude-API-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎯 What It Does

- 🗺️ **5 pre-built adventure scenarios** — fantasy, sci-fi, mystery, magic academy, pirates
- ✍️ **Custom scenario creator** — describe any world and start playing
- 🧠 **Full conversation memory** — the DM remembers your entire story
- 🎲 **Dynamic storytelling** — choices have real consequences, plot twists, NPCs
- ⚔️ **Suggests actions** — 3-4 choices offered after each scene
- 🔄 **Restart anytime** — begin a new adventure with one click

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Claude API (Anthropic) | AI Dungeon Master brain |
| Streamlit | Web app + session state management |

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/Navld14/ai-dungeon-master.git
cd ai-dungeon-master
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
cp .env.example .env
# Add your Anthropic API key to .env
export ANTHROPIC_API_KEY=your_key_here
```

Get your free API key at [console.anthropic.com](https://console.anthropic.com)

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🗺️ Available Scenarios

| Scenario | Setting |
|----------|---------|
| ⚔️ The Cursed Kingdom | Dark fantasy medieval world |
| 🚀 Stranded on Kepler-9 | Alien planet survival sci-fi |
| 🗺️ The Lost Temple | Jungle archaeology adventure |
| 🧙 The Magic Academy | School of magic mystery |
| 🏴‍☠️ Pirates of the Shattered Sea | High seas pirate adventure |

---

## 💡 How It Works

```
Player chooses scenario
        ↓
Claude API generates opening scene (system prompt = DM instructions)
        ↓
Full conversation history sent with every turn
        ↓
Claude responds as DM — describes scene + offers choices
        ↓
Player types action → cycle repeats
```

The key insight: sending the **full conversation history** with every API call gives Claude complete story memory, enabling coherent, stateful narratives without any database.

---

## 📁 Project Structure

```
ai-dungeon-master/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore
└── README.md
```

---

## 🙋 Author

**Naveen Ladha**
[GitHub](https://github.com/Navld14)

---

## 📄 License

MIT License — free to use and modify.
