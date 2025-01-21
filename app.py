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

@app.route('/profile')
def userProfile():
    if isLoggedIn:
        if UserType == "guest":
            return render_template('profile_guest.html')
        elif UserType == "organizer":
            return render_template('profile_organizer.html')
    else:
        return 'NOT LOGGED IN'

if __name__ == '__main__':
    app.run(debug=True)