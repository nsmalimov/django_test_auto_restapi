import re

from django.forms.models import model_to_dict
from django.http import JsonResponse

from companies.models import *


def parse_params(request, object_meta):
    params_from_get = request.GET
    sort_param = params_from_get.get('sort_by')
    filter_params = {}
    error_response = None
    limit = params_from_get.get('limit')

    if not (sort_param is None):
        # multiple sorting
        # https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/#
        sort_param_elems = sort_param.split(',')
        sort_param = []

        # можно написать в 1 регулярке (проверять повторы)
        # но всё равно придётся сплитить
        for sort_param_elem in sort_param_elems:
            if re.match(r'[+\-]\w+', sort_param_elem) is None:
                error_response = JsonResponse({'message':
                                                   'Not correct sort_by param syntax, example: '
                                                   'sort_by=-field_name,+field_name'},
                                              status=400)
                return filter_params, sort_param, limit, error_response
            else:
                sort_param.append(sort_param_elem)
    else:
        sort_param = '?'

    fields = [f.name for f in object_meta.get_fields()]

    for field in fields:
        filter_param_value = params_from_get.get(field)
        if not (filter_param_value is None):
            filter_params[field] = filter_param_value

    return filter_params, sort_param, limit, error_response


def person(request, person_id=None):
    response_dict = {"success": True}

    # global try?
    if request.method == 'GET':
        if not (person_id is None):
            try:
                person = Person.objects.get(id=person_id)
            except Exception as e:
                return JsonResponse({'message': 'No one person found in db by id {0}, err: {1}'.format(person_id,
                                                                                                       str(e))},
                                    status=204)
            person = model_to_dict(person)
            response_dict['data'] = person
        else:
            filter_params, order_by, limit, error_reponse = parse_params(request, Person._meta)

            if not (error_reponse is None):
                return error_reponse

            try:
                persons = Person.objects.filter(**filter_params).order_by(order_by)[:limit]
            except Exception as e:
                return JsonResponse({'message': 'Error when try filter person by filter_params: {0}, order_by: {1},'
                                                'limit: {2}, err: {3}'.format(filter_params, order_by, limit, str(e))},
                                    status=500)

            persons = persons.values()
            persons = [person for person in persons]

            response_dict['data'] = persons
    elif request.method == 'POST':
        print(request.POST)
    elif request.method == 'PUT':
        if person_id is None:
            return JsonResponse({'message': 'person_id not set'}, status=400)
    elif request.method == 'DELETE':
        if person_id is None:
            return JsonResponse({'message': 'person_id not set'}, status=400)
        try:
            person = Person.objects.get(id=person_id)
        except Exception as e:
            return JsonResponse({'message': 'No one person found in db by id: {0}, err: {1}'.format(person_id, str(e))},
                                status=204)
        try:
            person.delete()
        except Exception as e:
            return JsonResponse({'message': 'Error when try delete person with id: {0}, err: {1}'.format(person_id,
                                                                                                         str(e))},
                                status=500)

    return JsonResponse(response_dict)
