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
background:linear-gradient(rgba(10,10,10,.82),rgba(10,10,10,.82)),
url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1600');
background-size:cover;
background-position:center;
padding:70px;
border-radius:25px;
text-align:center;
margin-bottom:35px;
">

<h1 style="
font-size:60px;
font-weight:900;
color:white;
margin-bottom:15px;
">

🎬 Movie Recommendation System

</h1>

<p style="
font-size:22px;
color:#D1D5DB;
">

Find your next favorite movie using Artificial Intelligence

</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:#1B1F27;
padding:25px;
border-radius:18px;
margin-bottom:25px;
box-shadow:0px 8px 30px rgba(0,0,0,.35);
">

<h3 style="color:white;">
🔍 Search Movie
</h3>

<p style="color:#A3A3A3;">
Choose a movie you like and our AI will recommend similar ones.
</p>

</div>
""", unsafe_allow_html=True)

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
