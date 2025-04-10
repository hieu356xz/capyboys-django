# yourapp/templatetags/pagination_tags.py
from urllib.parse import urlparse, parse_qs
from django import template
from home.utils import QueryParams
import html

register = template.Library()

@register.simple_tag
def get_page_range(current_page, total_pages):
    current_page = int(current_page)
    total_pages = int(total_pages)
    
    start = max(1, current_page - 2)
    end = min(total_pages, current_page + 2)
    
    return range(start, end + 1)

@register.simple_tag
def set_query_param(url: str, param: str, value: str):
    url = html.unescape(url)
    parsed_url = urlparse(url)
    query_dict = { key: value[-1] for key, value in parse_qs(parsed_url.query).items()}
    query_params = QueryParams(query_dict)

    query_params.set(param, value)
    return query_params.build_url(parsed_url.path)

@register.simple_tag
def remove_query_param(url: str, param: str):
    url = html.unescape(url)
    parsed_url = urlparse(url)
    query_dict = { key: value[-1] for key, value in parse_qs(parsed_url.query).items()}
    query_params = QueryParams(query_dict)

    return query_params.without(param).build_url(parsed_url.path)

@register.filter
def calc_subtotal(price, count):
    price = float(price)
    count = int(count)
    subtotal = price * count
    return f"{subtotal:,.0f}"

@register.filter
def is_absolute_url(url):
    return bool(urlparse(str(url)).netloc)

@register.filter
def float_format(value, format_string):
    try:
        return f"{float(value):{format_string}}"
    except (ValueError, TypeError):
        return value