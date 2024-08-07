import pandas as pd
import streamlit as st
import pickle

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

movies=pickle.load(open('movies_list.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies_list=movies['title'].values
mov=pd.read_csv('moviedataset.csv')
st.header('Movie Recommender System')
selectvalue=st.selectbox('Select Movie from dropdown',movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    for i in distance[1:6]:
        movie_info = movies.iloc[i[0]]
        title = mov.iloc[i[0]]['title']
        genre = mov.iloc[i[0]]['genre']
        release_date=mov.iloc[i[0]]['release_date']
        vote_average=mov.iloc[i[0]]['vote_average']
        recommend_movie.append((title, genre,release_date,vote_average))
    return recommend_movie

if st.button("Show Recommend"):
    movie_recommendations = recommend(selectvalue)
    if movie_recommendations:
        for idx, (title, genre,release_date,vote_average) in enumerate(movie_recommendations):
            st.write(f"{idx + 1}. {title} - Genre: {genre} - Release Date: {release_date} - Vote Average: {vote_average} ")
