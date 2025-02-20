"""Categorycontroller"""

from time import time
from flask import flash, jsonify, redirect, render_template, request
from flask_login import login_required, current_user
from future_router import Router, ResourceDummy
from controller.helpers import discard_when_matched, filler
from db import portfolio_tbl
from forms_setup.portfolio import PortfolioForm

router = Router()


@router.resource("/portfolio")
class portfolioController(ResourceDummy):
    """Categorycontroller"""

    @staticmethod
    def index():
        return jsonify({"data": portfolio_tbl.select()})

    @login_required
    @staticmethod
    def update(res_id):
        form = PortfolioForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("portfolio.html", form=form), 400

        data = portfolio_tbl.select_one({"id": res_id})
        if not data:
            flash("portfolio not found", "danger")
            return redirect("/portfolio")

        pre_entry = {
            "title": form.title.data,
            "sort_description": form.sort_description.data,
            "category": form.category.data,
            "thumbnail": form.thumbnail.data,
            "content": form.content.data,
            "cover": form.cover.data,
            "meta_title": form.meta_title.data,
            "meta_description": form.meta_description.data,
            "is_active": form.is_active.data,
            "updated_at": time(),
            "tags": form.tags.data,
            "slug": form.slug.data,
        }

        entry = {"id": res_id, "author": current_user.id}
        entry.update(filler(pre_entry))
        entry = discard_when_matched(entry, data)

        portfolio_tbl.update_one(entry)

        flash("portfolio updated successfully", "success")
        return redirect("/portfolio")

    @login_required
    @staticmethod
    def create():
        return render_template("portfolio.html", form=PortfolioForm())

    @login_required
    @staticmethod
    def store():
        form = PortfolioForm()
        if not form.validate_on_submit():
            flash("Invalid form data", "danger")
            return render_template("portfolio.html", form=form), 400

        portfolio_tbl.insert(
            {
                "title": form.title.data,
                "sort_description": form.sort_description.data,
                "category": form.category.data,
                "thumbnail": form.thumbnail.data,
                "content": form.content.data,
                "cover": form.cover.data,
                "meta_title": form.meta_title.data,
                "meta_description": form.meta_description.data,
                "is_active": form.is_active.data,
                "author": current_user.id,
                "tags": form.tags.data,
                "slug": form.slug.data,
                "created_at": time(),
                "updated_at": time(),
            }
        )
        flash("portfolio created successfully", "success")
        return redirect("/portfolio")

    @login_required
    @staticmethod
    def edit(res_id):
        data = portfolio_tbl.select_one({"id": res_id})
        if not data:
            flash("portfolio not found", "danger")
            return redirect("/portfolio")

        form = PortfolioForm(data=data)
        return render_template("portfolio.html", form=form)

    @login_required
    @staticmethod
    def destroy(res_id):
        portfolio_tbl.delete({"id": res_id})
        flash("portfolio deleted successfully", "success")
        return redirect("/portfolio")

    @login_required
    @staticmethod
    def show(res_id):
        data = portfolio_tbl.select_one({"id": res_id})
        if not data:
            flash("portfolio not found", "danger")
            return redirect("/portfolio")

        return jsonify({"data": data})
