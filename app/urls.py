from django.urls import path
from app import views
 
urlpatterns = [
    path('', views.home, name='home'),
    path('upload_files', views.upload_files, name='upload_files'),
    path('compare/', views.compare_columns, name='compare_columns'),
    path('compare_json/', views.compare_json, name='compare_json'),
    path('compare_json_ajax/', views.compare_json_ajax, name='compare_json_ajax')
]