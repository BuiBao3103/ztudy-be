from django.utils.html import format_html
from api.utils import decode_emoji


def get_decoded_field(obj, field_name):
    """
    Get a decoded (emoji-friendly) representation of a field value
    
    Args:
        obj: The model instance
        field_name: The name of the field to decode
    
    Returns:
        Decoded string value
    """
    value = getattr(obj, field_name, None)
    if value is not None:
        return decode_emoji(value)
    return None


def render_image_preview(url, width=100, height="auto"):
    """
    Render an image preview with styled HTML
    
    Args:
        url: The image URL
        width: Width in pixels (default: 100)
        height: Height value (default: "auto")
    
    Returns:
        Formatted HTML for image preview
    """
    if not url:
        return "No image"
    
    return format_html(
        '<img src="{}" width="{}" height="{}" style="border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />', 
        url, width, height
    )


def render_url_link(url, display_text=None):
    """
    Render a clickable URL link
    
    Args:
        url: The URL to link to
        display_text: Optional text to display (defaults to URL itself)
    
    Returns:
        Formatted HTML for clickable link
    """
    if not url:
        return "No URL"
    
    display = display_text or url
    return format_html('<a href="{}" target="_blank">{}</a>', url, display) 