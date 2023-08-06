from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime


user_role = db.Table("user_role",
                         db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                         db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
                         )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    orders = db.relationship("Order", backref="user", lazy='dynamic')
    roles = db.relationship("Role", secondary=user_role, lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_admin(self, admin_name="Admin"):
        return admin_name in [role.name for role in self.roles]

    def __repr__(self):
        return "<User {id}: {email}>".format(id=self.id, email=self.email)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


order_product = db.Table("order_product",
                         db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
                         db.Column("product_id", db.Integer, db.ForeignKey("product.id"))
                         )

class Order(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    date_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_edit = db.Column(db.DateTime, nullable=True)
    date_end = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(120), nullable=False, default="Processing in progress")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    products = db.relationship("Product", secondary=order_product, backref="orders")

    def __repr__(self):
        return "<Order {date}: {user_id} - {products} - {address}>".format(date=self.date_start,
                                                                           user_id=self.user_id,
                                                                           products=[product.id for product in self.products],
                                                                           address=self.address_id)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    orders = db.relationship("Order", backref="address", lazy='dynamic')

    def __repr__(self):
        return "<Address {id}: {orders}>".format(id=self.id,
                                                 orders=[order.id for order in self.orders])

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # image_id = db.Column(db.Integer, nullable=False)
    products = db.relationship("Product", backref="category", lazy="dynamic")

    def __repr__(self):
        return "<Category {id}: {products}>".format(id=self.id,
                                                    products=[product.id for product in self.products])

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    # image_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __repr__(self):
        return "<Product {id}: {category_name} - {name}>".format(id=self.id,
                                                                 category_name=self.category.name,
                                                                 name=self.name)
