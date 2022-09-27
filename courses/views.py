import json

from django import forms
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views import View

from courses import models


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
    return form1.is_valid()


def get_all_courses():
    courses = models.Course.objects.all().values()
    ret = {}
    for course in courses:
        ret[course["id"]] = course
    return ret


def get_course_by_id(id):
    print(models.Course.objects.all())
    courses = models.Course.objects.all().filter(id=id).values()
    if len(courses):
        return courses[0]
    return {"msg": "No Course exist with this id"}


def assign_course(course, body):
    course["name"] = body["name"]
    course["description"] = body["description"]


class Course(View):
    def get(self, request):
        id = request.GET.get("id", "")
        if id == "":
            return JsonResponse(get_all_courses())
        id = int(id)
        return JsonResponse(get_course_by_id(id))

    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        if is_data_valid(body):
            new_course = models.Course()
            assign_course(new_course, body)
            try:
                new_course.save()
                return HttpResponse("DONE GG")
            except IntegrityError:
                return HttpResponse("invalid data")
        else:
            return JsonResponse({"msg": "the data is not valid"})

    def delete(self, request):
        body = request.body.decode("utf-8")
        body = json.loads(body)
        course = models.Course.objects.filter(id=int(body["id"]))
        if len(course):
            course = course[0]
            course.delete()
            return HttpResponse("Deleted gg")
        else:
            return HttpResponse("there is no Course with this id")

    def put(self, request):
        body = request.body.decode("utf-8")
        body = json.loads(body)
        if is_data_valid(body):
            id = int(body["id"])
            course = models.Course.objects.filter(id=id).values()
            if len(course):
                course = course[0]
                assign_course(course, body)
                try:
                    course.save()
                    return HttpResponse("DONE gg update")
                except IntegrityError:
                    return HttpResponse("the data is not valid")
            else:
                return HttpResponse("There is no Course with this id")
        else:
            return HttpResponse("the data is not valid")
