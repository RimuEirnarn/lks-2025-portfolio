import time
from flask import request
from flask_restful import Resource
from helpers import csrf
from db.helpers import generate_id
from limiter import limiter

from db import contact_form_tbl
from db.tables.contactform import VAL_REQUIRED
from .base import api


class ContactForm(Resource):
    """Contact form"""

    decorators = [csrf.exempt, limiter.limit("5 per minute")]

    def post(self):

        data = dict(request.json)
        data["full_name"] = data.get("firstname") + " " + data.get("lastname")

        if not all(field in data for field in VAL_REQUIRED):
            return {
                "message": "Missing required fields. Make sure either email, fullname, phone number, title, and message is provided"
            }, 400

        entry = {
            "id": generate_id(),
            "email": data["email"],
            "full_name": data["full_name"],
            "phone_number": data["phone_number"],
            "title": data["title"],
            "message": data["message"],
            "created_at": time.time(),
        }

        contact_form_tbl.insert(entry)

        return {"message": "Contact form submitted successfully", "data": entry}, 201


def register_resource():
    api.add_resource(ContactForm, "/contact")
