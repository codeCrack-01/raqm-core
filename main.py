from hashlib import sha256


def generate_secure_hash(hash_key: str, params: dict) -> str:
    values = "&".join(param[1] for param in sorted(params.items()))
    my_str = hash_key + "&" + values
    print(my_str)
    my_bytes = str.encode(my_str)
    my_sha256 = sha256(my_bytes)
    return my_sha256.hexdigest()


if __name__ == '__main__':
    params = {
        "pp_Amount": "1000",
        "pp_MerchantID": "MC123",
        "pp_OrderID": "ORD-001"
    }

    print(generate_secure_hash("MYSECRET", params))
    print(generate_secure_hash("MYSECRET", params))
