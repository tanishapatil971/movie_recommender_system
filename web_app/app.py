import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# ================= CONFIG =================

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

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:2rem;
padding-bottom:2rem;
max-width:1250px;
}

.stApp{
background:#0E1117;
}

div[data-testid="stMetric"]{
background:#1B1F27;
padding:18px;
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_title):

    try:

        url = "https://api.themoviedb.org/3/search/movie"

        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if not data.get("results"):
            return None

        movie = data["results"][0]

        poster = None

        if movie.get("poster_path"):

            poster = (
                "https://image.tmdb.org/t/p/w500"
                + movie["poster_path"]
            )

        return {

            "title": movie.get("title"),

            "poster": poster,

            "rating": round(
                movie.get("vote_average",0),
                1
            ),

            "year": movie.get(
                "release_date",
                ""
            )[:4],

            "overview": movie.get(
                "overview",
                ""
            )

        }

    except Exception:

        return None


def recommend(movie):

    index = movies[
        movies["title"] == movie
    ].index[0]

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

# ================= DATA =================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

movies = pd.DataFrame(

    pickle.load(

        open(

            os.path.join(
                BASE_DIR,
                "movie_dict.pkl"
            ),

            "rb"

        )

    )

)

similarity = pickle.load(

    open(

        os.path.join(
            BASE_DIR,
            "similarity.pkl"
        ),

        "rb"

    )

)

# ================= UI =================

st.markdown("""
<h1 style="
text-align:center;
font-size:48px;
font-weight:800;
margin-bottom:0;
">
🎬 Movie Recommendation System
</h1>

<p style="
text-align:center;
font-size:18px;
color:#9CA3AF;
margin-bottom:35px;
">
Discover your next favourite movie using AI-powered recommendations.
</p>
""", unsafe_allow_html=True)

left,right=st.columns([2,1])

with left:

    st.markdown("""
    ### 🍿 Find Similar Movies

    Select a movie you already enjoy and let the recommendation engine
    discover similar movies for you.
    """)

    selected_movie=st.selectbox(

        "",

        movies["title"].values,

        index=None,

        placeholder="Search any movie..."

    )

    recommend_btn=st.button(

        "✨ Recommend Movies",

        use_container_width=True

    )

st.divider()

# ================= RECOMMENDATIONS =================

if recommend_btn:

    if not selected_movie:

        st.warning("Please select a movie.")

    else:

        with st.spinner("Finding similar movies... 🍿"):

            recommendations = recommend(selected_movie)

        st.subheader("🎯 Recommended For You")

        cols = st.columns(5)

        for idx, movie in enumerate(recommendations):

            with cols[idx]:

                st.markdown("""
                <style>
                .movie-card{
                    background:#1B1F27;
                    border-radius:18px;
                    padding:12px;
                    transition:.3s;
                    box-shadow:0px 5px 20px rgba(0,0,0,.35);
                    min-height:610px;
                }

                .movie-title{
                    font-size:18px;
                    font-weight:700;
                    color:white;
                    margin-top:12px;
                    margin-bottom:6px;
                }

                .movie-rating{
                    color:#FFD43B;
                    font-size:15px;
                    font-weight:600;
                }

                .movie-year{
                    color:#A1A1AA;
                    font-size:14px;
                    margin-bottom:10px;
                }

                .movie-overview{
                    color:#D4D4D8;
                    font-size:13px;
                    text-align:justify;
                }

                </style>
                """, unsafe_allow_html=True)

                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)

                if movie["poster"]:

                    try:

                        img = requests.get(
                            movie["poster"],
                            timeout=10
                        )

                        st.image(
                            img.content,
                            use_container_width=True
                        )

                    except Exception:

                        st.image(
                            "https://placehold.co/300x450/png?text=No+Poster",
                            use_container_width=True
                        )

                st.markdown(
                    f"<div class='movie-title'>{movie['title']}</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<div class='movie-rating'>⭐ {movie['rating']}</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<div class='movie-year'>{movie['year']}</div>",
                    unsafe_allow_html=True
                )

                overview = movie["overview"]

                if len(overview) > 130:
                    overview = overview[:130] + "..."

                st.markdown(
                    f"<div class='movie-overview'>{overview}</div>",
                    unsafe_allow_html=True
                )

                st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.caption(
    "🎬 Built with Python • Streamlit • Scikit-learn • TMDB API"
)
