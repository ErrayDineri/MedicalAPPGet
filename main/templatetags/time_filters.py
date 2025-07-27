from django import template

register = template.Library()

@register.filter
def format_duration(seconds):
    """
    Convert seconds to a human-readable duration string in French.
    """
    if not seconds:
        return "un délai indéterminé"
    
    seconds = int(seconds)
    
    # Convert to different units
    if seconds < 60:
        return f"{seconds} seconde{'s' if seconds != 1 else ''}"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} heure{'s' if hours != 1 else ''}"
    else:
        days = seconds // 86400
        return f"{days} jour{'s' if days != 1 else ''}"
