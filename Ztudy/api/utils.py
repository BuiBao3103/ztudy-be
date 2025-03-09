import random
import string

def generate_unique_code(model, field_name, length):
    chars = string.ascii_lowercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not model.objects.filter(**{field_name: code}).exists():
            return code

def encode_emoji(text):
    """Chuyển emoji thành mã Unicode trước khi lưu vào database."""
    return text.encode('unicode_escape').decode() if text else text

def decode_emoji(text):
    """Chuyển mã Unicode thành emoji khi lấy dữ liệu từ database."""
    return text.encode().decode('unicode_escape') if text else text
