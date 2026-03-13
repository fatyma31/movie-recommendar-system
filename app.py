import streamlit as st
import pickle
import pandas as pd
import requests

# -----------------------
# Step 1: Load Pickle Files
# -----------------------
movies = pickle.load(open(r"C:\Users\MS\ml project\movie recommendar system\movie_recommender_system\movie.pkl", 'rb'))
similarity = pickle.load(open(r"C:\Users\MS\ml project\movie recommendar system\movie_recommender_system\similarity.pkl", 'rb'))

movies_list = movies['title'].values

st.title('🎬 Movie Recommender System')
selected_movie = st.selectbox(
    'Select a movie:',
    movies_list
)

# -----------------------
# Step 2: Fetch Poster Function
# -----------------------
def fetch_poster(movie_id):
    api_key = "94fbfc22dc90dbaa9c86cc02af96371a"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# -----------------------
# Step 3: Recommend Function
# -----------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list_sorted = sorted(list(enumerate(distances)),
                                reverse=True,
                                key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list_sorted:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# -----------------------
# Step 4: Show Recommendations in Grid
# -----------------------
if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)  # 5 posters in a row
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], width=150)
            st.caption(names[idx])


