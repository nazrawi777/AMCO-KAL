# routes/delete_routes.py
from flask import Blueprint, jsonify, request, redirect
from app import db
from app.model.model import AboutSlide, SliderDb, YoutubeVideosLinks, SlideVideoDb,ClientList
from werkzeug.utils import secure_filename
import cloudinary.uploader

delete_bp = Blueprint('delete', __name__)


@delete_bp.route('/slide/delete/<string:id>', methods=['GET', 'POST'])
def delete_slider(id):
    try:
        if request.method == "POST":
            resource_type = request.values.get('type')
            delete_result = ""
            if resource_type == 'video':
                delete_result = cloudinary.uploader.destroy(
                    id, resource_type="video")
            elif resource_type == "link":
                YoutubeVideosLinks.query.filter_by(id=id).delete()
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'deleted successfully'})
            else:
                delete_result = cloudinary.uploader.destroy(id)
            if delete_result['result'] == 'ok':
                slider_type = request.values.get('type')
                if slider_type == 'image':
                    SliderDb.query.filter_by(public_id=id).delete()
                    db.session.commit()
                    return jsonify({'status': 'success', 'message': 'Slider deleted successfully'})
                elif slider_type == 'about':
                    AboutSlide.query.filter_by(public_id=id).delete()
                    db.session.commit()
                    return jsonify({'status': 'success', 'message': 'Slider deleted successfully'})
                elif slider_type == 'logo':
                    ClientList.query.filter_by(public_id=id).delete()
                    db.session.commit()
                    return jsonify({'status': 'success', 'message': 'Slider deleted successfully'})
                elif slider_type == 'video':
                    SlideVideoDb.query.filter_by(public_id=id).delete()
                    db.session.commit()
                    return jsonify({'status': 'success', 'message': 'Slider deleted successfully'})
                else:
                    return jsonify({'status': 'error', 'message': 'Failed to delete item'})
            else:
                return jsonify({'status': 'error', 'message': 'Failed to delete item'})
    except cloudinary.exceptions.Error as e:
        return jsonify({'status': 'error', 'message': 'Failed to delete item'})
    return redirect(request.url)
