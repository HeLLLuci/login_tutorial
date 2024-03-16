import pyrebase

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

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

response = input("Are you existing user? [y/n]")


def login():
    print("Sign In.....")
    email = input("Enter Email : ")
    password = input("Enter Password: ")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        name = auth.get_account_info(user['email'])
        print(name)
    except:
        print("Wrong password")
    return


def signup():
    print("SignUp....")
    email = input("Enter email")
    password = input("Enter Password")
    try:
        user = auth.create_user_with_email_and_password(email, password)
    except:
        print("Email already exist")


if (response == "y"):
    login()
else:
    signup()
