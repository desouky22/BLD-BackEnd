from django.urls import path, include
from courses import views

urlpatterns = [
    path("get-all-courses/", views.GetAllCourses.as_view()),
    path("", views.Course.as_view()),
]
