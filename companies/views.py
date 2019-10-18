import json
import re

from django.apps import apps
from django.db.models.fields.related import ForeignKey
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
                # via raise?
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


def get_dict_object_by_post_params(request):
    # проверка на внешние ключи, так как в этом случае надо получить сам объект
    # из-за автогенерации кода мы не знаем какие именно внешние ключи нам надо будет получить
    # поэтому тут усложнение
    app_models = apps.get_app_config('companies').get_models()

    person_request_data = json.loads(request.body)

    for field in Person._meta.get_fields():
        if isinstance(field, ForeignKey):
            field_name = str(field).split('.')[-1]
            for model in app_models:
                if (field_name == model.__name__.lower()):
                    try:
                        person_request_data[field_name] = model.objects.get(id=person_request_data[field_name])
                    except Exception as e:
                        raise Exception('Error when try get foreign_key_object: {0}, err: {1}'.format(field_name,
                                                                                                      str(e)))
                    break

    return person_request_data


def person(request, person_id=None):
    response_dict = {"success": True}

    # global try?
    if request.method == 'GET':
        # todo: validation excess fields
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
        # todo: validation excess fields

        person_dict_from_post = get_dict_object_by_post_params(request)

        person = Person(**person_dict_from_post)

        try:
            person.save()
        except Exception as e:
            return JsonResponse({'message': 'Error when try save person: {0}, err: {1}'.format(person, str(e))},
                                status=500)

        return JsonResponse(response_dict)
    elif request.method == 'PUT':
        # todo: validation excess fields

        if person_id is None:
            return JsonResponse({'message': 'person_id not set'}, status=400)

        try:
            person_dict_from_post = get_dict_object_by_post_params(request)
        except Exception as e:
            return JsonResponse({'message': 'Error when try get_object_by_post_params request: '
                                            '{0}, err: {1}'.format(request, str(e))},
                                status=500)

        try:
            Person.objects.filter(id=person_id).update(**person_dict_from_post)
        except Exception as e:
            return JsonResponse({'message': 'Error when try update person: {0}, err: {1}'.format(person_dict_from_post,
                                                                                                 str(e))},
                                status=500)

        return JsonResponse(response_dict)
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
