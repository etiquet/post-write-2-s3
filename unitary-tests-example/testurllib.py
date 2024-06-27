import os
import urllib.parse
from urllib.parse import quote

# Example usage:
text = "/"
encoded_text = urllib.parse.quote(text, safe='')
print(f"Original text: {text}")
print(f"URL encoded text: {encoded_text}")