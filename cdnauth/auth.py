import logging
import json
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

logging.basicConfig(level=logging.INFO)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "samlNameId" not in session:
            return redirect(url_for("auth.saml", sso=True, next=request.url))

        return f(*args, **kwargs)

    return decorated_function


def load_saml_settings():
    """Load SAML settings for use in metadata generation and communication with the IdP

    This method overrides or adds values to what exists in the saml/settings.json file
    """
    json_settings = {}
    with open("saml/settings.json", "r") as json_file:
        json_settings = json.load(json_file)
        json_settings["debug"] = current_app.config["DEBUG"]
        json_settings["sp"]["entityId"] = current_app.config["SP_ENTITY_ID"]
        json_settings["sp"]["assertionConsumerService"]["url"] = current_app.config[
            "SP_ACS_URL"
        ]
        json_settings["sp"]["x509cert"] = current_app.config["SP_CERT"]
        json_settings["sp"]["privateKey"] = current_app.config["SP_KEY"]
        json_settings["idp"]["entityId"] = current_app.config["IDP_ENTITY_ID"]
        json_settings["idp"]["singleSignOnService"]["url"] = current_app.config[
            "IDP_SSO_URL"
        ]
        json_settings["idp"]["x509cert"] = current_app.config["IDP_CERT"]
        json_settings["security"]["wantAssertionsEncrypted"] = current_app.config[
            "SP_SECURITY_ASSERTIONS_ENCRYPTED"
        ]

    return json_settings


def prepare_flask_request(request):
    """Return a dictionary in a format that OneLogin_Saml2_Auth uses during init"""
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
    """This route handles two important situations.

    The first, "sso" path, redirects a user to the IdP and sets a value of where to redirect
    the user to after they come back to this application. "next_page" is the resource in our
    CDN they originally requested but were redirected to this auth app because they were not
    authenticated. Keeping track of what they wanted is essential to the functionality of
    this solution.

     The second, "acs" path is handles the response back from the IDP. We should never encounter
     the path with "acs" in which a user is not authenticated, as they would not be redirected
     back from the IDP to us and not be authenticated.
    """
    saml_settings = load_saml_settings()
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, saml_settings)
    next_page = request.args.get("next")

    if not next_page or is_safe_url(next_page) is False:
        next_page = ""

    if "sso" in request.args:
        return redirect(auth.login(return_to=next_page))

    elif "acs" in request.args:
        auth.process_response()
        errors = auth.get_errors()
        if not auth.is_authenticated():
            # TODO: return a useful error to the user
            logging.error("User returned from IdP with no authentication")
            logging.error(f"Errors: {errors}")
            pass
        if len(errors) == 0:
            session["samlUserdata"] = auth.get_attributes()
            session["samlNameId"] = session["samlUserdata"][
                current_app.config["URN_UID"]
            ][0]
            session["samlSessionIndex"] = auth.get_session_index()
            return redirect(request.form["RelayState"])
        else:
            # TODO: return a useful error to the user
            logging.error(f"Errors occured processing IdP response: {errors}")
            logging.error(f"Last error reason: {auth.get_last_error_reason()}")
            pass


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
