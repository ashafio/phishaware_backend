import re
from urllib.parse import urlparse

def extract_features(url: str):
    parsed = urlparse(url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    url_length = len(url)
    hostname_length = len(hostname)
    path_length = len(path)
    query_length = len(query)

    path_segments_count = len([p for p in path.split("/") if p])

    num_dots = url.count(".")
    num_hyphens = url.count("-")
    num_at = url.count("@")
    num_question = url.count("?")
    num_ampersand = url.count("&")
    num_equals = url.count("=")
    num_underscore = url.count("_")
    num_slash = url.count("/")

    num_digits = sum(c.isdigit() for c in url)
    num_letters = sum(c.isalpha() for c in url)
    num_special_chars = len(re.findall(r'[^a-zA-Z0-9]', url))

    length = max(len(url), 1)
    ratio_digits = num_digits / length
    ratio_letters = num_letters / length

    uses_https = 1 if url.startswith("https") else 0
    is_ip_address = 1 if re.match(r'\d+\.\d+\.\d+\.\d+', hostname) else 0
    contains_login = 1 if "login" in url.lower() else 0

    return [
        url_length,
        hostname_length,
        path_length,
        query_length,
        path_segments_count,
        num_dots,
        num_hyphens,
        num_at,
        num_question,
        num_ampersand,
        num_equals,
        num_underscore,
        num_slash,
        num_digits,
        num_letters,
        num_special_chars,
        ratio_digits,
        ratio_letters,
        uses_https,
        is_ip_address,
        contains_login,
    ]