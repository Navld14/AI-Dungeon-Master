# ⚔️ AI Dungeon Master

A text-based RPG where Google Gemini AI acts as your Dungeon Master — creating immersive stories, reacting to your choices, and building a dynamic narrative that remembers everything.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Gemini](https://img.shields.io/badge/Google-Gemini_API-4285F4?style=flat-square&logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

🌐 **Live Demo:** [Try it here](https://ai-dungeon-master-00.streamlit.app/)

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
| Google Gemini API | AI Dungeon Master brain (free tier) |
| Streamlit | Web app + session state management |

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/Navld14/AI-Dungeon-Master.git
cd AI-Dungeon-Master
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Gemini API key
- Go to [aistudio.google.com](https://aistudio.google.com)
- Click **Get API Key → Create API key**
- It's completely free

### 4. Set your API key
```bash
export GEMINI_API_KEY="AIzaSy..."
```

### 5. Run the app
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
Gemini API generates opening scene
        ↓
Full conversation history sent with every turn
        ↓
Gemini responds as DM — describes scene + offers choices
        ↓
Player types action → cycle repeats
```

---

## 📁 Project Structure

```
AI-Dungeon-Master/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🙋 Author

**Naveen Ladha**
[GitHub](https://github.com/Navld14)

---

## 📄 License

MIT License — free to use and modify.
