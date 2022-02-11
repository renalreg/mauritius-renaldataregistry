from django import template

register = template.Library()


@register.filter
def page_window(page, last, size=7):
    """Generate pagination"""
    if page < size // 2 + 1:
        return range(1, min(size + 1, last + 1))
    return range(page - size // 2, min(last + 1, page + 1 + size // 2))


@register.simple_tag(takes_context=True)
def parameter_replace(context, **kwargs):
    """Encode page context"""
    page_context = context["request"].GET.copy()
    for page_key, page_number in kwargs.items():
        page_context[page_key] = page_number
    for page_key in [
        page_key for page_key, page_number in page_context.items() if not page_number
    ]:
        del page_context[page_key]
    return page_context.urlencode()
