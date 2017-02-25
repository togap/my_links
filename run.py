import settings
from application import create_app
from flask import render_template, request, redirect, url_for, session
from application.models import User, Link, Tag
from application.models import db
from lxml import html, etree
import requests
import string
from functools import wraps
from flask_login import login_user, login_required, logout_user, LoginManager, current_user

app = create_app(settings)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def check_auth(username, password):
    user = User.query.filter_by(username=username).first()
    if user != None:
        if user.check_password(password):
            return user
    return None

def authenticate():
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = False
        if 'remember_me' in request.form:
            remember_me = True
        user = check_auth(username, password)
        if not user is None:
            print(remember_me)
            login_user(user, remember = remember_me)
            return redirect(request.args.get('next') or url_for('links'))

    return render_template('login/index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/links/new', methods=['GET', 'POST'])
@login_required
def new_link():
    if request.method == 'POST':
        url = request.form['url']
        page = requests.get(url)
        text = html.fromstring(page.content)
        title = text.xpath('//head/title/text()')[0]
        if len(text.xpath('//meta[@name="description"]/@content')) > 0:
            description = text.xpath('//meta[@name="description"]/@content')[0]
        elif len(text.xpath('//meta[@name="Description"]/@content')) > 0:
            description = text.xpath('//meta[@name="Description"]/@content')[0]
        elif len(text.xpath('//meta[@name="DESCRIPTION"]/@content')) > 0:
            description = text.xpath('//meta[@name="DESCRIPTION"]/@content')[0]
        else:
            description = None

        if len(text.xpath('//meta[@name="author"]/@content')) > 0:
            author = text.xpath('//meta[@name="author"]/@content')[0]
        elif len(text.xpath('//meta[@name="Author"]/@content')) > 0:
            author = text.xpath('//meta[@name="Author"]/@content')[0]
        elif len(text.xpath('//meta[@name="AUTHOR"]/@content')) > 0:
            author = text.xpath('//meta[@name="AUTHOR"]/@content')[0]
        else:
            author = None

        user = User.query.filter_by(id=1).first()
        link = Link(title, url, description, author, user)
        db.session.add(link)
        db.session.commit()
        return redirect(url_for('links'))
        
    return render_template('links/new.html')

@app.route('/links')
@login_required
def links():
    links = Link.query.filter_by(user_id=1).all()
    return render_template('links/list.html', links=links)

@app.route('/links/archived')
@login_required
def archived_links():
    params = {'user_id':1, 'state':True}
    links = Link.query.filter_by(**params).all()
    return render_template('links/list.html', links=links)

@app.route('/links/favorites')
@login_required
def favorites_links():
    params = {'user_id':1, 'favorite':True}
    links = Link.query.filter_by(**params).all()
    return render_template('links/list.html', links=links)

@app.route('/links/<int:id>')
@login_required
def detail_link(id):
    link = Link.query.get(id)
    return render_template('links/detail.html', link=link)

@app.route('/links/<int:link_id>/tags/<int:tag_id>/delete')
@login_required
def delete_link_tag(link_id, tag_id):
    tag = Tag.query.get(tag_id)
    link = Link.query.get(link_id)
    link.tags.remove(tag)
    db.session.add(link)
    db.session.commit()
    return redirect(url_for('attach_tag', id=link.id))

@app.route('/links/<int:id>/attach', methods=['GET', 'POST'])
@login_required
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

@app.route('/links/<int:id>/delete')
@login_required
def delete_link(id):
    link = Link.query.get(id)
    db.session.delete(link)
    db.session.commit()
    return redirect(url_for('links'))

@app.route('/links/<int:id>/favorite')
@login_required
def favorite_link(id):
    link = Link.query.get(id)
    link.favorite = not link.favorite
    db.session.commit()
    return redirect(request.referrer)

@app.route('/links/<int:id>/archived')
@login_required
def archived_link(id):
    link = Link.query.get(id)
    link.state = not link.state
    db.session.commit()
    return redirect(request.referrer)

@app.route('/tags')
@login_required
def tags():
    letters = string.ascii_lowercase
    tags = Tag.query.filter_by(user_id=1).order_by(Tag.name).all()
    o_tags = {}
    for letter in letters:
        o_tags[letter] = {'tags':[]}
        for tag in tags:
            if letter == tag.name[0]:
                o_tags[letter]['tags'].append(tag)

    return render_template('tags/list.html', o_tags=o_tags)

@app.route('/tags/<int:id>')
@login_required
def detail_tag(id):
    tag = Tag.query.get(id)
    return render_template('tags/detail.html', tag=tag)

@app.route('/tags/<int:id>/delete')
@login_required
def delete_tag(id):
    tag = Tag.query.get(id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tags'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
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

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

    return render_template('users/index.html')

if __name__ == '__main__':
    app.run()
