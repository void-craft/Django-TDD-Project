from django.urls import path
from .views import export_things_csv

urlpatterns = [
    path('export-things/', export_things_csv, name='export-things-csv'),
]