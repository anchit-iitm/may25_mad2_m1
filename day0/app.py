from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    backend_name = 'anchit'
    return render_template('page2.html', frontend_name=backend_name)

@app.route('/page2/<path_name>')
def page2_with_name(path_name):
    return render_template('page2.html', frontend_name=path_name)

@app.route('/page3', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        backend_name = request.form['name']
        return render_template('page3.html', frontend_name=backend_name)
    return render_template('page3.html')

@app.route('/page4', methods=['GET', 'POST'])
def page4():
    if request.method == 'POST':
        backend_name = request.form['name']
        backend_age = request.form['age']
        if backend_age.isdigit():
            backend_age = int(backend_age)
        else:
            backend_age = 0
        return render_template('page4.html', frontend_name=backend_name, frontend_age=backend_age)
    return render_template('page4.html')

if __name__ == "__main__":
    app.run(debug=True)