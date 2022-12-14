from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for, flash
from flask_login import current_user
from flask_security import login_required
from models import *
from .forms import PostForm
from app import db, app, user_datastore

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def post_create():
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
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page, per_page=4)

    return render_template('posts/post_create.html', form=form, pages=pages)


@posts.route('/')
def posts_list():
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

    return render_template('posts/posts.html', posts=posts, pages=pages, form=form)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    return render_template('posts/tag_detail.html', tag=tag)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def post_update(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post, form=form)


@app.route('/profile')
@login_required
def user_profile():
    poster = current_user.id
    return render_template('user_profile.html', poster=poster)


@app.route('/create_admin', methods=['POST', 'GET'])
def create_admin():
    if request.method == 'POST':
        admin_user = user_datastore.create_user(email=request.form['email'], password=request.form['password'])
        db.session.add(admin_user)
        roles = user_datastore.add_role_to_user(admin_user, 'admin')
        db.session.commit()
        return "Creation Successful"
    return render_template('create_admin.html')


@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    req = request.form
    password = req.get('password')
    email = req.get('email')
    if request.method == 'POST':
        user = user_datastore.create_user(firstname=request.form['firstname'], lastname=request.form['lastname'],
                                          email=request.form['email'], password=request.form['password'])
        if not len(password) >= 6:
            return redirect(request.url)
            flash("Password length must be 6 or more characters!")
        else:
            db.session.add(user)
            db.session.commit()
            flash("Account Created!")

        return render_template('create_acc.html', String='Account Created')
    return render_template('create_acc.html')
