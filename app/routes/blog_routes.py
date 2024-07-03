# routes/blog_routes.py
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from datetime import datetime
from app import db
from app.model.model import BlogPost, Event, NewsArticle,User

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/bloog')
def bloog():
    blog_posts = BlogPost.query.all()
    events = Event.query.all()
    news_articles = NewsArticle.query.all()
    return render_template('c.html', blog_posts=blog_posts, events=events, news_articles=news_articles)


@blog_bp.route('/bagin', methods=['GET', 'POST'])
def bagin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please enter both username and password.', 'error')
        else:
            find_user = User.query.filter_by(username=username).first()
            if find_user and find_user.password == password:
                session['admin_logged_in'] = True
                session['username'] = username
                session['role'] = find_user.role
                return redirect(url_for('blog.badmin'))
            else:
                flash('Invalid username or password.', 'error')
    return render_template('bagin.html')


@blog_bp.route('/bagout')
def bagout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))


@blog_bp.route('/badmin')
def badmin():
    posts = BlogPost.query.all()
    articles = NewsArticle.query.all()
    events = Event.query.all()
    return render_template('badmin.html', posts=posts, articles=articles, events=events)


@blog_bp.route('/badmin/blog/create', methods=['GET', 'POST'])
def create_blog_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_post = BlogPost(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        flash('Blog post created successfully', 'success')
        return redirect(url_for('blog.badmin'))
    return render_template('create_blog_post.html')


@blog_bp.route('/badmin/blog/edit/<int:id>', methods=['GET', 'POST'])
def edit_blog_post(id):
    post = BlogPost.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        flash('Blog post updated successfully', 'success')
        return redirect(url_for('blog.badmin'))
    return render_template('edit_blog_post.html', post=post)


@blog_bp.route('/badmin/blog/delete/<int:id>', methods=['POST'])
def delete_blog_post(id):
    post = BlogPost.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted successfully', 'success')
    return redirect(url_for('blog.badmin'))


@blog_bp.route('/badmin/events/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        location = request.form['location']
        new_event = Event(title=title, description=description,
                          date=date, location=location)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully', 'success')
        return redirect(url_for('blog.badmin'))
    return render_template('create_event.html')


@blog_bp.route('/badmin/events/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get(id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.description = request.form['description']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        event.location = request.form['location']
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('blog.badmin'))
    return render_template('edit_event.html', event=event)


@blog_bp.route('/badmin/events/delete/<int:id>', methods=['POST'])
def delete_event(id):
    event = Event.query.get(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('blog.badmin'))


@blog_bp.route('/badmin/news/create', methods=['GET', 'POST'])
def create_news_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_article = NewsArticle(title=title, content=content, author=author)
        db.session.add(new_article)
        db.session.commit()
        flash('News article created successfully', 'success')
        return redirect(url_for('blog.badmin'))
    return render_template('create_news_article.html')


@blog_bp.route('/badmin/news/edit/<int:id>', methods=['GET', 'POST'])
def edit_news_article(id):
    article = NewsArticle.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.author = request.form['author']
        db.session.commit()
        flash('News article updated successfully', 'success')
        return redirect(url_for('blog.badmin'))
    return render_template('edit_news_article.html', article=article)


@blog_bp.route('/badmin/news/delete/<int:id>', methods=['POST'])
def delete_news_article(id):
    article = NewsArticle.query.get(id)
    db.session.delete(article)
    db.session.commit()
    flash('News article deleted successfully', 'success')
    return redirect(url_for('blog.badmin'))
