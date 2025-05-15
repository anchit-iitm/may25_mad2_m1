from flask import Flask, render_template, request

from models_mad1_to_mad2 import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

# @app.route('/page1')
# def page1():
#     return render_template('page1.html')

# @app.route('/page2')
# def page2():
#     backend_name = 'anchit'
#     return render_template('page2.html', frontend_name=backend_name)

@app.route('/page2/<path_name>')
def page2_with_name(path_name):
    # return render_template('page2.html', frontend_name=path_name)
    return {'frontend_name': path_name}

@app.route('/page3', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        backend_name = request.json['name']
        if not User.query.filter_by(name=backend_name).first():
            new_name = User(name=backend_name, age=0)
            db.session.add(new_name)
            db.session.commit()
        # return render_template('page3.html', frontend_name=backend_name)
        return {'frontend_name': backend_name}
    # return render_template('page3.html')
    return {'status': 'ok, it should have rendered out the page'}

@app.route('/page4', methods=['GET', 'POST'])
def page4():
    if request.method == 'POST':
        backend_name = request.form['name']
        backend_age = request.form['age']
        if backend_age == None:
            backend_age = 0
        new_user = User(name=backend_name, age=int(backend_age))
        db.session.add(new_user)
        db.session.commit()
        return render_template('page4.html', frontend_name=backend_name, frontend_age=int(backend_age))
    return render_template('page4.html', frontend_name='', frontend_age=0)

if __name__ == "__main__":
    app.run(debug=True)