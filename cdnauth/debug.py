from flask import Blueprint, render_template

from cdnauth.auth import login_required


bp = Blueprint("debug", __name__, url_prefix="/debug")


@bp.route("/")
@login_required
def item():
    return render_template("debug.html")
