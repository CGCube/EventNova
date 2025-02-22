from flask import Flask, render_template

app = Flask(__name__)

isLoggedIn = True
UserType = "organizer"

@app.route('/')
def index():
    if isLoggedIn:
        return render_template('home_loggedin.html')
    else:
        return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup_select')
def signup_select():
    return render_template('signup_select.html')

@app.route('/signup_guest')
def signup_guest():
    return render_template('signup_guest.html')

@app.route('/signup_organizer')
def signup_organizer():
    return render_template('signup_organizer.html')

@app.route('/shows')
def shows():
    return render_template('shows.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/events')
def events():
    return render_template('events.html')

if isLoggedIn & (UserType == "organizer"):
    @app.route('/add-event')
    def add_event():
        return render_template('add_event.html')
    @app.route('/update-event')
    def edit_event():
        return render_template('update_event.html')
    @app.route('/event-stats')
    def event_stats():
        return render_template('event_stats.html')

@app.route('/profile')
def user_profile():
    if isLoggedIn:
        if UserType == "guest":
            return render_template('profile_guest.html')
        elif UserType == "organizer":
            return render_template('profile_organizer.html')
    else:
        return 'NOT LOGGED IN'

if __name__ == '__main__':
    app.run(debug=True)