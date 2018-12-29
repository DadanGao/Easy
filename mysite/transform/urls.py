from django.urls import path

from . import views

app_name = 'transform'
urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.transform, name='transform'),
    path('download/', views.file_download, name='download'),
]