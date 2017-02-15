import settings
from application import create_app
from flask import render_template, request, redirect
from application.models import User, Link, Tag
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

@app.route('/links/<int:id>')
def detail_link(id):
    link = Link.query.get(id)
    return render_template('links/detail.html', link=link)

@app.route('/edit/<int:id>')
def edit(id):
    link = Link.query.get(id)
    return link

@app.route('/links/<int:id>/attach', methods=['GET', 'POST'])
def attach_tag(id):
    link = Link.query.get(id)
    if request.method == 'POST':
        user = User.query.filter_by(id=1).first()
        name = request.form['tag']
        tag = Tag.query.filter_by(name=name.lower()).first()
        if tag is None:
            tag = Tag(name.lower(), user)
            
        link.tags.append(tag)
        db.session.add(link)
        db.session.commit()
        return render_template('links/attach.html', link=link)

    return render_template('links/attach.html', link=link)

@app.route('/tags')
def tags():
    tags = Tag.query.filter_by(user_id=1).all()
    return render_template('tags/list.html', tags=tags)

@app.route('/tags/<int:id>')
def detail_tag(id):
    tag = Tag.query.get(id)
    return render_template('tags/detail.html', tag=tag)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        tag = Tag.query.filter_by(name=search.lower()).first()
        if tag is None:
            links = Link.query.filter(
                    Link.title.ilike('%' + search + '%')).all()
        else:
            links = tag.links
        return render_template('search/index.html', links=links)
    return render_template('search/index.html')

if __name__ == '__main__':
    app.run()
