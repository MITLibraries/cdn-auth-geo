import json
import os
from functools import wraps
from urllib.parse import urljoin, urlparse

from flask import (
    Blueprint,
    current_app,
    make_response,
    redirect,
    request,
    session,
    url_for,
)

from onelogin.saml2.auth import OneLogin_Saml2_Auth


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (
            current_app.config["ENV"] != "development"
            and "samlSessionIndex" not in session
        ):
            return redirect(url_for("auth.saml", sso=True, next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def load_saml_settings():
    json_settings = {}
    with open("saml/settings.json", "r") as json_file:
        json_settings = json.load(json_file)
        json_settings["debug"] = current_app.config["DEBUG"]
        json_settings["sp"]["entityId"] = os.getenv("SP_ENTITY_ID")
        json_settings["sp"]["assertionConsumerService"]["url"] = os.getenv("SP_ACS_URL")
        json_settings["sp"]["x509cert"] = os.getenv("SP_CERT")
        json_settings["sp"]["privateKey"] = os.getenv("SP_KEY")
        json_settings["idp"]["entityId"] = os.getenv("IDP_ENTITY_ID")
        json_settings["idp"]["singleSignOnService"]["url"] = os.getenv("IDP_SSO_URL")
        json_settings["idp"]["x509cert"] = os.getenv("IDP_CERT")
    return json_settings


def prepare_flask_request(request):
    url_data = urlparse(request.url)
    return {
        "https": "on" if request.scheme == "https" else "off",
        "http_host": request.host,
        "server_port": url_data.port,
        "script_name": request.path,
        "get_data": request.args.copy(),
        "post_data": request.form.copy(),
    }


bp = Blueprint("auth", __name__, url_prefix="/saml")


@bp.route("/", methods=("GET", "POST"))
def saml():
    saml_settings = load_saml_settings()
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, saml_settings)
    errors = []
    next_page = request.args.get("next")
    if not next_page or is_safe_url(next_page) is False:
        next_page = ""

    if "sso" in request.args:
        return redirect(auth.login(return_to=next_page))

    elif "acs" in request.args:
        auth.process_response()
        errors = auth.get_errors()
        if not auth.is_authenticated():
            # TODO: return something helpful to the user
            pass
        if len(errors) == 0:
            session["samlNameId"] = auth.get_nameid()
            session["samlSessionIndex"] = auth.get_session_index()
            return redirect(request.form["RelayState"])
        else:
            print("Errors: %s", errors)
            print("Last error reason: %s", auth.get_last_error_reason())


@bp.route("/metadata/")
def metadata():
    saml_settings = load_saml_settings()
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, saml_settings)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers["Content-Type"] = "text/xml"
    else:
        resp = make_response(", ".join(errors), 500)
    return resp
