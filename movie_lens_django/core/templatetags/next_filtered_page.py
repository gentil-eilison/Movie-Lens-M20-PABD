from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def next_filtered_page(context, **kwargs):
    query = context["request"].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()
