import re

from django.forms.models import model_to_dict
from django.http import JsonResponse

from companies.models import *


def parse_params(request, object_meta):
    params_from_get = request.GET
    sort_param = params_from_get.get('sort_by')
    filter_params = {}

    if not(sort_param is None):
        # todo multiple sorting
        result = re.match(r'[+\-]\w+', sort_param)

        if result is None:
            return JsonResponse({'message':
                                     'Not correct sort_by param syntax, example: '
                                     'sort_by=+(field_name) or -(field_name)'},
                                status=400)
    else:
        sort_param = '?'

    limit = params_from_get.get('limit')

    fields = [f.name for f in object_meta.get_fields()]

    for field in fields:
        filter_param_value = params_from_get.get(field)
        if not(filter_param_value is None):
            filter_params[field] = filter_param_value

    return filter_params, sort_param, limit


def person(request, person_id=None):
    response_dict = {}

    if request.method == 'GET':
        # limit >= 1

        # and by fields (check field exist)

        if not (person_id is None):
            try:
                person = Person.objects.get(pk=person_id)
                person = model_to_dict(person)
                response_dict['data'] = person
            except:
                return JsonResponse({'message':
                                         format("No one person found in db by given clauses")}, status=204)
        else:
            filter_params, order_by, limit = parse_params(request, Person._meta)

            persons = Person.objects.filter(**filter_params).order_by(order_by)[:limit]
            persons = persons.values()
            persons = [person for person in persons]

            response_dict['data'] = persons
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

    return JsonResponse(response_dict)
