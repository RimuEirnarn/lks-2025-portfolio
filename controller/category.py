"""Category controller"""

from time import time
from flask import flash, jsonify, redirect, render_template, request
from flask_login import login_required, current_user
from future_router import Router, ResourceDummy
from controller.helpers import discard_when_matched, filler
from db import content_tbl
from forms_setup.category import ContentForm

router = Router()


@router.resource("/category")
class CategoryController(ResourceDummy):
    """Category controller"""

    @staticmethod
    def index():
        return jsonify({"data": content_tbl.select()})

    @login_required
    @staticmethod
    def update(res_id):
        form = ContentForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("category.html", form=form), 400

        data = content_tbl.select_one({"id": res_id})
        if not data:
            flash("Category not found", "danger")
            return redirect("/category")

        pre_entry = {
            "title": form.title.data,
            "sort_description": form.sort_description.data,
            "is_active": form.is_active.data,
            "thumbnail": form.thumbnail.data,
            "updated_at": time(),
        }

        entry = {
            "id": res_id,
        }

        entry.update(filler(pre_entry))
        entry = discard_when_matched(entry, data)

        content_tbl.update_one(entry)

        flash("Category updated successfully", "success")
        return redirect("/category")

    @login_required
    @staticmethod
    def create():
        return render_template("category.html", form=ContentForm())

    @login_required
    @staticmethod
    def store():
        form = ContentForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("category.html", form=form), 400

        content_tbl.insert(
            {
                "title": form.title.data,
                "sort_description": form.sort_description.data,
                "created_at": time(),
                "thumbnail": form.thumbnail.data,
                "is_active": form.is_active.data,
            }
        )
        flash("Category created successfully", "success")
        return redirect("/category")

    @login_required
    @staticmethod
    def edit(res_id):
        data = content_tbl.select_one({"id": res_id})
        if not data:
            flash("Category not found", "danger")
            return redirect("/category")

        form = ContentForm(data=data)
        return render_template("category.html", form=form)

    @login_required
    @staticmethod
    def destroy(res_id):
        content_tbl.delete({"id": res_id})
        flash("Category deleted successfully", "success")
        return redirect("/category")

    @login_required
    @staticmethod
    def show(res_id):
        data = content_tbl.select_one({"id": res_id})
        if not data:
            flash("Category not found", "danger")
            return redirect("/category")

        return jsonify({"data": data})
