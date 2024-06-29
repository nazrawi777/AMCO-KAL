# routes/admin_routes.py
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app import db
import cloudinary
from app.model.model import SliderDb, SlideVideoDb, YoutubeVideosLinks, ClientList, AboutSlide, Product
from app.utils import allowed_file

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login/admin', methods=['GET', 'POST'])
def admin():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return render_template('login.html')

    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            # Upload file to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file, resource_type='auto')
            newSlider = SliderDb(
                name=file.filename,
                public_id=upload_result['public_id'],
                url=upload_result['secure_url']
            )
            db.session.add(newSlider)
            db.session.commit()
            flash('File successfully uploaded')
            return "File successfully uploaded"
        else:
            flash('No file part or invalid file type')
            return redirect(request.url)

    # Fetch data from database for admin page
    products = Product.query.all()
    slideImg = SliderDb.query.all()
    slideVideo = SlideVideoDb.query.all()
    links = YoutubeVideosLinks.query.all()
    client_list = ClientList.query.all()
    about_img = AboutSlide.query.all()

    # Pass data to admin template
    return render_template('admin.html', data={
        "products": products,
        "slideImg": slideImg,
        "slideVideo": slideVideo,
        "links": links,
        "client_list": client_list,
        "about_img": about_img
    })


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin.admin'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))
