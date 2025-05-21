from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user
from datetime import datetime
from models import db, Category

# @app.route('/category', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def category():

class CategoryResource(Resource):
    from models import Category
    def get(self):
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
            
            return make_response(jsonify({'status': 'ok', 'message': 'Categories retrieved successfully', 'categories': categories_list}), 200)
        return make_response(jsonify({'status': 'error', 'message': 'No categories found'}), 404)
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        if not name:
            return make_response(jsonify({'status': 'error', 'message': 'Name is required'}), 400)
        description = data.get('description')
        if not description:
            return make_response(jsonify({'status': 'error', 'message': 'Description is required'}), 400)
        new_category = Category(name=name, description=description)
        new_category.created_by = current_user.id
        new_category.date_created = datetime.now()
        db.session.add(new_category)
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'Create category', 'id': new_category.id, 'name': new_category.name}), 201)
    
    def put(self):
        data = request.get_json()
        category_id = data.get('id')
        if not category_id:
            return make_response(jsonify({'status': 'error', 'message': 'Category ID is required'}), 400)
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            return make_response(jsonify({'status': 'error', 'message': 'Category not found'}), 404)
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        category.updated_by = current_user.id
        category.date_updated = datetime.now()
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'Update category', 'id': category.id, 'name': category.name}), 201)
    
    def delete(self):
        data = request.get_json()
        category_id = data.get('id')
        if not category_id:
            return make_response(jsonify({'status': 'error', 'message': 'Category ID is required'}), 400)
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            return make_response(jsonify({'status': 'error', 'message': 'Category not found'}), 404)
        db.session.delete(category)
        db.session.commit()
        return make_response(jsonify({'status': 'ok', 'message': 'Delete category', 'id': category.id, 'name': category.name}), 200)