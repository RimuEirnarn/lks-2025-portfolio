"""Categorycontroller"""

from time import time
from flask import flash, jsonify, redirect, render_template, request
from flask_login import login_required, current_user
from future_router import Router, ResourceDummy
from controller.helpers import discard_when_matched, filler
from db import content_tbl
from db.content import validate_enum
from forms_setup.content import ContentForm

router = Router()


@router.resource("/content")
class ContentController(ResourceDummy):
    """Categorycontroller"""

    @staticmethod
    def index():
        return jsonify({"data": content_tbl.select()})

    @login_required
    @staticmethod
    def update(res_id):
        form = ContentForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("content.html", form=form), 400

        data = content_tbl.select_one({"id": res_id})
        if not data:
            flash("Content not found", "danger")
            return redirect("/content")

        pre_entry = {
            "title": form.title.data,
            "content_type": form.content_type.data,
            "sort_description": form.sort_description.data,
            "thumbnail": form.thumbnail.data,
            "sub_title": form.sub_title.data,
            "content": form.content.data,
            "score": form.score.data,
            "updated_at": time(),
        }

        entry = {"id": res_id, "author": current_user.id}
        entry.update(filler(pre_entry))
        entry = discard_when_matched(entry, data)

        if not validate_enum(entry["content_type"]):
            flash("Invalid content type", "danger")
            return render_template("content.html", form=form), 400

        content_tbl.update_one(entry)

        flash("Content updated successfully", "success")
        return redirect("/content")

    @login_required
    @staticmethod
    def create():
        return render_template("content.html", form=ContentForm())

    @login_required
    @staticmethod
    def store():
        form = ContentForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("content.html", form=form), 400

        content_tbl.insert(
            {
                "title": form.title.data,
                "content_type": form.content_type.data,
                "sort_description": form.sort_description.data,
                "thumbnail": form.thumbnail.data,
                "sub_title": form.sub_title.data,
                "content": form.content.data,
                "score": form.score.data,
                "created_at": time(),
                "updated_at": time(),
                "author": current_user.id,
            }
        )
        flash("Content created successfully", "success")
        return redirect("/content")

    @login_required
    @staticmethod
    def edit(res_id):
        data = content_tbl.select_one({"id": res_id})
        if not data:
            flash("Content not found", "danger")
            return redirect("/content")

        form = ContentForm(data=data)
        return render_template("content.html", form=form)

    @login_required
    @staticmethod
    def destroy(res_id):
        content_tbl.delete({"id": res_id})
        flash("Content deleted successfully", "success")
        return redirect("/content")

    @login_required
    @staticmethod
    def show(res_id):
        data = content_tbl.select_one({"id": res_id})
        if not data:
            flash("Content not found", "danger")
            return redirect("/content")

        return jsonify({"data": data})
