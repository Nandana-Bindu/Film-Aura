
import streamlit as st
import random
import os


DATA_DIR = "data"
REQUIRED_FILES = ["english.txt", "hindi.txt", "malayalam.txt", "tamil.txt", "trending.txt"]


missing_files = [f for f in REQUIRED_FILES if not os.path.exists(os.path.join(DATA_DIR, f))]
if missing_files:
    st.error(f"⚠️ Missing TXT files in '{DATA_DIR}/': {', '.join(missing_files)}")
    st.stop()


def load_movies(language):
    path = os.path.join(DATA_DIR, f"{language}.txt")
    movies = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 5:
                title, director, rating, mood, summary = [p.strip() for p in parts]
                movies.append({
                    "title": title,
                    "director": director,
                    "rating": rating,
                    "mood": mood,
                    "summary": summary
                })
    return movies

def load_all_movies():
    all_movies = []
    for lang_file in REQUIRED_FILES[:-1]:
        lang = lang_file.split(".")[0]
        all_movies += load_movies(lang)
    return all_movies


if "history" not in st.session_state:
    st.session_state.history = []
if "seen_titles" not in st.session_state:
    st.session_state.seen_titles = set()

# --- Page Config ---
st.set_page_config(
    page_title="Film Aura 🎬",
    page_icon="🍿",
    layout="wide"
)


st.markdown("""
<style>
/* Animated gradient background - unique dark neon style */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1a2a6c, #b21f1f, #fdbb2d);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
    color: white;
    font-family: 'Trebuchet MS', sans-serif;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Cinematic header */
h1, h2, h3 {
    background: linear-gradient(to right, #ff416c, #ff4b2b, #ffda77, #ff416c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glow 2s ease-in-out infinite alternate;
}
@keyframes elegantFade {
    from { opacity: 0.8; color: #ffffff; }
    to { opacity: 1; color: #f5f5f5; }
}
/* Movie card */
.movie-card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    transition: transform 0.4s, box-shadow 0.4s;
}
.movie-card:hover {
    transform: scale(1.03) rotate(-1deg);
    box-shadow: 0 10px 35px rgba(255,200,150,0.5);
}

/* Popcorn explosion */
.popcorn-burst {
  position: relative;
  display: inline-block;
  font-size: 25px;
  animation: burst 1s ease-out forwards;
}
@keyframes burst {
  0% { transform: scale(0); opacity: 0; }
  40% { transform: scale(1.5) translateY(-50px); opacity: 1; }
  100% { transform: scale(1) translateY(0); opacity: 1; }
}

/* Button styling */
.stButton>button {
    background: linear-gradient(45deg, #ff512f, #dd2476, #24c6dc);
    border: none;
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px 24px;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111;
    color: white;
    border-right: 2px solid #ff416c;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.title("🎬 Film Aura")
mode = st.sidebar.radio(
    "Select Mode:",
    ["Language 📝", "Mood 😃", "Random 🎲", "Trending 🔥", "History 📜"]
)

if st.sidebar.button("🔄 Reset History"):
    st.session_state.history = []
    st.session_state.seen_titles = set()
    st.sidebar.success("History cleared!")


def show_movie(movie):

    popcorns = "".join([f"<span class='popcorn-burst'>🍿</span>" for _ in range(6)])
    st.markdown(f"""
    <div class="movie-card">
        <div style="font-size:28px;">{popcorns}</div>
        <h2>🎬 {movie['title']}</h2>
        <p>🎥 <b>Director:</b> {movie['director']} | ⭐ <b>Rating:</b> {movie['rating']} | 😃 <b>Mood:</b> {movie['mood']}</p>
        <p>{movie['summary']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.history.append(movie)
    st.session_state.seen_titles.add(movie["title"])


if mode == "Language 📝":
    st.header("📝 Language Based Recommendation")
    lang = st.selectbox("Pick a language", ["english", "hindi", "malayalam", "tamil"])
    movies = [m for m in load_movies(lang) if m["title"] not in st.session_state.seen_titles]
    if st.button("Suggest Movie"):
        if movies:
            show_movie(random.choice(movies))
        else:
            st.warning("No new movies left in this language.")

elif mode == "Mood 😃":
    st.header("😃 Mood Based Recommendation")
    moods = ["Comedy", "Thriller", "Romantic", "Action", "Horror", "Drama", "Adventure", "Sci-Fi"]
    mood = st.selectbox("Select mood", moods)
    all_movies = [m for m in load_all_movies() if m["title"] not in st.session_state.seen_titles]
    if st.button("Suggest Movie"):
        results = [m for m in all_movies if mood.lower() in m["mood"].lower()]
        if results:
            show_movie(random.choice(results))
        else:
            st.warning(f"No movies found for mood: {mood}")

elif mode == "Random 🎲":
    st.header("🎲 Random Movie Suggestion")
    all_movies = [m for m in load_all_movies() if m["title"] not in st.session_state.seen_titles]
    if st.button("Suggest Random Movie"):
        if all_movies:
            show_movie(random.choice(all_movies))
        else:
            st.warning("No movies left. Reset to start over.")

elif mode == "Trending 🔥":
    st.header("🔥 Trending Movies")
    trending_movies = [m for m in load_movies("trending") if m["title"] not in st.session_state.seen_titles]
    if st.button("Suggest Trending Movie"):
        if trending_movies:
            show_movie(random.choice(trending_movies))
        else:
            st.warning("No trending movies left.")

elif mode == "History 📜":
    st.header("📜 Previously Recommended Movies")
    if st.session_state.history:
        for movie in st.session_state.history:
            st.markdown(f"<div class='movie-card'><h4>{movie['title']}</h4><p>🎥 {movie['director']} | ⭐ {movie['rating']} | 😃 {movie['mood']}</p></div>", unsafe_allow_html=True)
    else:
        st.info("No history yet. Start discovering movies!")



