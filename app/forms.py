from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField, FileField, SelectField, IntegerField, FloatField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError, NumberRange, DataRequired
from app.models import User, Category

class LoginForm(FlaskForm):
    email = EmailField(label="Email")
    password = PasswordField(label="Password")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    email = EmailField(label="Email", validators=[InputRequired(), Email()])
    password = PasswordField(label="Password", validators=[InputRequired(), Length(min=8, max=60,message="Min Length - 8; Max Length - 60"),
                                                           EqualTo(fieldname="password_confirm",message="Passwords must match")])
    password_confirm = PasswordField("Repeat Password")
    submit = SubmitField("Sign In")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# class CategoryForm(FlaskForm):
#     name = StringField(label="Name", validators=[InputRequired(), Length(min=1, max=60,message="Min Length - 1; Max Length - 60")])
#     # img = FileField("Image")
#     submit = SubmitField("Submit")
#
#     def validate_name(self, name):
#         category = Category.query.filter_by(name=name.data).first()
#         if category is not None:
#             raise ValidationError('Please use a different category name.')

# class ProductForm(FlaskForm):
#     name = StringField(label="Name", validators=[InputRequired(), Length(min=1, max=60, message="Min Length - 1; Max Length - 60")])
#     category = SelectField(label="Category")
#     price = FloatField(label="Price", validators=[InputRequired(), NumberRange(min=0, message="Min Price - 0")])
#     quantity = IntegerField(label="Quantity", validators=[InputRequired(), NumberRange(min=0, message="Min Quantity - 0")])
#     description = StringField(label="Description", validators=[InputRequired()])
#     img = FileField("Image")
#     submit = SubmitField("Submit")

# class FilterForm(FlaskForm):
#     price_min = StringField('Price min')
#     price_max = StringField('Price max')
#     submit = SubmitField('Submit')

