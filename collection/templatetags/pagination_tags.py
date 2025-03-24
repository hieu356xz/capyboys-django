# yourapp/templatetags/pagination_tags.py
from django import template

register = template.Library()

@register.simple_tag
def get_page_range(current_page, total_pages):
    current_page = int(current_page)
    total_pages = int(total_pages)
    
    start = max(1, current_page - 2)
    end = min(total_pages, current_page + 2)
    
    return range(start, end + 1)
