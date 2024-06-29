# routes/vacancy_routes.py
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from datetime import datetime
from app import db
from app.model.model import Job, AppliedJob
import os
from dotenv import load_dotenv


vacancy_bp = Blueprint('vacancy', __name__)
load_dotenv()


@vacancy_bp.route('/vadmin/add_job', methods=['GET', 'POST'])
def add_job():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        requirements = request.form['requirements']
        deadline = datetime.strptime(
            request.form['deadline'], '%Y-%m-%dT%H:%M')
        job = Job(title=title, description=description,
                  requirements=requirements, deadline=deadline)
        db.session.add(job)
        db.session.commit()
        job.log_action('Added', f"Job '{title}' added successfully.")
        return "Job added successfully!"
    return render_template('add_job.html')


@vacancy_bp.route('/vadmin/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    db.session.delete(job)
    db.session.commit()
    job.log_action('Deleted', f"Job '{job.title}' deleted successfully.")
    return redirect(url_for('vacancy.vadmin'))


@vacancy_bp.route('/vacancy')
def vacancy():
    jobs = Job.query.filter_by(is_active=True).all()
    return render_template('vacancy.html', jobs=jobs)


@vacancy_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        jobs = Job.query.filter(Job.title.ilike(f'%{search_term}%')).all()
        return render_template('search_results.html', jobs=jobs, search_term=search_term)
    return redirect(url_for('home'))


@vacancy_bp.route('/lagin', methods=['GET', 'POST'])
def lagin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('vacancy.vadmin'))
        else:
            return render_template('lagin.html', error='Invalid username or password')
    return render_template('lagin.html')


@vacancy_bp.route('/lagout')
def lagout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('vacancy.lagin'))


@vacancy_bp.route('/lagin/vadmin')
def vadmin():
    jobs = Job.query.all()
    return render_template('vadmin.html', jobs=jobs)


@vacancy_bp.route('/vadmin/applied_jobs/<int:job_id>')
def applied_jobs(job_id):
    applied_jobs = AppliedJob.query.filter_by(job_id=job_id).all()
    return render_template('applied_jobs.html', applied_jobs=applied_jobs, job_id=job_id)


@vacancy_bp.route('/vadmin/delete_applied_job/<int:applied_job_id>', methods=['POST'])
def delete_applied_job(applied_job_id):
    applied_job = AppliedJob.query.get(applied_job_id)
    db.session.delete(applied_job)
    db.session.commit()
    applied_job.log_action('Deleted', f"Applied job with ID '{
                           applied_job_id}' deleted successfully.")
    return redirect(url_for('vacancy.applied_jobs', job_id=applied_job.job_id))


@vacancy_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    job = Job.query.get(job_id)
    current_time = datetime.now()
    if job.deadline and job.deadline < current_time:
        return render_template('apply.html', job=job, error='Application deadline has passed.', current_time=current_time)
    if request.method == 'POST':
        first_name = request.form['first_name']
        father_name = request.form['father_name']
        email = request.form['email']
        gender = request.form['gender']
        age = request.form['age']
        cv = request.files['cv']
        cv.save(os.path.join(os.getenv('UPLOAD_FOLDER'), cv.filename))
        applied_job = AppliedJob(
            job_id=job_id,
            first_name=first_name,
            father_name=father_name,
            applicant_email=email,
            gender=gender,
            age=age,
            cv_path=f"uploads/{cv.filename}"
        )
        db.session.add(applied_job)
        db.session.commit()
        return redirect(url_for('vacancy.vacancy'))
    return render_template('apply.html', job=job, current_time=current_time)
