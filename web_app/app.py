import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# ---------------- CONFIG ----------------
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- FUNCTIONS ----------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_title):
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("results") and data["results"][0].get("poster_path"):
            return f"https://image.tmdb.org/t/p/w500{data['results'][0]['poster_path']}"
    except:
        pass

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
        names.append(title)
        posters.append(fetch_poster(title))

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
                st.image(posters[i])
                st.markdown(f"**{names[i]}**")
