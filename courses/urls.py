from django.urls import path

from courses import views

urlpatterns = [
    path("", views.Course.as_view()),
]
