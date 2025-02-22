"""Auth"""

from flask import flash, redirect, render_template
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from future_router import Router

from helpers import User
from db import users_tbl
from db.tables.users import VAL_VISIBILITY as USER_DATA_VISIBILITY
from db.helpers import generate_id
from forms_setup.login import LoginForm
from forms_setup.register import Register

router = Router()


@router.route("/register", methods=["GET", "POST"])
def register():
    """Register"""
    form = Register()
    if not form.validate_on_submit():
        return render_template("register.html", form=form)
    username = form.username.data
    if users_tbl.select_one({"username": username}):
        flash("Username already exists")
        return render_template("register.html", form=form)
    fullname = form.fullname.data
    password = form.password.data
    email = form.email.data
    photo = form.photo.data
    uid = generate_id()

    if photo.filename:
        photo.save(f"static/uploads/{secure_filename(photo.filename)}")

    users_tbl.insert(
        {
            "id": uid,
            "full_name": fullname,
            "email": email,
            "photo": (
                f"static/uploads/{secure_filename(photo.filename)}"
                if photo.filename
                else ""
            ),
            "username": username,
            "password": generate_password_hash(password),
        }
    )
    user = users_tbl.select_one({"id": uid}, only=USER_DATA_VISIBILITY)
    login_user(User.load(**user))
    flash("Successfully created your account", "success")
    return redirect("/dashboard")


@router.route("/login", methods=["GET", "POST"])
def login():
    """Login"""
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template("login.html", form=form)

    username = form.username.data
    password = form.password.data
    remember = form.remember.data

    user = users_tbl.select_one({"username": username})
    if not user:
        flash(f"No account is registered as {username}", "warning")
        return render_template("login.html", form=form)

    if not check_password_hash(user.password, password):
        flash("Invalid password", "danger")
        return render_template("login.html", form=form)

    print(user)
    login_user(User.load(**user), remember=remember)

    flash("Logged in successfully", "success")
    return redirect("/dashboard")


@router.post("/logout")
@login_required
def logout():
    """Logout"""
    logout_user()
    flash("You have been logged out", "success")
    return redirect("/")


@router.post("/delete_account")
@login_required
def delete_account():
    """Delete account"""
    user = current_user.id
    logout_user()
    users_tbl.delete_one({"id": user})
    flash("Your account has been deleted", "success")
