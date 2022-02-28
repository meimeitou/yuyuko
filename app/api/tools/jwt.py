import jwt
from typing import Tuple

def decode_jwt(encode: str) -> Tuple[dict, dict]:
    body = jwt.decode(encode, options={"verify_signature": False})
    head = jwt.get_unverified_header(encode)
    return head,body
