from flask import Blueprint

from cdnauth.auth import login_required


bp = Blueprint("debug", __name__, url_prefix="/debug")


@bp.route("/")
@login_required
def item(item="None"):
    return "debug"
