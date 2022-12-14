from urllib import request
from flask_login import current_user
from app import app, db
from flask import render_template, redirect, url_for
from models import Post
from posts.forms import PostForm
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for, flash
from flask_login import current_user
from flask_security import login_required
from models import *
from posts.forms import PostForm
from app import db, app, user_datastore


@app.route('/')
def index():
    form = PostForm()
    q = request.args.get('q')
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        poster = current_user.id

        try:
            post = Post(title=title, body=body, poster_id=poster)
            db.session.add(post)
            db.session.commit()
        except:
            print('Very long traceback')
        return redirect(url_for('posts.post_detail', slug=post.slug))

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.asc())

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page, per_page=4)
    return render_template('index.html', posts=posts, pages=pages, form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
