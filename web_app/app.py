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
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>

/* Hide Streamlit UI */
#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

/* App background */

.stApp{
background:#0E1117;
}

/* Main title */

.main-title{
font-size:48px;
font-weight:800;
text-align:center;
color:white;
margin-top:20px;
letter-spacing:1px;
}

/* Subtitle */

.subtitle{
font-size:18px;
text-align:center;
color:#B3B3B3;
margin-bottom:25px;
}

/* Movie card */

.movie-card{
background:#1A1A1A;
padding:10px;
border-radius:15px;
box-shadow:0px 5px 15px rgba(0,0,0,.5);
transition:0.3s;
}

.movie-card:hover{
transform:scale(1.04);
}

.movie-title{
font-size:17px;
font-weight:700;
text-align:center;
margin-top:10px;
color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_title):

    try:
        url = "https://api.themoviedb.org/3/search/movie"

        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        if not data.get("results"):
            return None

        movie = data["results"][0]

        poster = None

        if movie.get("poster_path"):
            poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"

        return {
            "title": movie.get("title"),
            "poster": poster,
            "rating": movie.get("vote_average"),
            "year": movie.get("release_date","")[:4],
            "overview": movie.get("overview"),
            "id": movie.get("id")
        }

    except Exception:
        return None


def recommend(movie):

    index = movies[movies["title"] == movie].index[0]

    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    recommendations=[]

    for i in movie_list:

        title = movies.iloc[i[0]].title

        details = fetch_movie_details(title)

        if details:
            recommendations.append(details)

    return recommendations

# ---------------- DATA ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pd.DataFrame(
    pickle.load(
        open(
            os.path.join(BASE_DIR, "movie_dict.pkl"),
            "rb"
        )
    )
)

similarity = pickle.load(
    open(
        os.path.join(BASE_DIR, "similarity.pkl"),
        "rb"
    )
)

# ---------------- UI ----------------

st.markdown("""
<div style="
background:linear-gradient(135deg,#1B1B1B,#0E1117);
padding:45px;
border-radius:20px;
text-align:center;
margin-bottom:30px;
box-shadow:0px 8px 25px rgba(0,0,0,.45);
">

<h1 style="
color:white;
font-size:52px;
margin-bottom:10px;
font-weight:800;
">
🎬 Movie Recommendation System
</h1>

<p style="
color:#CFCFCF;
font-size:19px;
margin-bottom:20px;
">
Discover movies you'll love using Artificial Intelligence
</p>

<div style="
display:inline-block;
background:#262730;
padding:10px 22px;
border-radius:30px;
color:#E8E8E8;
font-size:16px;
">
✨ Content-Based Recommendation Engine • TMDB API • Machine Learning
</div>

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎥 Movies", f"{len(movies):,}")

with col2:
    st.metric("🤖 Model", "Cosine Similarity")

with col3:
    st.metric("🌐 API", "TMDB")

st.write("")

st.markdown("## 🍿 Find Your Favorite Movie")

st.caption(
    "Choose a movie you already enjoy and discover five similar recommendations."
)

selected_movie = st.selectbox(
    "🍿 Search Movie",
    movies["title"].values,
    index=None,
    placeholder="Start typing a movie..."
)

st.write("")

if st.button("✨ Discover Similar Movies", use_container_width=True):

    if not selected_movie:
        st.warning("Please select a movie first.")
        st.stop()

    with st.spinner("Finding movies you'll love... 🍿"):

        recommendations = recommend(selected_movie)

    st.markdown("## Recommended For You")

    cols = st.columns(5)

    for idx, movie in enumerate(recommendations):

        with cols[idx]:

            st.markdown("<div class='movie-card'>", unsafe_allow_html=True)

            if movie["poster"]:

                try:
                    img = requests.get(movie["poster"], timeout=10)

                    st.image(
                        img.content,
                        use_container_width=True
                    )

                except:

                    st.image(
                        "https://placehold.co/300x450/png?text=No+Poster",
                        use_container_width=True
                    )

            st.markdown(
                f"<div class='movie-title'>{movie['title']}</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"⭐ **{movie['rating']:.1f}**"
            )

            st.caption(movie["year"])

            st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.divider()

st.caption(
    "Built with ❤️ using Python • Streamlit • Scikit-learn • TMDB API"
)
