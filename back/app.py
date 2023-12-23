import os, json
from flask import Flask, render_template, request




app = Flask(__name__)
file_path = 'users.json'


# Check if the users.json file exists, if not, create it
if not os.path.exists(file_path):
    initial_data = {'users': []}
    with open(file_path, 'w') as json_file:
        json.dump(initial_data, json_file, indent=2)


# Loads user data from a JSON file
with open(file_path, 'r') as json_file:
    users_data = json.load(json_file)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/garage')
def garage():
    return render_template('garage.html')

@app.route('/xo')
def xo():
    return render_template('xo.html')



@app.route('/about')
def about():
    return render_template('about.html')


# ====== login and signup =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = any(user['username'] == username and user['password'] == password for user in users_data['users'])

        if user_exists:
            # Successful login
            return render_template('success.html')
        else:
            # Failed login
            msg = 'Invalid username or password'
            return render_template('login.html', msg = msg)
    return render_template('login.html', msg = msg) #GET    


# signup function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        # Checks if the new username is already taken
        if any(user['username'] == new_username for user in users_data['users']):
            msg = 'Username already taken. Please choose a different one.'
            return render_template('signup.html', msg=msg)

        # Adds the new user to the user data
        new_user = {'username': new_username, 'password': new_password}
        users_data['users'].append(new_user)

        # Writes the updated user data back into the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(users_data, json_file, indent=2)

        # Redirects to the login page and shows a success message
        return render_template('login.html',msg='Signup successful! Please login.')

    return render_template('signup.html')  

# ======== Garage ========
cars = []
my_data_file = "list.json"

# Check if the users.json file exists, if not, create it
if not os.path.exists(my_data_file):
    create_data = [
        [
            {
            "Brand": "Chevrolet",
            "Color": "Red",
            "ID": 1,
            "Model": "Corvette",
            "Plate": "123",
            "Year": "1999"
            }
        ],
        [
            {
            "Brand": "Ford",
            "Color": "Blue",
            "ID": 2,
            "Model": "Mustang",
            "Plate": "1234",
            "Year": "1979"
            }
        ]
    ]
    with open(my_data_file, 'w') as json_file:
        json.dump(create_data, json_file, indent=2)

# Loads user data from a JSON file
@app.route('/get_garage', methods=['GET'])
def get_garage():
    try:
        with open(my_data_file, 'r') as json_file:
            data = json.load(json_file)
        return {'status': 'success', 'data': data}
    except Exception as e:
        return {'status': 'error', 'message': f'Error fetching garage: {str(e)}'}


# Saves the garage data to the JSON file
@app.route('/save_garage', methods=['POST'])
def save_garage():
    try:
        data = request.get_json()
        with open(my_data_file, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return {'status': 'success', 'message': 'Garage saved successfully'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error saving garage: {str(e)}'}
    





#============================

if __name__ == "__main__":
    app.run(debug=True)    