import pickle
import streamlit as st
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tunely · Music Recommender",
    page_icon="🎵",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0a0a0f;
    --surface:   #13131a;
    --card:      #1c1c28;
    --accent:    #e8ff47;
    --accent2:   #ff6b6b;
    --text:      #f0f0f0;
    --muted:     #6b6b80;
    --border:    rgba(255,255,255,0.07);
}

/* ── Global resets ── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background: var(--bg) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1200px !important; }

/* ── Hero title ── */
.hero {
    text-align: center;
    padding: 3rem 0 1rem;
}
.hero h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(4rem, 10vw, 8rem) !important;
    letter-spacing: 0.05em;
    color: var(--accent) !important;
    line-height: 0.9;
    margin: 0;
}
.hero p {
    color: var(--muted);
    font-size: 1rem;
    margin-top: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── Search bar wrapper ── */
.search-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 2rem auto;
    max-width: 700px;
}

/* ── Streamlit selectbox overrides ── */
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stSelectbox label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}

/* ── Button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.2rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.6rem 2.5rem !important;
    width: 100% !important;
    margin-top: 0.75rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(232,255,71,0.25) !important;
}

/* ── Section label ── */
.section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--muted);
    margin: 2.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Song card ── */
.song-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    height: 100%;
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
.song-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0;
    transition: opacity 0.2s;
}
.song-card:hover { border-color: rgba(232,255,71,0.3); transform: translateY(-4px); }
.song-card:hover::before { opacity: 1; }

.card-rank {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    color: var(--border);
    line-height: 1;
    margin-bottom: 0.5rem;
}
.card-art {
    width: 100%;
    aspect-ratio: 1;
    border-radius: 8px;
    margin-bottom: 0.75rem;
    object-fit: cover;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}
.card-title {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1.3;
    margin-bottom: 0.25rem;
}
.card-artist {
    font-size: 0.8rem;
    color: var(--muted);
}
.card-badge {
    display: inline-block;
    background: rgba(232,255,71,0.1);
    color: var(--accent);
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    margin-top: 0.5rem;
}

/* ── Now playing bar ── */
.now-playing {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.np-dot {
    width: 10px; height: 10px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}
.np-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.15em; color: var(--muted); }
.np-song  { font-weight: 500; font-size: 0.95rem; }

/* ── Stats bar ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.78rem;
    color: var(--muted);
}
.stat-pill span { color: var(--accent); font-weight: 600; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_data():
    music = pickle.load(open('df.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return music, similarity

music, similarity = load_data()

# ── Emoji art placeholders (one per genre feel) ───────────────────────────────
EMOJIS = ["🎸", "🎹", "🎷", "🥁", "🎻", "🎺", "🎤", "🎧", "🪗", "🪘"]

def get_emoji(song_name):
    return EMOJIS[hash(song_name) % len(EMOJIS)]

def get_bg_color(song_name):
    colors = [
        "#1a1a2e", "#16213e", "#1e1b2e", "#0f3460",
        "#1a0a2e", "#2e1a0a", "#0a2e1a", "#2e0a1a",
    ]
    return colors[hash(song_name) % len(colors)]


# ── Recommendation logic ───────────────────────────────────────────────────────
def recommend(song, n=5):
    matches = music[music['song'] == song]
    if matches.empty:
        return [], []

    idx = matches.index[0]
    scores = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)[1:n+1]

    names, artists = [], []
    for i, _ in scores:
        row = music.iloc[i]
        names.append(row['song'])
        artists.append(row.get('artist', 'Unknown Artist'))

    return names, artists


# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>TUNELY</h1>
  <p>✦ AI-powered music recommendations ✦</p>
</div>
""", unsafe_allow_html=True)

# Stats bar
total_songs = len(music)
total_artists = music['artist'].nunique() if 'artist' in music.columns else "—"
st.markdown(f"""
<div class="stats-row">
  <div class="stat-pill"><span>{total_songs:,}</span> songs indexed</div>
  <div class="stat-pill"><span>{total_artists:,}</span> artists</div>
  <div class="stat-pill">Powered by <span>TF-IDF</span> + Cosine Similarity</div>
</div>
""", unsafe_allow_html=True)

# Search section
st.markdown('<div class="search-wrap">', unsafe_allow_html=True)

song_list = music['song'].values
selected_song = st.selectbox("🎵 Choose a song you like", song_list)

num_recs = st.slider("How many recommendations?", min_value=3, max_value=10, value=5)

clicked = st.button("Find Similar Songs →")
st.markdown('</div>', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────
if clicked:
    with st.spinner("Finding your next favourite tracks..."):
        names, artists = recommend(selected_song, n=num_recs)

    if not names:
        st.error(f"Could not find '{selected_song}' in the dataset. Try another song.")
    else:
        # Now playing
        sel_artist = music[music['song'] == selected_song].iloc[0].get('artist', 'Unknown')
        st.markdown(f"""
        <div class="now-playing">
          <div class="np-dot"></div>
          <div>
            <div class="np-label">Based on your selection</div>
            <div class="np-song">{selected_song} — {sel_artist}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="section-label">✦ {len(names)} recommendations for you</div>', unsafe_allow_html=True)

        cols = st.columns(min(num_recs, 5))
        for i, (name, artist) in enumerate(zip(names, artists)):
            col = cols[i % len(cols)]
            emoji = get_emoji(name)
            bg = get_bg_color(name)
            with col:
                st.markdown(f"""
                <div class="song-card">
                  <div class="card-rank">0{i+1}</div>
                  <div class="card-art" style="background:{bg}; font-size:3rem; text-align:center; line-height:1; padding:1.5rem 0;">
                    {emoji}
                  </div>
                  <div class="card-title">{name}</div>
                  <div class="card-artist">{artist}</div>
                  <div class="card-badge">Similar match</div>
                </div>
                """, unsafe_allow_html=True)

        # Shuffle tip
        st.markdown("""
        <p style='text-align:center; color:#6b6b80; font-size:0.8rem; margin-top:2rem;'>
          💡 Tip — select a different song and hit recommend again to explore more
        </p>
        """, unsafe_allow_html=True)
