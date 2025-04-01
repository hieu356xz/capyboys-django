from typing import Iterable, Sequence
from django.db.models.manager import BaseManager

class QueryParams:
    def __init__(self, query_dict: Iterable = None, accept_keys: Sequence = None):
        self.params = {}

        if query_dict:
            if accept_keys:
                self.params = { key: value for key, value in query_dict.items() 
                                if value and (key in accept_keys)}
            else:
                self.params = { key: value for key, value in query_dict.items() if value}

    def set(self, key, value):
        if value is not None:
            self.params[key] = value
        return self
    
    def remove(self, key):
        if key in self.params:
            del self.params[key]
        return self

    def get(self, key, default=None):
        return self.params.get(key, default)

    def get_if_not_in(self, key, iterable: Iterable, default=None):
        value = self.params.get(key)
        if value not in iterable:
            value = default

        return value

    def build_url(self, base_path: str):
        query_string = "&".join([f"{key}={value}" for key, value in self.params.items()])
        if not query_string:
            return base_path
        
        return f"{base_path}?{query_string}"
    
    def without(self, *keys):
        new_params = QueryParams(self.params)
        for k in keys:
            new_params.remove(k)
        
        return new_params

def get_queryset_with_filter(queryset: BaseManager, querystring: str, *args, **kwargs):
    if not querystring:
        return queryset
    
    model_class = queryset.model

    if queryset.exists():
        return queryset.filter(*args, **kwargs)
    else:
        return model_class.objects.filter(*args, **kwargs)