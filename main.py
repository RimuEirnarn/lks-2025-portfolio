"""Main"""

from os import environ
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_login import LoginManager, login_required
from flask_bootstrap import Bootstrap5

from helpers import is_admin, load_user, csrf
from controller.auth import router as login
from controller.api.base import api
from controller.api.contact_form import register_resource as contact_form_registry

from controller.category import router as category
from controller.content import router as content
from controller.portfolio import router as portfolio

# from controller.api.auth import register_resource as auth_registry

load_dotenv()

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY", "secret")
login_manager = LoginManager()
bootstrap = Bootstrap5()

# ==== API/CONTROLLER INJECTION ====

# auth_registry()
contact_form_registry()
api.init_app(app)
bootstrap.init_app(app)
# csrf.init_app(app)
login_manager.init_app(app)
login_manager.user_loader(load_user)
# posts.init_app(app)
login.init_app(app)
category.init_app(app)
content.init_app(app)
portfolio.init_app(app)


# ==== WEB ROUTE ====


@app.get("/")
def root():
    """Index"""
    return render_template("index.html")


@app.get("/dashboard")
@login_required
@is_admin
def dashboard():
    """Dashboard"""
    return render_template("dashboard.html")


@app.get("/about")
def about():
    """About us"""
    return render_template("about.html")


@app.get("/testing")
def test():
    return render_template("testing.html")


# ==== RUN ====

if __name__ == "__main__":
    app.run("127.0.0.1", 8000, debug=True, use_reloader=True, threaded=True)
