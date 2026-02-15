from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import requests
import urllib.parse
import difflib
import pandas as pd
import os
from database import Database

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize database
db = Database()

# Try to load model files, fallback to built-in dataset if not available
movies = None
similarity = None

try:
    movies = pickle.load(open('models/movies (1).pkl', 'rb'))
    similarity = pickle.load(open('models/similarity.pkl', 'rb'))
    print("✅ Model files loaded successfully")
except FileNotFoundError:
    print("⚠️ Model files not found, using fallback dataset")
    # Create a fallback movie dataset
    fallback_movies = [
        "The Dark Knight", "Inception", "Interstellar", "The Matrix", "Pulp Fiction",
        "The Shawshank Redemption", "Forrest Gump", "The Godfather", "Fight Club", "Goodfellas",
        "The Lord of the Rings", "Star Wars", "Avatar", "Titanic", "Gladiator",
        "The Avengers", "Spider-Man", "Iron Man", "Black Panther", "Thor",
        "Joker", "Parasite", "The Social Network", "The Grand Budapest Hotel", "Whiplash",
        "Mad Max: Fury Road", "The Revenant", "Django Unchained", "The Wolf of Wall Street", "Interstellar"
    ]
    
    # Create a simple DataFrame
    movies = pd.DataFrame({
        'title': fallback_movies,
        'genre': ['Action', 'Sci-Fi', 'Sci-Fi', 'Sci-Fi', 'Crime'] * 6
    })
    
    # Create a simple similarity matrix (basic genre-based similarity)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Use titles and genres for similarity
    movies['combined'] = movies['title'] + ' ' + movies['genre']
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(movies['combined'])
    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    print("✅ Fallback dataset created with", len(movies), "movies")

# If movies was saved as dict, convert to DataFrame
if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

OMDB_API_KEY = "5024ab00"


# 🔥 Fetch poster from OMDb
def fetch_poster(movie_title):
    encoded_title = urllib.parse.quote(movie_title)
    url = f"http://www.omdbapi.com/?t={encoded_title}&apikey={OMDB_API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data.get("Poster") and data["Poster"] != "N/A":
        return data["Poster"]
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"


# 🔥 Smart Recommendation Function
def recommend(movie_name):
    movie_list = movies['title'].tolist()

    # Find closest match (fuzzy search)
    closest_match = difflib.get_close_matches(movie_name, movie_list, n=1)

    if not closest_match:
        return [], []

    movie = closest_match[0]
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))


@app.route('/recommend', methods=['POST'])
def recommend_movies():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    movie = request.form.get('movie')
    names, posters = recommend(movie)

    return render_template(
        'index.html',
        names=names,
        posters=posters,
        searched_movie=movie,
        username=session.get('username')
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.authenticate_user(username, password)
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        if db.create_user(username, email, password):
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists', 'error')
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/rate_movie', methods=['POST'])
def rate_movie():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    movie_title = request.form.get('movie_title')
    rating = int(request.form.get('rating'))
    description = request.form.get('description')
    
    if db.add_rating(session['user_id'], movie_title, rating, description):
        flash('Rating added successfully!', 'success')
    else:
        flash('Failed to add rating', 'error')
    
    return redirect(url_for('home'))


@app.route('/movie_ratings/<movie_title>')
def movie_ratings(movie_title):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    ratings = db.get_movie_ratings(movie_title)
    return render_template('movie_ratings.html', ratings=ratings, movie_title=movie_title, username=session.get('username'))


if __name__ == '__main__':
    app.run(debug=True)
