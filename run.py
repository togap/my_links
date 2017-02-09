import settings
from application import create_app
from flask import render_template, request
from application.models import User, Link
from application.models import db

app = create_app(settings)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/links/new', methods=['GET', 'POST'])
def new_link():
    if request.method == 'POST':
        url = request.form['url']
        user = User.query.filter_by(id=1).first()
        link = Link(url, user)
        db.session.add(link)
        db.session.commit()
        return "Success"
        
    return render_template('links/new.html')

if __name__ == '__main__':
    app.run()
