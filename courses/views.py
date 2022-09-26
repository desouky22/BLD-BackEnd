from django import forms
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
import json
from django.views import View
from .db import *

id_exist = all_courses()


class BasicFormCustom(forms.Form):
    errors1 = {
        'required': 'This field is required desouky',
        'invalid': 'Enter a valid value desouky',
        "min_length": "u need to enter more chars :)",
        "max_length": "u need to enter less chars :)"
    }
    name = forms.CharField(min_length=10, max_length=100, required=True, error_messages=errors1)
    description = forms.CharField(min_length=10, max_length=100, required=True, error_messages=errors1)


class BasicFormDefault(forms.Form):
    name = forms.CharField(min_length=10, max_length=100, required=True)
    description = forms.CharField(min_length=10, max_length=100, required=True)


def is_data_valid(body):
    form1 = BasicFormCustom(body)
    return form1.is_valid() and (body["id"] not in id_exist.keys() or not id_exist[body["id"]])


def show_custom_error(body):
    form1 = BasicFormCustom(body)
    output = {}
    if body["id"] in id_exist.keys() and id_exist[body["id"]]:
        output["id"] = "there is a course exist with the same ID"

    for data in ("name", "description"):
        if data in form1.errors.as_data().keys():
            for item in form1.errors.as_data()[data][0]:
                output[data] = item
    return output


class Course(View):
    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        if is_data_valid(body):
            writeDB(body)
            id_exist[body["id"]] = True
            return JsonResponse(body)
        else:
            return JsonResponse(show_custom_error(body))

    def delete(self, request):
        body = request.body.decode("utf-8")
        body = json.loads(body)
        id = body["id"]
        if id in id_exist.keys() and id_exist[id]:
            id_exist[id] = False
            return JsonResponse(delete_with_id(id))

        return HttpResponse("this id is not exist")

    def get(self, request):
        id = request.GET.get("id", "")
        id = int(id)
        return JsonResponse(get_course_with_id(id))

    def put(self, request):
        body = request.body.decode("utf-8")
        body = json.loads(body)
        if is_data_valid(body):
            new_course = update_course_with_id(body)
            return JsonResponse(new_course)
        return HttpResponse("the course doesn't exist")


class GetAllCourses(View):
    def get(self, request):
        data = {"courses": readDB()}
        return JsonResponse(data)
