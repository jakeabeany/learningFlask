from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'jake'}
    posts = [
        {
            'author': {'username': 'Charlotte'},
            'body': 'Beautiful day in Nowich'
        },
        {
            'author': {'username': 'Matty'},
            'body': 'I am a fuckin goat'
        }
    ]

    return render_template('index.html', title="A title", user=user, posts=posts)
