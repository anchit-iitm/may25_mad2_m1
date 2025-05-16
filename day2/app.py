from flask import Flask, request
from flask_security import Security, auth_required, roles_required, roles_accepted, current_user
from flask_restful import Api
from datetime import datetime
import os

from models import db, user_datastore
from routes.category import CategoryResource

def create_app():
    init_app = Flask(__name__)

    from config import localDev
    init_app.config.from_object(localDev)

    db.init_app(init_app)

    init_api = Api(init_app, prefix='/api')
    return init_app, init_api

app, api = create_app()

api.add_resource(CategoryResource, '/category')

Security(app, user_datastore)


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
        print(user.password)
    if not user:
        return {'status': 'error', 'message': 'User not found'}, 404
    if user and user.password != password:
        return {'status': 'error', 'message': 'Invalid password'}, 401
    
    auth_token = user.get_auth_token()

    return {
        'status': 'ok',
        'message': 'Login successful',
        'auth_token': auth_token,
        'role': user.roles[0].name if user.roles else None,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'last_login_at': user.last_login_at if user.last_login_at else None,
    }, 200


@app.route('/test', methods=['GET'])
@auth_required('token')
# @roles_required('user', 'admin') # AND
@roles_accepted('user', 'admin') # OR
def test():
    # found_user = User.query.filter_by(id=1).first()
    # print(found_user.email)
    return {'status': 'ok', 'message': 'Test successful', 'email': current_user.username}, 200


@app.route('/category', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_required('token')
@roles_accepted('admin')
def category():
    from models import Category
    if request.method == 'GET':
        categories = Category.query.all()
        if categories:
            categories_list = []
            for category in categories:
                categories_list.append({
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'date_created': category.date_created,
                    'date_updated': category.date_updated,
                    'created_by': category.created_by,
                    'updated_by': category.updated_by
                })
            
            return {'status': 'ok', 'message': 'Categories retrieved successfully, from older api', 'categories': categories_list}, 200
        return {'status': 'error', 'message': 'No categories found'}, 404
    
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        if not name:
            return {'status': 'error', 'message': 'Name is required'}, 400
        description = data.get('description')
        if not description:
            return {'status': 'error', 'message': 'Description is required'}, 400
        new_category = Category(name=name, description=description)
        new_category.created_by = current_user.id
        new_category.date_created = datetime.now()
        db.session.add(new_category)
        db.session.commit()
        return {'status': 'ok', 'message': 'Create category', 'id': new_category.id, 'name': new_category.name}, 201
    
    elif request.method == 'PUT':
        data = request.get_json()
        category_id = data.get('id')
        if not category_id:
            return {'status': 'error', 'message': 'Category ID is required'}, 400
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            return {'status': 'error', 'message': 'Category not found'}, 404
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        category.updated_by = current_user.id
        category.date_updated = datetime.now()
        db.session.commit()
        return {'status': 'ok', 'message': 'Update category', 'id': category.id, 'name': category.name}, 201
    
    elif request.method == 'DELETE':
        data = request.get_json()
        category_id = data.get('id')
        if not category_id:
            return {'status': 'error', 'message': 'Category ID is required'}, 400
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            return {'status': 'error', 'message': 'Category not found'}, 404
        db.session.delete(category)
        db.session.commit()
        return {'status': 'ok', 'message': 'Delete category', 'id': category.id, 'name': category.name}, 200
    

if __name__ == '__main__':

    app.run()