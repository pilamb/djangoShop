# -*- coding: utf-8 -*-
import re
from django.db.models import Q


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    """
    Chops of string in sole words, deleting spaces and grouping words
    """
    return [
        normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def search_filter(string, campos):
    """
    Returns a query object of Q type
    :param string:
    :param campos:
    :return:
    """
    query = None # Query to search for every search term
    terms = normalize_query(string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in campos:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
