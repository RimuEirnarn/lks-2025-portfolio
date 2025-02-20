"""Categorycontroller"""

from time import time
from flask import flash, jsonify, redirect, render_template, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from future_router import Router, ResourceDummy
from controller.helpers import discard_when_matched, filler
from db import category_tbl
from db.content import validate_enum
from db.helpers import generate_id
from forms_setup.content import ContentForm

router = Router()


@router.resource("/content")
class ContentController(ResourceDummy):
    """Categorycontroller"""

    @staticmethod
    def index():
        return render_template("admin/content.html", data=category_tbl.select())

    @login_required
    @staticmethod
    def update(res_id):
        form = ContentForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("admin/form/content.html", form=form), 400

        data = category_tbl.select_one({"id": res_id})
        if not data:
            flash("Content not found", "danger")
            return redirect("/content")

        file = form.thumbnail.data

        pre_entry = {
            "title": form.title.data,
            "content_type": form.content_type.data,
            "sort_description": form.sort_description.data,
            "thumbnail": (
                ""
                if file is None
                else f"static/uploads/{secure_filename(file.filename)}"
            ),
            "sub_title": form.sub_title.data,
            "content": form.content.data,
            "score": form.score.data,
            "updated_at": time(),
        }

        if file:
            file.save(f"static/uploads/{secure_filename(file.filename)}")

        entry = {"id": res_id, "author": current_user.id}
        entry.update(filler(pre_entry))
        entry = discard_when_matched(entry, data)

        if not validate_enum(entry["content_type"]):
            flash("Invalid content type", "danger")
            return render_template("content.html", form=form), 400

        category_tbl.update_one(entry)

        flash("Content updated successfully", "success")
        return redirect("/content")

    @login_required
    @staticmethod
    def create():
        return render_template("admin/form/content.html", form=ContentForm())

    @login_required
    @staticmethod
    def store():
        form = ContentForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("admin/form/content.html", form=form), 400

        file0 = form.thumbnail.data

        category_tbl.insert(
            {
                "id": generate_id(),
                "title": form.title.data,
                "content_type": form.content_type.data,
                "sort_description": form.sort_description.data,
                "thumbnail": (
                    ""
                    if file0 is None
                    else f"static/uploads/{secure_filename(file0.filename)}"
                ),
                "sub_title": form.sub_title.data,
                "content": form.content.data,
                "score": form.score.data,
                "created_at": time(),
                "updated_at": time(),
                "author": current_user.id,
            }
        )

        if file0:
            file0.save(f"static/uploads/{secure_filename(file0.filename)}")

        flash("Content created successfully", "success")
        return redirect("/content")

    @login_required
    @staticmethod
    def edit(res_id):
        data = category_tbl.select_one({"id": res_id})
        if not data:
            flash("Content not found", "danger")
            return redirect("/content")

        form = ContentForm(data=data)
        return render_template("admin/form/content.html", form=form)

    @login_required
    @staticmethod
    def destroy(res_id):
        category_tbl.delete({"id": res_id})
        flash("Content deleted successfully", "success")
        return redirect("/content")

    @login_required
    @staticmethod
    def show(res_id):
        data = category_tbl.select_one({"id": res_id})
        if not data:
            flash("Content not found", "danger")
            return redirect("/content")

        return render_template("admin/data/content.html", **data)
