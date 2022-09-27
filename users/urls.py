from django.urls import path

from users import views

urlpatterns = [
    path("age/", views.AgeUtility.as_view()),
    path("", views.Users.as_view()),
]
