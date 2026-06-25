import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# ---------------- CONFIG ----------------
load_dotenv()  # keeps local development working

try:
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]   # Streamlit Cloud
except Exception:
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")    # Local .env
    
st.write("TMDB Key Loaded:", TMDB_API_KEY is not None)
st.write("TMDB Key Prefix:", TMDB_API_KEY[:5] if TMDB_API_KEY else "None")

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- FUNCTIONS ----------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }

    response = requests.get(url, params=params, timeout=10)

    st.write("Movie:", movie_title)
    st.write("Status Code:", response.status_code)
    st.write("Response:", response.json())

    data = response.json()

    if response.status_code == 200 and data.get("results"):
        poster_path = data["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    names, posters = [], []

    for i in movie_list:
        title = movies.iloc[i[0]]['title']

        poster = fetch_poster(title)

        st.write("Movie:", title)
        st.write("Poster URL:", poster)

        names.append(title)
        posters.append(poster)

    return names, posters

# ---------------- DATA ----------------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pd.DataFrame(
    pickle.load(open(os.path.join(BASE_DIR, "movie_dict.pkl"), "rb"))
)

similarity = pickle.load(
    open(os.path.join(BASE_DIR, "similarity.pkl"), "rb")
)

# ---------------- UI ----------------
st.title("🎬 Movie Recommender System")

st.caption(
    "A content-based movie recommendation system using cosine similarity "
    "and TMDB API for poster visualization."
)

st.markdown("---")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values,
    index=None,
    placeholder="Type or select a movie"
)

if st.button("Recommend"):
    if not selected_movie:
        st.warning("Please select a movie.")
    else:
        with st.spinner("Generating recommendations..."):
            names, posters = recommend(selected_movie)

        st.markdown("### Recommended Movies")

        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(
    posters[i],
    caption=names[i],
    use_container_width=True,
    output_format="PNG"
)
                st.markdown(f"**{names[i]}**")
