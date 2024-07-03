from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from werkzeug.utils import secure_filename
from app import db
from app.model.model import TeamMember,User
from app.utils import allowed_file
import os
from dotenv import load_dotenv

team_bp = Blueprint('team', __name__)
load_dotenv()


@team_bp.route('/tagin/team/add', methods=['POST'])
def add_member():
    name = request.form['name']
    job_title = request.form['job_title']
    photo = request.files.get('photo')
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(os.getenv('UPLOAD_FOLDER'), filename)
        photo.save(photo_path)
        photo_url = url_for('uploaded_file', filename=filename)
        new_member = TeamMember(
            name=name, job_title=job_title, photo_url=photo_url)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('team.tagin'))
    else:
        print("error")
        return 'Invalid file type.', 400


@team_bp.route('/about')
def about():
    team_members = TeamMember.query.all()
    return render_template('about.html', team_members=team_members)


@team_bp.route('/tagin/team/edit/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    member = TeamMember.query.get(member_id)
    if request.method == 'POST':
        member.name = request.form['name']
        member.job_title = request.form['job_title']
        photo = request.files.get('photo')
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(os.getenv('UPLOAD_FOLDER'), filename)
            photo.save(photo_path)
            member.photo_url = url_for('uploaded_file', filename=filename)
        db.session.commit()
        return redirect(url_for('team.tagin'))
    return render_template('edit_member.html', member=member)


@team_bp.route('/tagin/team/delete/<int:member_id>', methods=['GET'])
def delete_member(member_id):
    member = TeamMember.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
    return redirect(url_for('team.tagin'))


@team_bp.route('/tagin', methods=['GET', 'POST'])
def tagin():
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
                return redirect(url_for('team.team'))
            else:
                return render_template('tagin.html', error='Invalid username or password')
    return render_template('tagin.html')


@team_bp.route('/tagout')
def tagout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('team.tagin'))

@team_bp.route('/tagin/team')
def team():
    team_members = TeamMember.query.all()
    return render_template('team.html', team_members=team_members)
