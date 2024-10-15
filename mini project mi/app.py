import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Spotify API Credentials
client_id = 'ea24d1f56f374cc9a56ec56f82f68de9'
client_secret = 'adaca824ad504a4bb336a18922b67259'

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Route to render homepage
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission
@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user inputs from form
    artist_name = request.form.get('artist_name')
    genre = request.form.get('genre')
    
    # Case 1: Artist-based recommendation
    if artist_name:
        results = sp.search(q=f'artist:{artist_name}', type='artist')
        artist_items = results['artists']['items']
        
        if len(artist_items) > 0:
            artist_id = artist_items[0]['id']
            artist_name = artist_items[0]['name']
            
            # Get top tracks from the artist
            tracks = sp.artist_top_tracks(artist_id)['tracks']
            recommended_songs = [(track['name'], track['external_urls']['spotify']) for track in tracks]
            
            return render_template('index.html', songs=recommended_songs, artist=artist_name)
        else:
            return render_template('index.html', error="Artist not found.")

    # Case 2: Genre-based recommendation
    elif genre:
        results = sp.search(q=f'genre:{genre}', type='track', limit=10)
        tracks = results['tracks']['items']
        recommended_songs = [(track['name'], track['external_urls']['spotify']) for track in tracks]
        
        if recommended_songs:
            return render_template('index.html', songs=recommended_songs, genre=genre)
        else:
            return render_template('index.html', error="No songs found for this genre.")
    
    return render_template('index.html', error="Please enter an artist name or genre.")

if __name__ == "__main__":
    app.run(debug=True)
