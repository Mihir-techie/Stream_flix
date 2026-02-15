# Movie_Recommend

A modern movie recommendation platform with user authentication and rating system, built with Flask and styled with a Jio Hotstar-inspired theme.

## Features

- 🔐 User authentication (Login/Signup)
- ⭐ Movie rating system with descriptions
- 🎬 Movie recommendations using ML algorithms
- 🎨 Modern Jio Hotstar-inspired UI
- 📱 Responsive design
- 💾 SQLite database for user data and ratings
- 🚀 **Direct deployment ready** - Works without external model files

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Scikit-learn, Pandas
- **API**: OMDb API for movie posters

## Quick Start & Deployment

### Option 1: Deploy Directly to Render (Recommended)
1. Clone this repository
2. Connect to Render.com
3. Deploy - Works immediately with built-in movie dataset!

### Option 2: Local Development
1. Clone repository
```bash
git clone https://github.com/Mihir-techie/Movie_Recommend.git
cd Movie_Recommend
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python app.py
```

## How It Works

The app automatically detects if model files are available:
- **With Model Files**: Uses full movie dataset with advanced recommendations
- **Without Model Files**: Falls back to built-in dataset with 30 popular movies

## Usage

1. Sign up for a new account
2. Login to access the movie recommendation system
3. Search for movies to get recommendations
4. Rate movies and leave reviews
5. View other users' ratings

## Deployment on Render

**Ready for immediate deployment!**

1. Push this code to your GitHub repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Render will automatically detect `render.yaml` file
5. Deploy - No additional setup required!

The app will automatically:
- Create SQLite database on first run
- Handle user sessions and authentication
- Use built-in movie dataset if model files are missing
- Serve the web application

## Project Structure

```
Movie_Recommend/
├── app.py                 # Main Flask application with fallback system
├── database.py           # Database models and functions
├── requirements.txt      # Python dependencies
├── render.yaml          # Render deployment configuration
├── templates/
│   ├── index.html        # Main page with movie recommendations
│   ├── login.html        # User login page
│   ├── signup.html       # User registration page
│   └── movie_ratings.html # Movie ratings display
├── models/              # Model files (optional - app works without them)
│   ├── movies (1).pkl    # Movie dataset (optional)
│   └── similarity.pkl    # Similarity matrix (optional)
└── README.md
```

## Advanced Setup (Optional)

If you want to use the full movie dataset:
1. Download the original model files
2. Place them in `models/` directory:
   - `movies (1).pkl` - Movie dataset
   - `similarity.pkl` - Similarity matrix
3. Restart the app

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
