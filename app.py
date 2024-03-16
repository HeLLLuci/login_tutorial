from flask import Flask, session, render_template, request, redirect
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Firebase configuration
firebaseConfig = {
    'apiKey': "AIzaSyBoITORNGRFvc_vAu0K-FLpIHU8XMxVSFk",
    'authDomain': "python-tutorial-4ad96.firebaseapp.com",
    'databaseURL': "https://python-tutorial-4ad96-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "python-tutorial-4ad96",
    'storageBucket': "python-tutorial-4ad96.appspot.com",
    'messagingSenderId': "585196497723",
    'appId': "1:585196497723:web:a9c7642128f8ac1be2a51e",
    'measurementId': "G-YE3E10XG7C"
}

# Initialize Firebase app
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Initialize Firestore database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Secret key for Flask session
app.secret_key = 'secret'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Sign in the user
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']  # Store user token in session
            # Check if the user is an admin
            user_ref = db.collection('userDetails').document(user['localId'])
            user_data = user_ref.get().to_dict()
            if user_data and user_data.get('isAdmin', False):
                return redirect('/welcome.html')
            else:
                return redirect('/Allocationrequest.html')  # Redirect non-admin users to Allocationrequest.html
        except Exception as e:
            return f'Failed to login. Error: {str(e)}'
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/Allocationrequest.html')
def allocationRequest():
    return render_template('Allocationrequest.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        employee_name = request.form.get('employee_name')
        circle_name = request.form.get('circle_name')
        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_ref = db.collection('userDetails').document(user['localId'])
            user_ref.set({
                'email': email,
                'employee_name': employee_name,
                'circle_name': circle_name,
                'isAdmin': False
            })
            return redirect('/')
        except Exception as e:
            return f'Failed to signup. Error: {str(e)}'
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)
