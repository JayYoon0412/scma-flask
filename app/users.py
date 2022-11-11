from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.purchase import Purchase
from .models.user import User

from flask import Blueprint

bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


class PurchasesForm(FlaskForm):
    user_id = IntegerField('Enter User id: ')
    submit = SubmitField('Submit')


@bp.route('/users/purchases', methods=['GET', 'POST'])
def get_purchases():
    purchasesForm = PurchasesForm()
    if purchasesForm.validate_on_submit():
        purchases = Purchase.getByUserId(purchasesForm.user_id.data)
        return render_template('userPurchases.html', purchasesForm=purchasesForm, purchases=purchases)
    return render_template('userPurchases.html', purchasesForm=purchasesForm)


@bp.route('/account', methods=['GET'])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user = User.get(current_user.get_id())
    return render_template('account/profile.html', user=user)


class EditForm(FlaskForm):
    field1 = StringField('Default')
    field2 = StringField('Default')
    has_field2 = False
    submit = SubmitField('Confirm')


class PasswordEditForm(FlaskForm):
    field1 = PasswordField('Enter New Password:')
    field2 = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('field1')])
    has_field2 = True
    submit = SubmitField('Confirm')


@bp.route('/account/edit/name', methods=['GET', 'POST'])
def edit_name():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user = User.get(current_user.get_id())
    editForm = EditForm()

    editForm.has_field2 = True
    editForm.field1.label = 'Enter New First Name:'
    editForm.field2.label = 'Enter New Last Name:'

    if editForm.validate_on_submit():
        if User.update_name(current_user.get_id(), editForm.field1.data, editForm.field2.data):
            flash('Name Changed Successfully')
            return redirect(url_for('users.account'))
    return render_template('account/accountEdit.html', user=user, editForm=editForm)


@bp.route('/account/edit/email', methods=['GET', 'POST'])
def edit_email():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user = User.get(current_user.get_id())
    editForm = EditForm()

    editForm.field1.label = 'Enter New Email:'
    editForm.field1.validators = [Email()]
    if editForm.validate_on_submit():
        if User.email_exists(editForm.field1.data):
            flash('Already a user with this email')
            return redirect(url_for('users.edit_email'))

        if User.update_email(current_user.get_id(), editForm.field1.data):
            flash('Email Changed Successfully')
            return redirect(url_for('users.account'))
    return render_template('account/accountEdit.html', user=user, editForm=editForm)


@bp.route('/account/edit/password', methods=['GET', 'POST'])
def edit_password():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user = User.get(current_user.get_id())
    editForm = PasswordEditForm()

    if editForm.validate_on_submit():
        if User.update_password(current_user.get_id(), editForm.field2.data):
            flash('Password Changed Successfully')
            return redirect(url_for('users.account'))
    return render_template('account/accountEdit.html', user=user, editForm=editForm)


@bp.route('/account/edit/address', methods=['GET', 'POST'])
def edit_address():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user = User.get(current_user.get_id())
    editForm = EditForm()

    editForm.field1.label = 'Enter New Address:'
    if editForm.validate_on_submit():
        if User.update_address(current_user.get_id(), editForm.field1.data):
            flash('Address Changed Successfully')
            return redirect(url_for('users.account'))
    return render_template('account/accountEdit.html', user=user, editForm=editForm)