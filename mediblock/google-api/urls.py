from django.urls import path
from . import views

urlpatterns = [
    path('analyze/<medical_bill_id>', views.analyze)
]
