import json
from sqlite3 import IntegrityError

from django import forms
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views import View

from users import models


class BasicFormDefault(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password = forms.PasswordInput()
    birth_date = forms.DateField()


def is_data_valid(body):
    form1 = BasicFormDefault(body)
    return form1.is_valid()


# Create your views here.
def get_all_users():
    all_users = models.User.objects.all().values()
    ret = {}
    for user in all_users:
        ret[user["id"]] = user
    return ret


def get_user_by_id(id):
    all_users = models.User.objects.all().filter(id=id).values()
    if len(all_users):
        return all_users[0]
    return {"msg": "No user exist with this id"}


def assign_user(user, body):
    user.first_name = body["first_name"]
    user.last_name = body["last_name"]
    user.email = body["email"]
    user.birth_date = body["birth_date"]
    user.password = body["password"]


def revert_user(user, old_user):
    user.first_name = old_user.first_name
    user.last_name = old_user.last_name
    user.email = old_user.email
    user.password = old_user.password
    user.birth_date = old_user.birth_date


class Users(View):
    def get(self, request):
        id = request.GET.get("id", "")
        if id == "":
            return JsonResponse(get_all_users())
        id = int(id)
        return JsonResponse(get_user_by_id(id))

    def post(self, request):
        body = request.body.decode("utf-8")
        body = json.loads(body)
        if is_data_valid(body):
            new_user = models.User()
            assign_user(new_user, body)
            try:
                new_user.save()
                return HttpResponse("DONE gg")
            except IntegrityError:
                return HttpResponse("This Email exists")
        else:
            return JsonResponse({"msg": "the data is not valid"})

    def delete(self, request):
        body = request.body.decode("utf-8")
        body = json.loads(body)
        user = models.User.objects.filter(id=int(body["id"]))
        if len(user):
            user = user[0]
            user.delete()
            return HttpResponse("Deleted GG")
        else:
            return HttpResponse("there is no user with this id")

    def put(self, request):
        body = request.body.decode("utf-8")
        body = json.loads(body)
        if is_data_valid(body):
            id = int(body["id"])
            user = models.User.objects.filter(id=id)
            if len(user):
                user = user[0]
                assign_user(user, body)
                try:
                    user.save()
                    return HttpResponse("DONE gg update")
                except IntegrityError:
                    return HttpResponse("the data is not valid")
            else:
                return HttpResponse("There is no user exist with this ID")
        else:
            return HttpResponse("Data is not valid")


class AgeUtility(View):
    def get(self, request):
        body = request.body.decode("utf-8")
        body = json.loads(body)
        age = int(body["age"])
        all_users = models.User.objects.all().order_by("birth_date")
        output = []
        for user in all_users:
            if user.age > age:
                output.append(user)
            else:
                break

        return HttpResponse(output)
