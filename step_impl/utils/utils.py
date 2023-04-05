import jwt
import datetime
import uuid


SECRET_KEY = "django-insecure-5spx1k$(w)xncdhk&z%&b9ohztpcyjk9u(t8swf3$53e+@z69l"


def generate_auth_header(account_id):
    """
    Example Auth0 access token
    {
      "https://www.zenbusiness.com/email": "eugene.fabrikant+dev@zenbusiness.com",
      "https://www.zenbusiness.com/account_uuid": "3308d07b-d946-4a6f-b3ca-3c44481f125",
      "iss": "https://login.dev.zenbusiness.com/",
      "sub": "auth0|623bd591bfade6006f0170dd",
      "aud": [
        "https://zen-business-core-api",
        "https://zen-business-dev.us.auth0.com/userinfo"
      ],
      "iat": 1649275993,
      "exp": 1649362393,
      "azp": "liinIbvP490BKJxJX1TGmNxlTvBcVRAu",
      "scope": "openid profile email",
      "permissions": []
    }
    """
    auth_header = jwt.encode(
        {
            "token_type": "access",
            "https://www.zenbusiness.com/email": "unittest@example.com",
            "https://www.zenbusiness.com/account_uuid": account_id,
            "sub": f"auth0|{str(uuid.uuid4())}",
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
            "scope": "openid profile email",
            "permissions": [],
        },
        SECRET_KEY,
    )
    return f"Bearer {auth_header}"
