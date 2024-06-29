from flask import Blueprint, jsonify, request, flash, redirect
from app.model.model import SlideVideoDb, YoutubeVideosLinks, AboutSlide, ClientList
from app import db
import cloudinary
import cloudinary.uploader
import cloudinary.api


upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/sidevideo/upload', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # Upload video to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file, resource_type='auto')
            newSlidevideo = SlideVideoDb(
                name=file.filename,
                public_id=upload_result['public_id'],
                url=upload_result['secure_url']
            )
            db.session.add(newSlidevideo)
            db.session.commit()
            flash('File successfully uploaded')
            return jsonify({'status': 'success', 'message': 'Slider upload successfully'})
        else:
            flash('No file part')
            return redirect(request.url)
    return jsonify({'status': 'error', 'message': 'Something went wrong'})


@upload_bp.route('/youtube-link/upload', methods=['POST'])
def upload_link():
    if request.method == 'POST':
        link = request.values.get('link')
        if link:
            newYoutubevideo = YoutubeVideosLinks(
                url=link
            )
            db.session.add(newYoutubevideo)
            db.session.commit()
            flash('Link successfully uploaded')
            return jsonify({'status': 'success', 'message': 'Link upload successfully'})
        else:
            flash('link is required')
            return redirect(request.url)
    return jsonify({'status': 'error', 'message': 'Something went wrong'})


@upload_bp.route('/about-img/upload', methods=['POST'])
def upload_about_img():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # Upload image to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file, resource_type='auto')
            newSlidevideo = AboutSlide(
                name=file.filename,
                public_id=upload_result['public_id'],
                url=upload_result['secure_url']
            )
            db.session.add(newSlidevideo)
            db.session.commit()
            flash('File successfully uploaded')
            return jsonify({'status': 'success', 'message': 'Slider upload successfully'})
        else:
            flash('No file part')
            return redirect(request.url)
    return jsonify({'status': 'error', 'message': 'Something went wrong'})


@upload_bp.route('/client-log/upload', methods=['POST'])
def upload_client_img():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # Upload image to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file, resource_type='auto')
            newSlidevideo = ClientList(
                name=file.filename,
                public_id=upload_result['public_id'],
                url=upload_result['secure_url']
            )
            db.session.add(newSlidevideo)
            db.session.commit()
            flash('File successfully uploaded')
            return jsonify({'status': 'success', 'message': 'Slider upload successfully'})
        else:
            flash('No file part')
            return redirect(request.url)
    return jsonify({'status': 'error', 'message': 'Something went wrong'})
