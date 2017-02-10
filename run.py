import settings
from application import create_app
from flask import render_template, request, redirect
from application.models import User, Link
from application.models import db
from lxml import html, etree
import requests

app = create_app(settings)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/links/new', methods=['GET', 'POST'])
def new_link():
    if request.method == 'POST':
        url = request.form['url']
        page = requests.get(url)
        text = html.fromstring(page.content)
        title = text.xpath('//head/title/text()')
        user = User.query.filter_by(id=1).first()
        link = Link(title[0], url, user)
        db.session.add(link)
        db.session.commit()
        return redirect('/links')
        
    return render_template('links/new.html')

@app.route('/links')
def links():
    links = Link.query.filter_by(user_id=1).all()
    return render_template('links/list.html', links=links)

if __name__ == '__main__':
    app.run()
