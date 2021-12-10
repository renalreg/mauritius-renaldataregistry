from django import template

register = template.Library()


@register.filter
def page_window(page, last, size=7):
    if page < size // 2 + 1:
        return range(1, min(size + 1, last + 1))
    else:
        return range(page - size // 2, min(last + 1, page + 1 + size // 2))


@register.simple_tag(takes_context=True)
def parameter_replace(context, **kwargs):
    d = context["request"].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
