"""Core Flask app routes."""
from flask import render_template
from flask import current_app as app


@app.route('/')
def home():
    return render_template('index.jinja2',
                           title='Artist.io | What is artists',
                           template='home-template',
                           body="This is a homepage served with Flask.")

    
   