# coding: utf-8
import copy

def query_from_argument(model, data):
    query = model.query.filter_by(**data)
    return query

def query_from_json(model, query, data={}):
    new_query = copy.deepcopy(query)
    for key, value in data.items():
        new_query = new_query.filter(model.data[key] == value)
    return new_query