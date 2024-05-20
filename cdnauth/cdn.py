import logging

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

logging.basicConfig(level=logging.INFO)

bp = Blueprint("cdn", __name__, url_prefix="/")


@bp.route("/")
@login_required
def session_jwt():
    """Sets a JWT token as domain cookie if the redirect url is valid"""
    if "cdn_resource" in request.args:
        if valid_redirect(request.args["cdn_resource"]) is False:
            logging.info(f"Invalid redirect URL: {request.args['cdn_resource']}")
            return "Invalid redirect URL"

        cdn_resource = request.args["cdn_resource"]

        if "timdexui=true" in cdn_resource:
            timdexui = True
        else:
            timdexui = False

        response = make_response(
            render_template("download.html", cdn_resource=cdn_resource,
                            timdexui=timdexui))
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
        logging.info("No download URL present")
        return "No download URL present"


def valid_redirect(url):
    """valid_redirect(url) ensures the redirect is to a domain we trust to prevent
    our app being used to trick users into clicking on malicious links
    """
    domain = urlparse(url).netloc
    if domain in valid_domains():
        return True
    return False


def valid_domains():
    """valid_domains() is a list of domains we trust for redirect purposes"""
    return current_app.config["VALID_DOMAINS"].split(",")
