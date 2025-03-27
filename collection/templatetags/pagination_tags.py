# yourapp/templatetags/pagination_tags.py
from urllib.parse import urlparse, parse_qs
from django import template
from home.utils import QueryParams

register = template.Library()

@register.simple_tag
def get_page_range(current_page, total_pages):
    current_page = int(current_page)
    total_pages = int(total_pages)
    
    start = max(1, current_page - 2)
    end = min(total_pages, current_page + 2)
    
    return range(start, end + 1)

@register.filter
def add_query_param(url: str, param: str):
    parsed_url = urlparse(url)
    query_dict = { key: value[-1] for key, value in parse_qs(parsed_url.query).items()}
    query_params = QueryParams(query_dict)

    param_name, param_value = param.split('=', 1)
    query_params.set(param_name, param_value)
    return query_params.build_url(parsed_url.path)