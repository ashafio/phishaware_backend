import re
from urllib.parse import urlparse

def extract_features(url: str):
    # 1. Strip protocol and www so the model can't use them to 'cheat'
    url_clean = url.replace("https://", "").replace("http://", "").replace("www.", "")
    
    # 2. Parse the clean version
    parsed = urlparse(f"http://{url_clean}") # dummy protocol for parsing
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    
    length = max(len(url_clean), 1)

    # 3. These 22 features are now "Protocol Neutral"
    features = [
        len(url_clean),
        len(hostname),
        len(path),
        hostname.count("."),
        path.count("/"),
        url_clean.count("-"),
        url_clean.count("@"),
        url_clean.count("?"),
        url_clean.count("&"),
        url_clean.count("="),
        url_clean.count("_"),
        sum(c.isdigit() for c in url_clean),
        sum(c.isalpha() for c in url_clean),
        len(re.findall(r'[^a-zA-Z0-9]', url_clean)),
        sum(c.isdigit() for c in url_clean) / length,
        1 if "login" in url_clean.lower() else 0,
        1 if "verify" in url_clean.lower() else 0,
        1 if "update" in url_clean.lower() else 0,
        1 if "account" in url_clean.lower() else 0,
        1 if "secure" in url_clean.lower() else 0,
        hostname.count("-"),
        1 if re.match(r'\d+\.\d+\.\d+\.\d+', hostname) else 0,
    ]
    return features