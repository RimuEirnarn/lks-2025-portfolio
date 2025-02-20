# """Posts controller"""

# from time import time
# from flask import redirect, render_template, request
# from flask_login import login_required, current_user
# from future_router import Router, ResourceDummy
# from db import posts_tbl

# router = Router()


# @router.resource("/posts")
# class PostsController(ResourceDummy):
#     """Posts controller"""

#     @login_required
#     @staticmethod
#     def index():
#         uid = current_user.uid
#         return render_template(
#             "user_posts.html", posts=posts_tbl.select({"author_id": uid})
#         )

#     @login_required
#     @staticmethod
#     def update(res_id):
#         uid = current_user.uid
#         post = posts_tbl.select_one({"post_id": res_id})
#         if post.author_id != uid:
#             return render_template("unauthorized.html"), 403
#         data = request.form.to_dict()
#         posts_tbl.update_one(
#             {
#                 "post_id": res_id,
#                 "author_id": uid,
#                 "title": data["title"],
#                 "content": data["content"],
#                 "updated_at": time(),
#             }
#         )
#         return redirect("/posts")
