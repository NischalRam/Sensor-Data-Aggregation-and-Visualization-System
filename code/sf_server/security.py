import string
import random

chars = " " + string.punctuation + string.digits + string.ascii_letters
chars_list = list(chars)

key = chars_list.copy()
random.shuffle(key)

print(f"chars: {chars_list}")
print(f"key  : {key}")
