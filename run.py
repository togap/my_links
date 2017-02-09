import settings
from application import create_app
from flask import render_template

app = create_app(settings)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/links/new')
def new_link():
    return render_template('links/new.html')

if __name__ == '__main__':
    app.run()
