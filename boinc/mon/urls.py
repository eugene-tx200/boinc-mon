from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('task_status', views.task_status, name='task_status'),
    path('', TemplateView.as_view(template_name="mon/index.html")),
]
