import random
import string

def generate_unique_code(model, field_name, length):
    chars = string.ascii_lowercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not model.objects.filter(**{field_name: code}).exists():
            return code
