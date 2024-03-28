import os


class Config:
    COOKIE_NAME = os.getenv("COOKIE_NAME", default="mitlcdnauthjwt")
    COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")
    DEBUG = False
    ENV = os.getenv("FLASK_ENV", default="production")
    IDP_ENTITY_ID = os.getenv("IDP_ENTITY_ID")
    IDP_SSO_URL = os.getenv("IDP_SSO_URL")
    IDP_CERT = os.getenv("IDP_CERT")
    JWT_SECRET = os.getenv("JWT_SECRET")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SP_ENTITY_ID = os.getenv("SP_ENTITY_ID")
    SP_ACS_URL = os.getenv("SP_ACS_URL")
    SP_SECURITY_ASSERTIONS_ENCRYPTED = os.getenv(
        "SP_SECURITY_ASSERTIONS_ENCRYPTED", default=True
    )
    SP_CERT = os.getenv("SP_CERT")
    SP_KEY = os.getenv("SP_KEY")
    TESTING = False
    URN_UID = os.getenv("URN_UID", default="urn:oid:1.3.6.1.4.1.5923.1.1.1.6")


class DevelopmentConfig(Config):
    COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", default=False)
    DEBUG = True
    ENV = "development"
    SP_ACS_URL = os.getenv("SP_ACS_URL", default="http://localhost:5000/saml/?acs")
    SP_ENTITY_ID = os.getenv("SP_ENTITY_ID", default="http://localhost:5000/saml")
    SP_SECURITY_ASSERTIONS_ENCRYPTED = os.getenv(
        "SP_SECURITY_ASSERTIONS_ENCRYPTED", default=False
    )
    URN_UID = os.getenv("URN_UID", default="email")


