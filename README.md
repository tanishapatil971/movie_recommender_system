# 🎬 Movie Recommender System

A content-based movie recommender system built using **Machine Learning** and deployed as a **Streamlit web application**.  
The system recommends similar movies based on user selection and displays movie posters using the **TMDB API**.

---

## 📌 Project Overview

This project demonstrates an end-to-end workflow of building a recommendation system:
- Data preprocessing and model training using Machine Learning
- Similarity-based recommendations using cosine similarity
- Model persistence using Pickle
- Web-based interaction using Streamlit

The Machine Learning model is developed in **Google Colab**, while the web application is built and run locally using **PyCharm**.

---

## 🧠 Recommendation Approach

- Content-based filtering technique
- Movie similarity calculated using **cosine similarity**
- Given a selected movie, the system recommends the **top 5 similar movies**
- Movie posters are fetched dynamically using the **TMDB API**

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Machine Learning:** Pandas, NumPy, Scikit-learn  
- **Web Framework:** Streamlit  
- **API Integration:** TMDB API  
- **Development Tools:** Google Colab, PyCharm  
- **Version Control:** Git & GitHub  

---

## 📁 Project Structure
movie_recommender_system/
│
├── datasets/
│ ├── tmdb_5000_movies.csv
│ └── tmdb_5000_credits.csv
│
├── ml_model/
│ └── movie_recommender_system.ipynb
│
├── screenshots/
│ ├── home.jpg
│ └── recommendation.jpg
│
├── web_app/
│ ├── app.py
│ ├── requirements.txt
│ └── .env.example
│
└── README.md
