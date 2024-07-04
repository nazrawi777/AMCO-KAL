from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from werkzeug.utils import secure_filename
from app import db
from app.model.model import Product
from app.utils import allowed_file
import os
from dotenv import load_dotenv

product_bp = Blueprint('product', __name__)
load_dotenv()


@product_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(
        Product.id != product.id,
        Product.name.like(f'%{product.name.split()[0]}%')
    ).limit(4).all()
    return render_template('product_detail.html', product=product, related_products=related_products)


@product_bp.route('/prod')
def p_page():
    products = Product.query.all()
    return render_template('prod.html', products=products)


@product_bp.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_file = request.files.get('image')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(os.getenv('UPLOAD_FOLDER'), filename)
            image_file.save(image_path)
            new_product = Product(name=name, price=price,
                                  image=filename, description=description)
            db.session.add(new_product)
            db.session.commit()
            new_product.log_action('Added', f'''Product'{name}'added successfully.''')

            flash('Product added successfully.', 'success')
            return redirect(url_for('admin.admin'))
        else:
            flash('No image selected or invalid file type.', 'error')
            return redirect(request.url)
    return render_template('add_product.html')


@product_bp.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('admin.login'))
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        image_file = request.files.get('image')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(os.getenv('UPLOAD_FOLDER'), filename)
            image_file.save(image_path)
            product.image = filename
        db.session.commit()
        product.log_action('Edited',f"Product '{product.name}' edited successfully.")
        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin.admin'))
    return render_template('edit_product.html', product=product)


@product_bp.route('/admin/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('admin.login'))
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    product.log_action('Deleted',f"Product '{product.name}' deleted successfully")
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('admin.admin'))
