import re


def extract_urls(text):
    # Regex pattern for finding URLs including those with IPv4 and IPv6 addresses
    url_pattern = (
        r'https?://'  # http:// or https://
        r'(?:'  # One of:
        r'(?:\d{1,3}\.){3}\d{1,3}'  # IPv4 address
        r'|'  # or
        r'\[?(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\]?'  # IPv6 address
        r'|'  # or
        r'(?:[-\w.]|(?:%[\da-fA-F]{2}))+'  # domain name
        r')'
        r'(?:/\S*)?'  # Path
    )
    # Finding all matches in the text
    urls = re.findall(url_pattern, text)
    return urls

