import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# ---------------- CONFIG ----------------
load_dotenv()

try:
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
except Exception:
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pd.DataFrame(
    pickle.load(open(os.path.join(BASE_DIR, "movie_dict.pkl"), "rb"))
)

similarity = pickle.load(
    open(os.path.join(BASE_DIR, "similarity.pkl"), "rb")
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

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get("results"):
                poster_path = data["results"][0].get("poster_path")

                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception:
        pass

    return None


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movie_list:
        movie_title = movies.iloc[i[0]].title

        names.append(movie_title)
        posters.append(fetch_poster(movie_title))

    return names, posters


# ---------------- UI ----------------
st.title("🎬 Movie Recommender System")

st.caption(
    "A content-based movie recommendation system using cosine similarity and TMDB API."
)

st.divider()

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):

    with st.spinner("Finding similar movies..."):

        names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            if posters[i]:

                try:
                    image = requests.get(posters[i], timeout=10)

                    st.image(
                        image.content,
                        use_container_width=True
                    )

                except Exception:
                    st.warning("Poster unavailable")

            else:
                st.warning("Poster unavailable")

            st.markdown(
                f"**{names[i]}**"
            )
