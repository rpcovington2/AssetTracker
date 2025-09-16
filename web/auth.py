from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from .models import SignUpForm, LoginForm, User
from web import db
from werkzeug.security import generate_password_hash, check_password_hash

# TODO: Make Function to add budget total to the next months bills???

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        email = loginForm.Email.data
        user = User.query.filter_by(Email=email).first()
        if user:
            # TODO: SETUP SIGNUP SCREEN TO Hash(SHA-256) PASSWORDSh
            # if check_password_hash(user.Password, loginForm.Password.data):
            if check_password_hash(user.password, loginForm.Password.data):
                login_user(user, True)
                flash("Login Successful!!", 'Success')
                if user.Role == 'Guest':
                    return redirect(url_for('views.wish'))
                else:
                    return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password/E-mail!!", 'error')
                # return redirect(url_for('views.home'))
        else:
            print("Error")
            flash("Sign up", 'error')

    return render_template("login.html", loginform=loginForm, user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    SignUpform = SignUpForm()

    if SignUpform.validate_on_submit():
        # print(SignUpform.pass)
        Email = SignUpform.Email.data
        users = User.query.filter(User.Email == Email).count()
        if users >= 1:
            flash("Email Already in use!!!", 'error')
            return redirect(url_for('auth.login'))
        else:
            userCount = User.query.count()
            if SignUpform.Password.data == SignUpform.Password2.data:
                new_User = User(id=int(userCount) + 1,
                                FirstName=SignUpform.FirstName.data,
                                LastName=SignUpform.LastName.data,
                                Email=SignUpform.Email.data,
                                Username=SignUpform.Email.data,
                                password=generate_password_hash(SignUpform.Password.data),
                                Role='Guest',
                                )
                db.session.add(new_User)
                db.session.commit()
                flash("Account Created!!", "Success")

                # print(f"First Name: {SignUpform.FirstName.data}")
                # print(f"Last name: {SignUpform.LastName.data}")
                # print(f"E-Mail: {SignUpform.Email.data}")
                # print(f"Password: {SignUpform.Password.data}")
                # print(f"Confirm Password: {SignUpform.Password2.data}")
                #
                return redirect(url_for('auth.login'))
            else:
                flash("Passwords Do not Match!!!", "error")

    return render_template("register.html", form=SignUpform, user=current_user)
