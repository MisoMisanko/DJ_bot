# 🎧 DJ Bot – Your Mood-Based Music Companion

DJ Bot is a conversational Spotify recommender that dynamically responds to your **mood** and **activity** to generate the perfect playlist. It uses sentiment analysis and emotion detection to assess your input, then queries the Spotify API for context-aware suggestions. You can also unlock a one-time “special” playlist curated just for you.  

You can interact with DJ Bot via a terminal interface (`run_chatbot.py`) or a fully styled **Streamlit web app**.

---

## 🚀 Features
- 🌡️ Sentiment detection using TextBlob  
- 🎭 Emotion recognition (happy, sad, excited, calm, angry, stressed, etc.)  
- 🧠 Activity-based playlist matching  
- ✨ One-time “special” Spotify playlist  
- 🧵 Multi-step mood logic with fallback handling  
- 💬 Conversational prompts with emoji-enhanced personality  
- 🎨 Custom styled web app matching personal portfolio  

---

## 🖥️ How to Run

### Option 1 – Web App (Streamlit)
1. Ensure you have Python 3.10+ and all dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Save your Spotify API credentials as environment variables:
   ```bash
   export SPOTIPY_CLIENT_ID="your_client_id"
   export SPOTIPY_CLIENT_SECRET="your_client_secret"
   ```

3. Run the web app:
   ```bash
   streamlit run dj_bot_app.py
   ```

4. Chat with DJ Bot in the browser and receive Spotify playlists based on your mood and context.

---

### Option 2 – Terminal Chat (Command Line Interface)
1. Activate your virtual environment (e.g. conda):
   ```bash
   conda activate nlp
   ```

2. Run the script with your Spotify credentials:
   ```bash
   python run_chatbot.py <client_id> <client_secret>
   ```

3. Type freely! DJ Bot will analyze your mood and activity and respond with matching playlists.

---

## 💡 How It Works
- **Mood Parsing:** TextBlob analyzes your input’s polarity. Keywords are matched to specific emotions.
- **Contextual Search:** DJ Bot combines the detected emotion and your described activity into a Spotify query.
- **Resilience:** If Spotify doesn’t return results, fallback playlists ensure continuity.
- **Special Mode:** DJ Bot will upsell a one-time “special” playlist experience.
- **Terminal vs Streamlit:** Both interfaces share the same logic but differ in delivery style and UI/UX.

---

## 🛠 Files Overview
| File                | Purpose                                  |
|---------------------|-------------------------------------------|
| `dj_bot.py`         | Core class handling logic and Spotify API |
| `dj_bot_app.py`     | Streamlit web interface                   |
| `run_chatbot.py`    | Terminal chatbot                          |
| `assets/styles.css` | Custom CSS for the web app styling        |
| `requirements.txt`  | Python dependencies                       |

---

## 🧪 Example Prompts
> “I’m feeling excited today!”  
> “Pretty sad actually.”  
> “Calm and focused – I’m studying.”  
> “Just got dumped 💔”  

---

## 🔐 Notes on Credentials
You will need valid Spotify API credentials to run DJ Bot.  
A working `.env` file or exported credentials (or via Streamlit secrets) must be used.

> *If you are reviewing the project for assessment, my credentials are included in the submitted zip archive.*

✅ You can also test the chatbot live on my portfolio:  
[https://www.misomisanko.com](https://www.misomisanko.com)

ENJOY :)
---

## ✅ Final Touches
- Some UI elements are custom styled using `styles.css`
- Streamlit layout is compact and mobile-friendly
- Includes emoji-enhanced dialogue and playlist logic for engagement