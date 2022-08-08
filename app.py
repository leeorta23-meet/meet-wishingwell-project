from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import datetime

firebaseConfig = {
  "apiKey": "AIzaSyAWGgb_KfjpqN_TBmPyKDpt-1gboxxB0tk",
  "authDomain": "wishingwell-12696.firebaseapp.com",
  "projectId": "wishingwell-12696",
  "storageBucket": "wishingwell-12696.appspot.com",
  "messagingSenderId": "1084222567056",
  "appId": "1:1084222567056:web:6d53fc78ca3501bd8c5e15",
  "measurementId": "G-BDP9HD9G7D",
  "databaseURL": "https://wishingwell-12696-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def index():
    print('yes')
    if request.method == 'POST':
       name = request.form['name']
       email = request.form['email']
       extra = request.form['extra']

       try:
           user = {"name": name, "email" : email, 'extra':extra}
           print(user)
           db.child("Users").push(user)
           return redirect(url_for('petition'))
       except:
           print("Authentication failed")
    return render_template("index.html")

@app.route('/chat')
def petition():
    users = db.child("Users").get().val()
    my_user = []
    name = []
    email = []
    extra = []
    n = 0
    if users is not None:
      for user in users:
          name.append(users[user]['name'])
          email.append(users[user]['email'])
          extra.append(users[user]['extra'])
          my_user.append(users[user])

    return render_template('chat.html', name = name, email = email, extra = extra, users = my_user, n = n)

if __name__ == '__main__':
    app.run(debug=True)