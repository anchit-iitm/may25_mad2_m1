from flask import Flask, request
from flask_security import Security

from models import db, user_datastore
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_LOGIN_URL'] = '/SiGnIn'

db.init_app(app)
Security(app, user_datastore)

with app.app_context():
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    '''
    new_role = Role(name='admin', description='Administrator')
    db.session.add(new_role)
    '''
    user_datastore.find_or_create_role(name='user', description='User')
    db.session.commit()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return {'status': 'error', 'message': 'Username is required'}, 400
    email = data.get('email')
    if not email:
        return {'status': 'error', 'message': 'Email is required'}, 400
    password = data.get('password')
    if not password:
        return {'status': 'error', 'message': 'Password is required'}, 400

    if not user_datastore.find_user(email=email):
        new_user = user_datastore.create_user(email=email, username=username, password=password)
        user_datastore.add_role_to_user(new_user, 'user')
        db.session.commit()
        return {'status': 'ok', 'message': 'User created successfully'}
    return {'status': 'error', 'message': 'User already exists'}, 400


@app.route('/login', methods=['POST'])  
def login():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    if not email and not username:
        return {'status': 'error', 'message': 'Email or Username is required'}, 400
    password = data.get('password')
    if not password:
        return {'status': 'error', 'message': 'Password is required'}, 400
    
    if email:
        user = user_datastore.find_user(email=email)
    else:
        user = user_datastore.find_user(username=username)
    if not user:
        return {'status': 'error', 'message': 'User not found'}, 404
    if user and user.password != password:
        return {'status': 'error', 'message': 'Invalid password'}, 401
    
    auth_token = user.get_auth_token()

    return {
        'status': 'ok',
        'message': 'Login successful',
        'auth_token': auth_token
    }, 200
    


if __name__ == '__main__':
    app.run(debug=True)