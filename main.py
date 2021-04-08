from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/hello/<name>', methods=['GET'])
def hello_world(name):
    print("GET ran")
    return render_template('hello_world.html', name=name)

@app.route('/hello/<name>', methods=['POST'])
def hello_world_process_post(name):
    print("POST ran")
    fname = request.form['fname']
    lname = request.form['lname']
    context = {
        'fname': fname,
        'lname': lname,
        'name':name,
    }
    return render_template('hello_world_results.html', **context)
