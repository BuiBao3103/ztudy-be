def decode_emoji(text):
    """
    Decode emoji from database format to display format
    """
    if not text:
        return text
    return bytes(text.encode()).decode('unicode-escape') 