from django.urls import path, include
from . import views

urlpatterns = [
    path('analyze/<medical_bill_id>', views.analyze)
]
