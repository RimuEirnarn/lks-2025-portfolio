"""Category controller"""

from time import time
from flask import flash, jsonify, redirect, render_template, request
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from future_router import Router, ResourceDummy
from controller.helpers import discard_when_matched, filler
from db import category_tbl
from db.helpers import generate_id
from forms_setup.category import CategoryForm

router = Router()


@router.resource("/category")
class CategoryController(ResourceDummy):
    """Category controller"""

    @staticmethod
    def index():
        return render_template("admin/category.html", data=category_tbl.select())

    @login_required
    @staticmethod
    def update(res_id):
        form = CategoryForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("admin/category_form.html", form=form), 400

        data = category_tbl.select_one({"id": res_id})
        if not data:
            flash("Category not found", "danger")
            return redirect("/category")

        file = form.thumbnail.data

        pre_entry = {
            "title": form.title.data,
            "sort_description": form.sort_description.data,
            "is_active": form.is_active.data,
            "thumbnail": (
                ""
                if file is None
                else f"static/uploads/{secure_filename(file.filename)}"
            ),
            "updated_at": time(),
        }

        if file:
            file.save(f"static/uploads/{secure_filename(file.filename)}")

        entry = {
            "id": res_id,
        }

        entry.update(filler(pre_entry))
        entry = discard_when_matched(entry, data)

        category_tbl.update_one(entry)

        flash("Category updated successfully", "success")
        return redirect("/category")

    @login_required
    @staticmethod
    def create():
        return render_template("admin/form/category.html", form=CategoryForm())

    @login_required
    @staticmethod
    def store():
        form = CategoryForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("admin/form/category.html", form=form), 400

        file0 = form.thumbnail.data

        category_tbl.insert(
            {
                "id": generate_id(),
                "title": form.title.data,
                "sort_description": form.sort_description.data,
                "created_at": time(),
                "thumbnail": (
                    ""
                    if file0 is None
                    else f"static/uploads/{secure_filename(file0.filename)}"
                ),
                "is_active": form.is_active.data,
            }
        )

        if file0:
            file0.save(f"static/uploads/{secure_filename(file0.filename)}")
        flash("Category created successfully", "success")
        return redirect("/category")

    @login_required
    @staticmethod
    def edit(res_id):
        data = category_tbl.select_one({"id": res_id})
        if not data:
            flash("Category not found", "danger")
            return redirect("/category")

        form = CategoryForm(data=data)
        return render_template("admin/form/category.html", form=form)

    @login_required
    @staticmethod
    def destroy(res_id):
        category_tbl.delete({"id": res_id})
        flash("Category deleted successfully", "success")
        return redirect("/category")

    @login_required
    @staticmethod
    def show(res_id):
        data = category_tbl.select_one({"id": res_id})
        if not data:
            flash("Category not found", "danger")
            return redirect("/category")

        return render_template("admin/data/category.html", **data)
