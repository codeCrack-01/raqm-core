import base64


def generate_auth_header(username: str, password: str) -> str:
    encoded_string = str.encode(username + ":" + password)
    base64_encoded = base64.b64encode(encoded_string)
    return "Basic " + base64_encoded.decode()
