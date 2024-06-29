# routes/home_routes.py
from flask import Blueprint, render_template, url_for
from app.model.model import SliderDb, SlideVideoDb, YoutubeVideosLinks, ClientList, AboutSlide

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
@home_bp.route('/home')
def home():
    # Fetch data from database
    slideImg = SliderDb.query.all()
    videos = SlideVideoDb.query.all()
    links = YoutubeVideosLinks.query.all()
    client_list = ClientList.query.all()
    about_img = AboutSlide.query.all()

    # Pass data to template
    return render_template('home.html', slideImg=slideImg, videoSlides=videos, i=0, data={
        "links": links,
        "client_list": client_list,
        "about_img": about_img
    })
