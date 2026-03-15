from web import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
#from wtforms import *
#from wtforms.validators import DataRequired, Length, NumberRange, Optional
#from wtforms.widgets import TextArea
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(45), index=False, unique=True, nullable=False)
    FirstName = db.Column(db.String(80))
    LastName = db.Column(db.String(80))
    Email = db.Column(db.String(255))
    password = db.Column(db.String(45))
    Role = db.Column(db.String(45))


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    # Name = db.Column(db.String(1000))
    AccountFrom = db.Column(db.String(1000))
    AccountPaid = db.Column(db.String(1000))
    Amount = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    PostedDate = db.Column(db.String(1000), nullable=True)
    Date = db.Column(db.String(1000))
    Comment = db.Column(db.String(1000))
    Type = db.Column(db.String(1000))

class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))
    location = db.Column(db.String(255))
    status = db.Column(db.String(50), default='available')
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<Asset {self.asset_id} - {self.name}>"

#    ALL FORMS USED IN WEB APP
class IncomeForm(FlaskForm):
    Name = StringField('Name')
    Amount = DecimalField('Amount Due')
    NextPayDate = DateField('Next Pay Date', default=datetime.now())
    Frequency = SelectField(u'Frequency',
                            choices=[(0, 'Weekly'), (2, 'Bi-Weekly'), (1, 'Monthly')])
    submit = SubmitField('Add')


class SignUpForm(FlaskForm):
    FirstName = StringField('First Name', [DataRequired()], render_kw={"placeholder": "test"})
    LastName = StringField('Last Name', [DataRequired()])
    Email = StringField('E-Mail Address', [DataRequired()])
    Password = PasswordField('Password', [DataRequired(), Length(min=4, max=20)])
    Password2 = PasswordField('Confirm Password', [DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    Email = StringField('Username/E-mail', [DataRequired()])
    Password = PasswordField('Password', [DataRequired()], id='password')
    submit = SubmitField('Login')


class EditProfile(FlaskForm):
    FirstName = StringField('First Name')
    LastName = StringField('Last Name')
    Email = StringField('E-Mail Address')
    HomePhone = StringField('Phone')
    MobilePhone = StringField('Mobile')
    Address = StringField('Address')
    City = StringField('City')
    State = StringField('State')
    Sumbit = SubmitField('Submit')


class ProductForm(FlaskForm):
    Description = StringField('Description')
    Barcode = StringField('UPC')
    Brand = StringField('Brand')
    Unit = StringField('Unit Type')
    Price = DecimalField('Price')
    Size = DecimalField('Size')
    submit = SubmitField('Submit')


class IssueForm(FlaskForm):
    Name = TextAreaField('Issue')
    # Amount = DecimalField('Amount Due')
    DueDate = StringField('Due Date')
    userName = StringField('UserName')
    # Password = StringField('Password')
    Active = SelectField(u'Priority', choices=[('High'), ('Medium'), ('Low')])
    submit = SubmitField('Add')

class AssetForm(FlaskForm):
    asset_id = StringField('Asset ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Type')
    location = StringField('Location')
    status = StringField('Status')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Asset')


