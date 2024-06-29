from app.model.model import ActionHistory
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app import db

action_history_bp = Blueprint('action_history', __name__)


@action_history_bp.route('/sagin/super')
def super_view():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('action_history.sagin'))
    actions = ActionHistory.query.order_by(ActionHistory.timestamp.desc()).all()
    return render_template('all.html', actions=actions)


@action_history_bp.route('/sagin/delete_action/<int:action_id>', methods=['POST'])
def delete_action(action_id):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('action_history.sagin'))
    action = ActionHistory.query.get_or_404(action_id)
    db.session.delete(action)
    db.session.commit()
    flash('Action deleted successfully.', 'success')
    return redirect(url_for('action_history.super_view'))


@action_history_bp.route('/sagin', methods=['GET', 'POST'])
def sagin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('action_history.super_view'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('sagin.html')


@action_history_bp.route('/sagout')
def sagout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))