class TestingConfig(Config):
    TESTING = True
    COOKIE_NAME = "mitlcdnauthjwt"
    COOKIE_DOMAIN = "example.com"
    ENV = "testing"
    IDP_ENTITY_ID = "http://example.com/shibboleth"
    IDP_SSO_URL = "http://example.com/idp/profile/SAML2/Redirect/SSO"
    IDP_CERT = "fakeIdPCert"
    JWT_SECRET = "supersecret"
    SECRET_KEY = "testing"
    SP_ENTITY_ID = "http://example.com/saml"
    SP_ACS_URL = "http://example.com/saml?acs"
    # Do not under any circumstances use this SP CERT or KEY in a deployed environment!
    SP_CERT = "MIIEGTCCAwGgAwIBAgIUCaZuYLMNiHxO9LEq+CgzB271rBswDQYJKoZIhvcNAQELBQAwgZsxCzAJBgNVBAYTAlVTMRYwFAYDVQQIDA1NYXNzYWNodXNldHRzMRIwEAYDVQQHDAlDYW1icmlkZ2UxFTATBgNVBAoMDEZha2UgQ29tcGFueTESMBAGA1UECwwJRmFrZSBVbml0MRQwEgYDVQQDDAtleGFtcGxlLmNvbTEfMB0GCSqGSIb3DQEJARYQZmFrZUBleGFtcGxlLmNvbTAeFw0yNDAzMjIxODE1MzlaFw0zNDAzMjAxODE1MzlaMIGbMQswCQYDVQQGEwJVUzEWMBQGA1UECAwNTWFzc2FjaHVzZXR0czESMBAGA1UEBwwJQ2FtYnJpZGdlMRUwEwYDVQQKDAxGYWtlIENvbXBhbnkxEjAQBgNVBAsMCUZha2UgVW5pdDEUMBIGA1UEAwwLZXhhbXBsZS5jb20xHzAdBgkqhkiG9w0BCQEWEGZha2VAZXhhbXBsZS5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCkOCiZwvEpRjV0mSSX8jYYgqpfZUzQ+6YuXOBBrkOEVqMRO5pnIi/pE+QXeRfujgE9NcytFYrdr6w7aojcovMweroAdw0BCSuykfluxfpEA1p5fUi/p6rC6lgsd36ByKtZD6IX9xOw0qyh6Ch9YQg+U7atT+qFJnjlewX/EexGfGI14DNlTFSWalRxXiaQorf+9Cc6RVEqqk0WTcE903etqMIuRg/fOrV/HhbqPT3tLpdXmLA1wijRX3DIpWlgqOIFxQfMgy8P0Fn5tuSNah45o3rJLhAMWxttCEDUl17EjLcwZYHAREHTpCWx7BJ0FUkNypPT/Ub3e08EbOJlJOI3AgMBAAGjUzBRMB0GA1UdDgQWBBRCfiJzC0jNaQAXdp+oS29sDs31djAfBgNVHSMEGDAWgBRCfiJzC0jNaQAXdp+oS29sDs31djAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQBbqOqflhNsWuuIciBeOixu/SeG7mh9wSOV0VhxnAdlWLHQekcXYi5i5eFH9n1U90BktIPWWlOQpqocVQIvAed8TDgMwcr+64ZmN9BGGmF97OB5oD0SZGxs5IyB3O+EnR26HD4WXum6x0tCoLyV3heSRn9ff91bcRQfrs5ZLGuJFobcwDGeTC1YTnGg0mEWSV9Ao8w100qG/FvFpWRz4VQBajsEHvuy4JQXl56+kdvW60M3iXbawNgz+Ht8lebeZ5AI3mhK+qk5FUHyogemFcujtFSdeZ3CS/pAmmfAJdF2SGShVwf6twHS+8jipD1O+Y4SdyD1BjvO8tYXE9rB1XgH"
    SP_KEY = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCkOCiZwvEpRjV0mSSX8jYYgqpfZUzQ+6YuXOBBrkOEVqMRO5pnIi/pE+QXeRfujgE9NcytFYrdr6w7aojcovMweroAdw0BCSuykfluxfpEA1p5fUi/p6rC6lgsd36ByKtZD6IX9xOw0qyh6Ch9YQg+U7atT+qFJnjlewX/EexGfGI14DNlTFSWalRxXiaQorf+9Cc6RVEqqk0WTcE903etqMIuRg/fOrV/HhbqPT3tLpdXmLA1wijRX3DIpWlgqOIFxQfMgy8P0Fn5tuSNah45o3rJLhAMWxttCEDUl17EjLcwZYHAREHTpCWx7BJ0FUkNypPT/Ub3e08EbOJlJOI3AgMBAAECggEAB4L0irHCqMHvGXdN0LNznQBmZ9xUoDulNUFcMqaxAc+ZznLujO+vAFc/op2swoIRysYGfRcwqxOT+GasRS52RZU/huqyQvfP62EqvHyR6bn0bjYUytmuVtqlni/4Z690u+Q2q7ZKd3N+LldHsmeVjOPYYjhMa0lOfu2TmkBJA0wSHlEQRnOclfWw9IGYQYYXbtQzQhLNTHRBA4plokcWw/KXH8qhQbAIk1eEnsqOVJk5XrdPpBZSwfWZ9VXhHi8EHSeRqbRsGtQ2RisKJfTEKFFTDVyEjuUUHN+Eghx7i/PCVE0dlytzKSytNo86AtEO9bS6Zb5WgjhsdpUpBpWaaQKBgQDS+oTrdNx1io3nWODMxlZ9hZd+x6Fc9gPHcqK50htOAT6bFrEC4B9z1xqlkGj3qprK8mYtPEGRxINziO53O7ZQsWTRXv+LL+Az2wMfnYHhKkybUpLAA+ENW6EwmgMISWjpUNmJht8POLYQiZFmU9yN1p5+6S30uFBG/2Msb5HjaQKBgQDHQz6+1MXdMdbuE9YACAeqt8C/KMokgAw+VJZmYMxAW5ozt6iLwKHE8pnLUx15WSMDiz2v8NGHDUi8kxw92Cww1/MF3XMgihTENPlNx1EwGv41HuumlQaXWrrBFkC2+1WYg2DcvovtDU+fJ7gGiP1f/Nkh3Lo+jYDCmZPXscMEnwKBgQCZJs5SdfSLRtcX94bIX7ntSIret1/FsbiwkeDab1Du4SxnPKOmaLesSZvIT/pCvw+6/xd5AuK+RB8AQYiJ+UixbvS2n/V1Pn3MZtHvo1Di+Oe/YMOyq541KizqsQI+g7uqksw3bzaBQDO58YMg+wOB2ygXDIIVwa5Uu5NscFlA8QKBgFSA5w4ky9iXd0+1585RmXbDwKEQ2lEKYKbaVoIKUPSGJGoEXB0QT0pnm+NHVzuMGrY5CasglKsSbiNSu+paT7tTCYQWOum0xUPEN2nNuleNSvsaJtOZZZcwafzSxBUVl2I7bQuQX2TjfT3AqWFUHSfk4exjYDSA6/cbDECv6UV/AoGADRkoNPvkeLnFMt/3Z6ZCmUxyFJ4MgtwmvYDDa5TW1gifXCRp71g0JXAVCk78oNYk2Q69nAKlG0+ST+jTOqMvxb9UNMt5j01q5CLxyzuxQoGGVpq/b4fwpt33VTMPNtffzeq1oY/6rYy0TSKFFIxE3rrjOpo/1b0DeES0Yb77H1E="
