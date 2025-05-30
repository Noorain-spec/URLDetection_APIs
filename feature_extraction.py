import joblib
import pandas as pd
import re
from urllib.parse import urlparse
from tld import get_tld

#model = joblib.load('ml_model/url_model.joblib')
#model_features = joblib.load('ml_model/model_features.joblib')

# Defined all feature extraction functions
def process_tld(url):
    try:
        res = get_tld(url, as_object=True, fail_silently=False, fix_protocol=True)
        return res.parsed_url.netloc
    except:
        return None

def abnormal_url(url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    return 1 if re.search(hostname, url) else 0

def httpSecure(url):
    return 1 if urlparse(url).scheme == 'https' else 0

def digit_count(url):
    return sum(c.isdigit() for c in url)

def letter_count(url):
    return sum(c.isalpha() for c in url)

def Shortining_Service(url):
    match = re.search(r'bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co', url)  # Add all patterns you had
    return 1 if match else 0

def having_ip_address(url):
    match = re.search(r'(([0-9]{1,3}\.){3}[0-9]{1,3})', url)
    return 1 if match else 0

# Extract features from a single new URL (must match model features exactly)
def extract_features(url, model_features):
    url = re.sub(r'www\.', '', url)  # remove www.
    data = {
        'url_len': len(url),
        '@': url.count('@'),
        '?': url.count('?'),
        '-': url.count('-'),
        '=': url.count('='),
        '.': url.count('.'),
        '#': url.count('#'),
        '%': url.count('%'),
        '+': url.count('+'),
        '$': url.count('$'),
        '!': url.count('!'),
        '*': url.count('*'),
        ',': url.count(','),
        '//': url.count('//'),
        'abnormal_url': abnormal_url(url),
        'https': httpSecure(url),
        'digits': digit_count(url),
        'letters': letter_count(url),
        'Shortining_Service': Shortining_Service(url),
        'having_ip_address': having_ip_address(url)
    }
    df = pd.DataFrame([data])

    # Make sure all columns exist and in the right order
    for col in model_features:
        if col not in df.columns:
            df[col] = 0
    df = df[model_features]
    return df

