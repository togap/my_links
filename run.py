import settings
from application import create_app
from flask import render_template, request

app = create_app(settings)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/links/new', methods=['GET', 'POST'])
def new_link():
    if request.method == 'POST':
        user = request.form['url']
        return user
    return render_template('links/new.html')

if __name__ == '__main__':
    app.run()
