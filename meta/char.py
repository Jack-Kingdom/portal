"""
declare url allow character
check follow link for more details:
https://en.wikipedia.org/wiki/Percent-encoding
"""

number = [chr(i + ord('0')) for i in range(10)]
lower = [chr(i + ord('a')) for i in range(26)]
upper = [chr(i + ord('A')) for i in range(26)]
special = ['-', '_', '.', '~']

url_unreserved_characters = number + lower + upper + special
url_unreserved_characters_length = len(url_unreserved_characters)
