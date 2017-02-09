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
        user = User.query.get(1)
        link = Link(url, user)
        db.session.add(link)
        db.session.commit()
        return "Success"
        
    return render_template('links/new.html')

@app.route('/links')
def links():
    links = Link.query.filter_by(user_id=1).all()
    return render_template('links/list.html', links=links)

if __name__ == '__main__':
    app.run()
