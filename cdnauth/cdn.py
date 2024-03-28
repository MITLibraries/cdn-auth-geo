from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from flask import (
    Blueprint,
    render_template,
    session,
    request,
    make_response,
    current_app,
)

from cdnauth.auth import login_required

import jwt

bp = Blueprint("cdn", __name__, url_prefix="/")


@bp.route("/")
@login_required
def session_jwt():
    if "cdn_resource" in request.args:
        if valid_redirect(request.args["cdn_resource"]) is False:
            return "Invalid redirect URL"
        response = make_response(
            render_template("download.html", cdn_resource=request.args["cdn_resource"])
        )
        token = jwt.encode(
            {
                "user": session["samlNameId"],
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=1),
                "nbf": datetime.now(tz=timezone.utc) - timedelta(minutes=5),
            },
            current_app.config["JWT_SECRET"],
            algorithm="HS256",
        )
        response.set_cookie(
            current_app.config["COOKIE_NAME"],
            token,
            domain=current_app.config["COOKIE_DOMAIN"],
        )
        return response

    else:
        return "No download URL present"


# valid_redirect(url) ensures the redirect is to a domain we trust to prevent
# our app being used to trick users into clicking on malicious links
def valid_redirect(url):
    domain = urlparse(url).netloc
    if domain in valid_domains():
        return True
    return False


# valid_domains() is a list of domains we trust for redirect purposes
def valid_domains():
    return [
        "cdn.libraries.mit.edu",
        "cdn.dev1.mitlibrary.net",
        "cdn.stage.mitlibrary.net",
    ]
