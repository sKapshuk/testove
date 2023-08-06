from flask import render_template, redirect, url_for, flash, request
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from urllib.parse import urlparse
from functools import partial, wraps

import os

@app.route("/")
@app.route("/category")
def category():
    category = Category.query.all()

    return render_template("category_main.html", category=category, title="Category List")

@app.route("/product/<int:category_id>", methods=["GET", "POST"])
def products(category_id):
    category = Category.query.filter_by(id=category_id).first()
    products = category.products

    if ("price_min" in request.form) and (request.form["price_min"]):
        products = [product for product in products if product.price >= float(request.form["price_min"])]

    if ("price_max" in request.form) and (request.form["price_max"]):
        products = [product for product in products if product.price <= float(request.form["price_max"])]

    return render_template("product_main.html", products=products, category = category, title="Products List")

@app.route("/product_info/<int:product_id>")
def product_info(product_id):
    product = Product.query.filter_by(id=product_id).first()
    return render_template("product_info.html", product=product, title="View Product")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect(url_for("category"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if (user is None) or (not user.check_password(form.password.data)):
            flash("Invalid email or password")
            return redirect(url_for("login"))

        login_user(user=user)
        next_page = request.args.get("next")

        if (not next_page) or (urlparse(next_page).netloc != ""):
            next_page = url_for("category")

        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        redirect(url_for("category"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(password=form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template("registration.html", form=form)

def restricted_entry(f, *, list_role=["Admin"]):
    if f is None:
        return partial(restricted_entry, list_role=list_role)

    @wraps(f)
    def inner(*args, **kwargs):
        if set([role.name for role in current_user.roles]).intersection(list_role):
            return f(*args, **kwargs)
        else:
            return redirect(url_for("category"))
    return inner


@app.route("/admin")
@restricted_entry
def admin_panel():
    return render_template("layout.html")

@app.route("/admin/category")
@restricted_entry
def admin_category():
    category = Category.query.all()
    return render_template("category.html", category=category)

@app.route("/admin/edit_category/<int:category_id>", methods=["GET", "POST"])
@restricted_entry
def edit_category(category_id):
    category = Category.query.filter_by(id=category_id).first()
    return render_template("edit_category.html", category=category)

@app.route("/admin/delete_category/<int:category_id>", methods=["GET", "POST"])
@restricted_entry
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id).first()

    for product in category.products:
        image_delete(image_name=product.id, config_path="PRODUCT_UPLOAD_FOLDER")
        db.session.delete(product)

    image_delete(image_name=category_id, config_path="CATEGORY_UPLOAD_FOLDER")
    db.session.delete(category)
    db.session.commit()

    flash(message='The category was successfully deleted !!', category='message')
    return redirect(url_for('admin_category'))

def image_delete(image_name, config_path):
    os.remove(os.path.join(app.config[config_path], f"{image_name}.jpg"))

def image_save(request, file_name, image_name, config_path, remove):
    image = request.files[file_name]

    if remove:
        image_delete(image_name, config_path)

    image.save(os.path.join(app.config[config_path], f"{image_name}.jpg"))

@app.route("/admin/save_category", methods=["POST"])
@restricted_entry
def save_category():
    category = Category.query.filter_by(name=request.form['name']).first()

    if category is not None:
        if (request.form["action"] == "updateCategory") and (int(request.form["categoryid"]) == category.id):
            function = "edited"

            remove = True if request.files["uploadFile"] else None
        else:
            flash(message='Please use a different category name.', category='warning')
            return redirect(url_for("admin_category"))

    else:
        if request.form["action"] == "updateCategory":
            function = "edited"
            category = Category.query.filter_by(id=request.form["categoryid"]).first()
            category.name = request.form['name']

            remove = True if request.files["uploadFile"] else None
        else:
            function = "added"
            category = Category(name=request.form["name"])
            db.session.add(category)
            # db.session.flush()

            remove = False
        db.session.commit()

    if remove is not None:
        image_save(request,
                   file_name="uploadFile",
                   image_name=category.id,
                   config_path="CATEGORY_UPLOAD_FOLDER",
                   remove=remove)

    flash(message=f'The category was successfully {function} !!', category='message')

    return redirect(url_for("admin_category"))

@app.route("/admin/product")
@restricted_entry
def admin_product():
    products = Product.query.all()
    category = Category.query.all()
    return render_template("product.html", products=products, category=category)

@app.route("/admin/edit_product/<int:product_id>", methods=["GET", "POST"])
@restricted_entry
def edit_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    category = Category.query.all()
    return render_template("edit_product.html", product=product, category=category)

@app.route("/admin/delete_product/<int:product_id>", methods=["GET", "POST"])
@restricted_entry
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()

    image_delete(image_name=product.id, config_path="PRODUCT_UPLOAD_FOLDER")
    db.session.delete(product)
    db.session.commit()

    flash(message='The product was successfully deleted !!', category='message')
    return redirect(url_for('admin_product'))

@app.route("/admin/save_product", methods=["POST"])
@restricted_entry
def save_product():
    if request.form["action"] == "updateProduct":
        function = "edited"
        product = Product.query.filter_by(id=request.form["productid"]).first()
        category = Category.query.filter_by(id=request.form.get('category_select')).first()

        product.name = request.form['name']
        product.price = request.form['price'],
        product.quantity = request.form['quantity'],
        product.description = request.form['description'],
        product.category = category

        remove = True if request.files["uploadFile"] else None
    else:
        function = "added"

        category = Category.query.filter_by(id=request.form.get('category_select')).first()
        product = Product(name=request.form['name'],
                          price=request.form['price'],
                          quantity=request.form['quantity'],
                          description=request.form['description'],
                          category=category)

        # db.session.flush()
        remove = False

    db.session.add(product)
    db.session.commit()

    if remove is not None:
        image_save(request,
                   file_name="uploadFile",
                   image_name=product.id,
                   config_path="PRODUCT_UPLOAD_FOLDER",
                   remove=remove)

    flash(message=f'The product was successfully {function} !!', category='message')

    return redirect(url_for("admin_product"))