from flask import Flask, redirect, request, session, render_template

import requests
import base64
import urllib

# Add client ID (from Spotify Developer Dashboard)
CLIENT_ID = "9dde2b6fe56a49129cc39fc86caf91d6"

# Add client Secret (from Spotify Developer Dashboard)
CLIENT_SECRET = "1dee944b3dcb45db925d43c90ad01f99"

# Add the redirect URI (from Spotify Developer Dashboard)
REDIRECT_URI = "http://localhost:5000/callback"

# Scopes
SCOPE = 'user-library-read'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-secret-key'  # Replace with your secret key

@app.route('/')
def index():
    if 'access_token' in session:
        return '''You are logged in! <br> 
                  <a href="/logout">Click here to log out</a>'''
    else:
        return render_template('login.html')  # render login.html template

@app.route('/login')
def login():
    auth_url = 'https://accounts.spotify.com/authorize'

    query_params = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "client_id": CLIENT_ID
    }

    request_url = f"{auth_url}?{urllib.parse.urlencode(query_params)}"
    return redirect(request_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    auth_token_url = "https://accounts.spotify.com/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    res_body = res.json()
    session['access_token'] = res_body.get('access_token')
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
